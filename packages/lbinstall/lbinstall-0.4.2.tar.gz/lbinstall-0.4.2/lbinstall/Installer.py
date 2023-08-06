###############################################################################
# (c) Copyright 2016 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''
Installer for the for LHCb Software.
All it needs is the name of a local directory to use to setup the install area
and the yum repository configuration.

@author: Ben Couturier
'''
import logging
import os
import sys
import traceback
from os.path import abspath
import shutil

from lbinstall.Model import IGNORED_PACKAGES
from lbinstall.InstallAreaManager import InstallArea
from lbinstall.PackageManager import PackageManager
from lbinstall.extra.RPMExtractor import sanitycheckrpmfile


# Little util to find a file in a directory tree
def findFileInDir(basename, dirname):
    ''' Look for a file with a given basename in a
    directory struture.
    Returns the first file found... '''
    for root, _, files in os.walk(dirname, followlinks=True):
        if basename in files:
            return abspath(os.path.join(root, basename))
    return None


class Installer(object):
    '''
    LHCb Software installer.
    This class can be used to query the remote YUM database,
    and to install packages on disk.
    It create the InstallArea files needed for the installation.
    You can create it either:

    * Passing the siteroot of the Installation, in which case the
    repositories are setup to the default LHCb ones

    * Passing a full InstallAreaConfig as the named parameter config,
    in which case all customizations are possible (by specifying the configType
    parameter). A class like LHCbConfig.py must be created in that case...
    '''

    def __init__(self, siteroot, config=None,
                 localRPMcache=None, disableYumCheck=False,
                 chained_db_list=[], nodeps=False,
                 tmp_dir=None):
        '''
        Class to install a set of packages to a specific area
        '''
        self.log = logging.getLogger(__name__)
        self._siteroot = os.path.abspath(siteroot)
        self._lcgDir = os.path.join(self._siteroot, "lcg")
        if config is None:
            from lbinstall.LHCbConfig import Config
            config = Config()
        self._config = config
        self._nodeps = nodeps
        # Creating the install area and getting the relevant info
        self.__installArea = InstallArea(self._config, self._siteroot,
                                         tmp_dir=tmp_dir)
        self._lbYumClient = self.__installArea \
                                .createYumClient(not disableYumCheck)
        self._chainedDBManger = self.__installArea.createChainedDBManager()
        self._localDB = self.__installArea.createDBManager(
            self._chainedDBManger)
        self._relocateMap = self.__installArea.getRelocateMap()
        self._tmpdir = self.__installArea.getTmpDir()
        self._localRPMcache = []
        if localRPMcache is not None:
            self._localRPMcache = localRPMcache
        for chained_db in chained_db_list:
            self._chainedDBManger.addDb(chained_db)

    # Various utilities to query the yum database
    # ############################################################################

    def getPackageListFromTuples(self, tuplesList, local=False):
        packagelist = []
        for rpmname, version, release in tuplesList:
            if local:
                packagelist.extend(self.localFindPackages(rpmname,
                                                          version,
                                                          release))
            else:
                packagelist.extend(self.remoteFindPackage(rpmname,
                                                          version,
                                                          release))
        return packagelist

    def remoteListProvides(self, nameRegexp):
        """ List provides matching in the remote repo """
        return self._lbYumClient.listProvides(nameRegexp)

    def remoteFindPackage(self, name, version=None, release=None):
        from .Model import Requires
        req = Requires(name, version, release, None, "EQ", None)
        pack = self._lbYumClient.findLatestMatchingRequire(req)

        res = [pack] if pack is not None else []
        return res

    def localFindPackages(self, name, version=None, release=None):
        return self._localDB.getPackages(match=name,
                                         vermatch=version,
                                         relmatch=release,
                                         local_only=True)

    def listDependencies(self, package):
        ''' Return the list of dependencies of a given package '''
        return self._getPackagesToInstall(package, ignoreInstalled=True)

    def remoteListPackages(self, nameRegexp=None,
                           versionRegexp=None,
                           releaseRegexp=None):
        packages = self._lbYumClient.listPackages(nameRegexp,
                                                  versionRegexp,
                                                  releaseRegexp)
        return packages

    # Queries to the local DB
    # ############################################################################3
    def localListPackages(self, nameRegexp=None,
                          versionRegexp=None,
                          releaseRegexp=None):
        packages = self._localDB.listPackages(nameRegexp,
                                              versionRegexp,
                                              releaseRegexp)
        return packages

    def getPackageListToInstall(self, packagelist,
                                nodeps=False, dry_run_update=False):
        if not packagelist:
            raise Exception("Please specify one or more packages")

        # Looking for the files to install
        rpmtoinstall = list()
        if not nodeps and not self._nodeps:
            for p in packagelist:
                rpmtoinstall_tmp = self._getPackagesToInstall(
                    p, dry_run_update=dry_run_update)
                for rpm in rpmtoinstall_tmp:
                    if rpm not in rpmtoinstall:
                        rpmtoinstall.append(rpm)
        else:
            rpmtoinstall = packagelist

        if dry_run_update:
            return rpmtoinstall
        for package in rpmtoinstall:
            local_packages = self.localFindPackages(package.name,
                                                    None,
                                                    None)
            for local_package in local_packages:
                if local_package.name == package.name:
                    if (package.version > local_package.version or
                        (package.version == local_package.version and
                         (package.release > local_package.release))):
                        raise Exception('Please use update! The script '
                                        'needs to install %s-%s-%s, but the '
                                        'package %s-%s-%s is already '
                                        'installed' % (package.name,
                                                       package.version,
                                                       package.release,
                                                       local_package.name,
                                                       local_package.version,
                                                       local_package.release))
        return rpmtoinstall

    # Installation routines
    # ############################################################################3
    def install(self, packagelist,
                justdb=False,
                overwrite=False,
                nodeps=False,
                dry_run=False,
                dry_run_update=False):
        '''
        Installation procedure, it takes a list of package objects...
        '''
        rpmtoinstall = self.getPackageListToInstall(
            packagelist, nodeps=nodeps, dry_run_update=dry_run_update)

        # Deduplicating in case some package were there twice
        # but keep the order...
        # There might be two as we take list of packages,
        # and getPackagesToInstall is called multiple
        # times...
        rpmtoinstalldeduprev = []
        for p in rpmtoinstall:
            if p not in rpmtoinstalldeduprev:
                rpmtoinstalldeduprev.append(p)

        # If dry run, just display the info
        if dry_run:
            msg = "\n\t".join([p.rpmName() for p in rpmtoinstalldeduprev])
            self.log.info(("Dry run mode, install list (%s packages):\n\t "
                           " %s") % (len(rpmtoinstalldeduprev), msg))
            return


        # Now downloading
        self.log.warning("%s RPM files to install" % len(rpmtoinstalldeduprev))
        filestoinstall = []
        for package in rpmtoinstalldeduprev:
            localcopy = self._findFileLocally(package)
            if localcopy is not None:
                self.log.info("Using file %s from cache" % localcopy)
                filestoinstall.append((localcopy, True))
            else:
                downloadres = self._downloadfiles([package])
                filestoinstall.append((downloadres[0], False))

        # And installing...
        # We should deal with the order to avoid errors in case of problems
        # Half waythrough XXX
        filesinstalled = []
        # Taking reverse order to start with those
        # that haven't been installed yet
        for (rpm, inLocalCache) in filestoinstall[::-1]:
            self._installpackage(rpm, justdb=justdb,
                                 overwrite=overwrite,
                                 removeAfterInstall=(not inLocalCache))
            filesinstalled.append(rpm)

        if len(filesinstalled) > 0:
            self.log.info("Installed:")
            for f in filesinstalled:
                self.log.info(os.path.basename(f))
        else:
            self.log.info("Nothing Installed")

    def _findInExtrapackages(self, req, extrapackages):
        ''' Util function to check if a package scheduled
        to be installed already fulfills a given requirement '''
        for extrap in extrapackages:
            if extrap.fulfills(req):
                return extrap
        return None

    def _getPackagesToRemove(self, p,
                             extrapackages=None,
                             extrainfo=None,
                             dry_run_update=False):
        '''
        Proper single package installation method
        '''
        # Setting up data if needed
        if extrapackages is None:
            extrapackages = set()

        if extrainfo is None:
            from collections import defaultdict
            extrainfo = defaultdict(list)

        # Checking if the package is not there..
        if not self._localDB.isPackagesInstalled(p):
            self.log.warning("%s is not installed" % p.rpmName())
            return []

        # We are planning to remove p, so its provides are now a granted
        extrapackages.add(p)
        toremove = [p]
        # Iterating though the reuired packages
        for req in p.requires:
            if req.name in IGNORED_PACKAGES:
                continue
            match = self._lbYumClient.findLatestMatchingRequire(req)
            if match and match not in extrapackages:
                toremove += self._getPackagesToRemove(match,
                                                      extrapackages,
                                                      extrainfo)
        return toremove

    def _getPackagesToInstall(self, p,
                              extrapackages=None,
                              extrainfo=None,
                              ignoreInstalled=False,
                              dry_run_update=False):
        '''
        Proper single package installation method
        '''
        # Setting up data if needed
        if extrapackages is None:
            extrapackages = set()

        if extrainfo is None:
            from collections import defaultdict
            extrainfo = defaultdict(list)

        # Checking if the package is already there..
        if self._localDB.isPackagesInstalled(p) and not dry_run_update:
            self.log.warning("%s already installed" % p.rpmName())
            return []

        # We are planning to install p, so its provides are now a granted
        extrapackages.add(p)
        toinstall = [p]
        # Iterating though the reuired packages, first checking
        # what's already on the local filesystem...
        for req in p.requires:
            # First checking that one of the packages already
            # scheduled for install do not already provide the package...
            tmp = self._findInExtrapackages(req, extrapackages)
            if tmp is not None and not dry_run_update:
                self.log.debug("%s already fulfilled by %s, to be installed"
                               % (str(req), tmp.name))

            elif (not ignoreInstalled and self._localDB.provides(req) and
                  not dry_run_update):
                # Now checking whether the package isn't already installed...
                self.log.warning("%s already available on local system"
                                 % str(req))
                extrainfo["alreadyInstalled"].append(req)
            else:
                # Ok lets find in from YUM now...
                match = self._lbYumClient.findLatestMatchingRequire(req)
                if match and match not in extrapackages:
                    toinstall += self._getPackagesToInstall(match,
                                                            extrapackages,
                                                            extrainfo)
        return toinstall

    def _installpackage(self, filename, removeAfterInstall=True,
                        justdb=False, overwrite=False):
        ''' To install a RPM and record the info in the local DB'''
        # The PackageManager responsible for dealing
        # with the local package file
        pm = PackageManager(filename, self._siteroot, self._relocateMap)
        # DBManager to update local DB
        db = self._localDB
        # Metadata associated with the RPM
        dbp = pm.getPackage()
        try:
            # Now extract the file to disk
            self.log.warning("Installing %s just-db=%s" % (filename, justdb))
            if not justdb:
                pm.extract(overwrite=overwrite)
            else:
                self.log.warning(
                    "--just-db mode, will not install files from %s"
                    % filename)
            # Update the local DB
            db.addPackage(dbp, pm.getRelocatedFileMetadata())

            # Now checking
            if not justdb:
                pm.checkFileSizesOnDisk()

        except Exception as e:
            print(e)
            traceback.print_exc()
            # Rollback here
            self.log.error("Error installing files, rolling back")
            pm.removeFiles()
            db.removePackage(dbp)
            raise e

        if not justdb:
            try:
                # Running the post install
                self._runPostInstall(pm, dbp)
            except Exception as e:
                print(e)
                traceback.print_exc()
                self.log.error("Error running post install for %s" % filename)
        else:
            self.log.warning("--just-db mode, will not attempt to run "
                             "post-install for %s"
                             % filename)

        # Now cleanup if install was successfull
        if removeAfterInstall:
            self.log.debug("Install of %s succesful, removing RPM"
                           % filename)
            # Checking the location, do not remove files that are in a
            # local cache...
            willremove = True
            for cachedir in self._localRPMcache:
                if abspath(filename).startswith(abspath(cachedir)):
                    self.log.debug("File %s in local cache, will not remove"
                                   % filename)
                    willremove = False
            if willremove:
                self.log.warning("Removing %s" % filename)
                os.unlink(filename)

    def _runPostInstall(self, packageManager, dbPackage):
        ''' Runs the post install script for a given
        package '''

        # First checking whether we have a script to run
        piscriptcontent = packageManager.getPostInstallScript()
        if not piscriptcontent:
            return

        # Opensing the tempfile and running it
        db = self._localDB
        db.setPostInstallRun(dbPackage, "N")

        # Setting the RPM_INSTALL_PREFIX expected by the scripts
        newenv = dict(os.environ)
        prefix = packageManager.getInstallPrefix()
        if prefix is not None:
            self.log.warning("Setting RPM_INSTALL_PREFIX to %s" % prefix)
            newenv["RPM_INSTALL_PREFIX"] = prefix

        import tempfile
        import subprocess
        self.log.info("Running post-install scripts for %s"
                      % packageManager.getFullName())
        with tempfile.NamedTemporaryFile(prefix="lbpostinst",
                                         delete=False) as piscript:
            try:
                data = bytes(piscriptcontent, 'utf-8')
            except:
                data = bytes(piscriptcontent)
            piscript.write(data)
            piscript.flush()
            shellpath = "/bin/sh"
            bashpath = "/bin/bash"
            if os.path.exists(bashpath):
                shellpath = bashpath

            rc = subprocess.check_call([shellpath, piscript.name],
                                       stdout=sys.stdout,
                                       stderr=sys.stderr,
                                       env=newenv)
            if rc == 0:
                db.setPostInstallRun(dbPackage, "Y")
            else:
                db.setPostInstallRun(dbPackage, "E")

    def addDirToRPMCache(self, cachedir):
        ''' Add a directory to the list of dirs that will be scanned
        to look for RPM files before scanning them'''
        self._localRPMcache.append(cachedir)

    def _findFileLocally(self, package):
        ''' Look for RPM  in the local cache directory '''
        for cachedir in self._localRPMcache:
            # Try to look for file on local disk
            self.log.debug("Looking for %s in %s"
                           % (package.rpmFileName(), cachedir))
            localfile = findFileInDir(package.rpmFileName(), cachedir)
            if localfile is not None:
                return localfile
        return None

    def _downloadfiles(self, installlist, location=None):
        """ Downloads a list of files """

        # Default to the TMP directory...
        if location is None:
            location = self._tmpdir

        try:
            # Python 3 workaround
            import urllib.request as urllib
        except:
            import urllib

        files = []
        for pack in installlist:
            filename = pack.rpmFileName()
            full_filename = os.path.join(location, filename)
            files.append(full_filename)

            # Checking if file is there and is ok
            needs_download = True
            if os.path.exists(full_filename):
                fileisok = self._checkRpmFile(full_filename)
                # fileisok could be None, but in that case we could
                # not check so download again
                if fileisok or fileisok is None:
                    needs_download = False

            # Now doing the download
            if not needs_download:
                self.log.debug("%s already exists, will not download"
                               % filename)
            else:
                while True:
                    self.log.info("Downloading %s to %s" % (pack.url(),
                                                            full_filename))
                    urllib.urlretrieve(pack.url(), full_filename)
                    fileisok = self._checkRpmFile(full_filename)
                    if fileisok or fileisok is None:
                        # In this case we couldn't check so we will
                        # install the file as it is...
                        break
        return files

    def _checkRpmFile(self, full_filename):
        """ Check a specific RPM file """
        return sanitycheckrpmfile(full_filename)

    # Package removal
    # ############################################################################3
    def remove(self, removelist, justdb=False, nodeps=False, force=False,
               dry_run=False):
        '''
        Remove packages from the system
        '''
        if not force:
            for p in removelist:
                required_by = self._localDB \
                                  .findPackagesRequiringPackage(p.name,
                                                                p.version,
                                                                p.release,
                                                                True)
                for _, r in required_by:
                    for req in r:
                        if req not in removelist:
                            raise Exception(("Package %s is required "
                                             " by %s. Please use "
                                             "--force" %
                                             (p.name, req.name)))
        if dry_run:
            msg = "\n\t".join([p.rpmName() for p in removelist])
            self.log.info(("Dry run mode, %s packages to remove:\n\t"
                           " %s") % (len(removelist), msg))
            return

        # Deduplicating in case some package were there twice
        # but keep the order...
        # There might be two as we take list of packages,
        # and getPackagesToInstall is called multiple
        # times...
        rpmtoremovededuprev = []
        for p in removelist:
            if p not in rpmtoremovededuprev:
                rpmtoremovededuprev.append(p)
        self.log.warning("%s RPM files to remove" % len(rpmtoremovededuprev))
        toRemoveDBPacakges = set()
        for p in rpmtoremovededuprev:
            dbPackage = list(self._localDB.getDBPackages(match=p.name,
                                                         vermatch=p.version,
                                                         relmatch=p.release,
                                                         local_only=True))
            toRemoveDBPacakges.update(dbPackage)
        for p in toRemoveDBPacakges:
            self._removeOne(p, force=force, justdb=justdb)

    def _removeOne(self, package, force=False, justdb=False):
        '''
        Remove one package from DB and disk
        '''
        self.log.warning("Removing %s" % package.name)

        filemetadata = self._localDB.loadFMData(package.rpmName())
        if not justdb:
            # Doing the files first
            for l in filemetadata:
                file_path = "%s%s" % (self._siteroot, '%s' % l[0])
                if not os.path.isdir(file_path):
                    self.log.debug("Removing file %s" % file_path)
                    try:
                        os.unlink(file_path)
                    except:
                        pass  # ignore error
            # Doing the files first
            for l in filemetadata[::-1]:
                file_path = "%s%s" % (self._siteroot, '%s' % l[0])
                if os.path.isdir(file_path):
                    self.log.debug("Removing dir %s" % file_path)
                    if os.path.islink(file_path):
                        os.unlink(file_path)
                    else:
                        shutil.rmtree(file_path)
        else:
            self.log.info("Running in just database mode."
                          "The files are not deleted")
        # Now removing the package metadata
        self._localDB.removePackage(package.toDmPackage())
