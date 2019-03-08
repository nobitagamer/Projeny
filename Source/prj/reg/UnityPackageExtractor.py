
import mtm.ioc.Container as Container
from mtm.log.Logger import Logger
from mtm.log.LogStreamConsole import LogStreamConsole
from mtm.util.SystemHelper import SystemHelper

import tempfile

from mtm.ioc.Inject import Inject
from mtm.ioc.Inject import InjectMany
import mtm.ioc.IocAssertions as Assertions

from mtm.util.ScriptRunner import ScriptRunner
from mtm.util.VarManager import VarManager
from mtm.config.Config import Config

import shutil

import os

from mtm.util.ProcessRunner import ProcessRunner
from mtm.util.Assert import *

from mtm.util.pathutils import *

class UnityPackageExtractor:
    _log = Inject('Logger')
    _sys = Inject('SystemHelper')

    # Returns the chosen name for the directory
    # If forcedName is given then this value is always forcedName
    def extractUnityPackage(self, packageRootDir, unityPackagePath, fallbackName, forcedName):

        fileName = os.path.basename(unityPackagePath)

        with self._log.heading("Extracting '{0}'", fileName):
            self._log.debug("Extracting unity package at path '{0}'", unityPackagePath)
            tempDir = tempfile.mkdtemp()
            self._log.info("Using temp directory '{0}'", tempDir)

            try:
                self._sys.createDirectory(os.path.join(tempDir, 'ProjectSettings'))
                self._sys.createDirectory(os.path.join(tempDir, 'Assets'))

                self._sys.executeAndWait('"[UnityExePath]" -batchmode -nographics -quit -projectPath "{0}" -importPackage "{1}"'.format(tempDir, unityPackagePath))

                with self._log.heading("Copying extracted results to output directory"):
                    assetsDir = os.path.join(tempDir, 'Assets')
                    # If the unitypackage only contains a single directory, then extract that instead
                    # To avoid ending up with PackageName/PackageName directories for everything
                    dirToCopy = self._chooseDirToCopy(assetsDir)

                    dirToCopyName = os.path.basename(dirToCopy)

                    assertThat(not self._isSpecialFolderName(dirToCopyName))

                    # If the extracted package contains a single directory, then by default use that directory as the name for the package
                    # This is nice for packages that assume some directory structure (eg. UnityTestTools)
                    # Also, some packages have titles that aren't as nice as directories.  For example, Unity Test Tools uses the directory name UnityTestTools
                    # which is a bit nicer (though adds a bit of confusion since the release name doesn't match)
                    # Note that for upgrading/downgrading, this doesn't matter because it uses the ID which is stored in the ProjenyInstall.yaml file
                    if not forcedName and (dirToCopyName.lower() != 'assets' and dirToCopyName.lower() != 'plugins'):
                        forcedName = dirToCopyName

                    if forcedName:
                        newPackageName = forcedName
                    else:
                        assertThat(fallbackName)
                        newPackageName = fallbackName

                    newPackageName = self._sys.convertToValidFileName(newPackageName)

                    assertThat(not self._isSpecialFolderName(newPackageName))

                    outDirPath = os.path.join(packageRootDir, newPackageName)
                    self._sys.copyDirectory(dirToCopy, outDirPath)

                    return newPackageName
            finally:
                self._log.debug("Deleting temporary directory", tempDir)
                shutil.rmtree(tempDir, onerror=onerror)

    def _isSpecialFolderName(self, dirName):
        dirNameLower = dirName.lower()
        return dirNameLower == 'editor' or dirNameLower == 'streamingassets'

    def _chooseDirToCopy(self, startDir):
        rootNames = [x for x in self._sys.walkDir(startDir) if not x.endswith('.meta')]

        assertThat(len(rootNames) > 0)

        if len(rootNames) > 1:
            return startDir

        rootName = rootNames[0]
        fullRootPath = os.path.join(startDir, rootName)

        if rootName.lower() == 'plugins':
            return self._chooseDirToCopy(fullRootPath)

        if rootName.lower() == 'editor':
            return startDir

        if os.path.isdir(fullRootPath):
            return fullRootPath

        return startDir

if __name__ == '__main__':
    Container.bind('Config').toSingle(Config, [])
    Container.bind('Logger').toSingle(Logger)
    Container.bind('VarManager').toSingle(VarManager, { 'UnityExePath': "C:/Program Files/Unity/Editor/Unity.exe" })
    Container.bind('LogStream').toSingle(LogStreamConsole, True, True)
    Container.bind('SystemHelper').toSingle(SystemHelper)
    Container.bind('ProcessRunner').toSingle(ProcessRunner)

    def main():
        runner = UnityPackageExtractor()

        outDir = "F:/Temp/outputtest/output"

        if os.path.exists(outDir):
            shutil.rmtree(outDir)

        runner.extractUnityPackage(packageRootDir, "C:/Users/Steve/AppData/Roaming/Unity/Asset Store-5.x/Modest Tree Media/Scripting/Zenject Dependency Injection IOC.unitypackage", outDir)

    ScriptRunner().runWrapper(main)

