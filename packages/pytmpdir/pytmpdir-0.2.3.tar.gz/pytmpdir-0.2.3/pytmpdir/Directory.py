# Created by Synerty Pty Ltd
# Copyright (C) 2013-2017 Synerty Pty Ltd (Australia)
#
# This software is open source, the MIT license applies.
#
# Website : http://www.synerty.com
# Support : support@synerty.com

import os
import shutil
import tempfile
import weakref
from platform import system
from subprocess import check_output


class DirSettings:
    """ Directory Settings

    User configuration settings.
    """

    tmpDirPath = '/tmp'
    defaultDirChmod = 0o700


__author__ = 'synerty'

textChars = bytearray([7, 8, 9, 10, 12, 13, 27]) + bytearray(list(range(0x20,
                                                                        0x100)))

isWindows = system() is "Windows"


def is_binary_string(data):
    """ Is Binary String

    Determines if the input variable contains specific ASCII
    characters.

    @param data: Input variable being checked if it's a string.
    @return: True if variable is string.
    """

    return bool(data.translate(None, textChars))


class FileDisappearedError(Exception):
    """ File Disappeared Error

    Raise Exception if file does not exist .
    """

    pass


class FileClobberError(Exception):
    """ File Clobber Error

    Raise Exception if path does not exist.
    """

    pass


class Directory(object):
    """ Directory

    Functions as a directory object to extract, archive and pass around code.
    Auto deletes when the directory falls out of scope.
    """

    def __init__(self, initWithDir: bool = None,
                 autoDelete: bool = True,
                 inDir: str = None):
        """ Directory Initialise

        Creates a temporary directory if the directory doesn't exist.

        @param initWithDir: Force creation of temporary directory.
        @param autoDelete: Remove temporary files and folders.  Default as True.
        @param inDir: Current directory.
        @type initWithDir: Boolean
        @type autoDelete: Boolean
        @type inDir: String
        """

        self._files = {}
        self._autoDelete = autoDelete

        if initWithDir:
            self._path = initWithDir
            self.scan()

        else:
            if (os.path.isdir(inDir if inDir else
                              DirSettings.tmpDirPath) is False):
                os.mkdir(inDir if inDir else DirSettings.tmpDirPath)
            self._path = tempfile.mkdtemp(dir=(inDir if inDir else
                                               DirSettings.tmpDirPath))

        closurePath = self._path

        def cleanup(me):
            """ Cleanup

            Recursively delete a directory tree of the created path.
            """

            if autoDelete:
                shutil.rmtree(closurePath)

        self.__cleanupRef = weakref.ref(self, cleanup)

    @property
    def path(self) -> str:
        """ Path

        :return The absolute path of this directory
        """
        return self._path

    @property
    def delete(self) -> bool:
        """ Delete

        :return True if this directory will delete it's self when it falls out of scope.
        """
        return self._autoDelete

    @property
    def files(self) -> ['File']:
        """ Files

        @return: A list of the Directory.File objects.
        """

        return list(self._files.values())

    @property
    def pathNames(self) -> [str]:
        """ Path Names

        @return: A list of path + name of each file, relative to the root
        directory.
        """

        return [f.pathName for f in list(self._files.values())]

    @property
    def paths(self) -> [str]:
        """ Paths

        @return: A list of the paths, effectively a list of relative
        directory names.
        """

        return set([f.path for f in list(self._files.values())])

    def getFile(self, path: str = '', name: str = None,
                pathName: str = None) -> 'File':
        """ Get File

        Get File name corresponding to a path name.

        @param path: File path.  Default as empty string.
        @param name: File name to be used if passed.
        @param pathName: Joined file name and path to be used if passed.
        @type path: String
        @type name: String
        @type pathName: String
        @return: Specific file from dictionary.
        """

        assert (name or pathName)
        pathName = (pathName if pathName else os.path.join(path, name))
        return self._files.get(pathName)

    def createFile(self, path: str = '', name: str = None,
                   pathName: str = None) -> 'File':
        """ Create File

        Creates a new file and updates file dictionary.

        @param path: File path.  Defaults as empty string.
        @param name: File name to be used if passed.
        @param pathName: Joined file name and path to be used if passed.
        @type path: String
        @type name: String
        @type pathName: String
        @return: Created file.
        """

        file = File(self, path=path, name=name, pathName=pathName)
        self._files[file.pathName] = file
        return file

    def createTempFile(self, suffix=None, prefix=None, secure=True) -> 'File':
        """ Create File

        Creates a new file within the directory with a temporary file like name.

        @return: Created file.
        """
        if not secure:
            raise NotImplementedError("We only support secure files at this point")

        # tempfile.mkstemp(suffix=None, prefix=None, dir=None, text=False)

        newFileNum, newFileRealPath = tempfile.mkstemp(
            suffix=suffix, prefix=prefix, dir=self._path)
        os.close(newFileNum)

        relativePath = os.path.relpath(newFileRealPath, self.path)

        file = File(self, pathName=relativePath, exists=True)
        self._files[file.pathName] = file
        return file

    def createHiddenFolder(self) -> 'File':
        """ Create Hidden Folder

        Create a hidden folder.  Raise exception if auto delete isn't True.

        @return: Created folder.
        """

        if not self._autoDelete:
            raise Exception("Hidden folders can only be created within"
                            " an autoDelete directory")
        return tempfile.mkdtemp(dir=self._path, prefix=".")

    def _listFilesWin(self) -> ['File']:
        """ List Files for Windows OS

        Search and list the files and folder in the current directory for the
        Windows file system.

        @return: List of directory files and folders.
        """

        output = []
        for dirname, dirnames, filenames in os.walk(self._path):
            for subdirname in dirnames:
                output.append(os.path.join(dirname, subdirname))
            for filename in filenames:
                output.append(os.path.join(dirname, filename))
        return output

    def _listFilesPosix(self) -> ['File']:
        """ List Files for POSIX

        Search and list the files and folder in the current directory for the
        POSIX file system.

        @return: List of directory files and folders.
        """

        find = "find %s -type f" % self._path
        output = check_output(args=find.split()).strip().decode().split(
            '\n')
        return output

    def scan(self) -> ['File']:
        """ Scan

        Scan the directory for files and folders and update the file dictionary.

        @return: List of files
        """

        self._files = {}
        output = self._listFilesWin() if isWindows else self._listFilesPosix()
        output = [line for line in output if "__MACOSX" not in line]
        for pathName in output:
            if not pathName:  # Sometimes we get empty lines
                continue

            pathName = pathName[len(self._path) + 1:]
            file = File(self, pathName=pathName, exists=True)
            self._files[file.pathName] = file

        return self.files

    def clone(self, autoDelete: bool = True) -> 'Directory':
        """ Clone

        Recursively copy a directory tree.  Removes the destination
        directory as the destination directory must not already exist.

        @param autoDelete: Used to clean up files on completion.  Default as
        True.
        @type autoDelete: Boolean
        @return: The cloned directory.
        """

        d = Directory(autoDelete=autoDelete)
        os.rmdir(d._path)  # shutil doesn't like it existing
        shutil.copytree(self._path, d._path)
        d.scan()
        return d

    def _fileDeleted(self, file: 'File'):
        """ File Deleted

        Drop the file name from dictionary.

        @param file: File name.
        @type file: File
        """

        self._files.pop(file.pathName)

    def _fileMoved(self, oldPathName: str, file: 'File'):
        """ File Moved

        Drop the old file name from the dictionary and add the new file name.

        @param oldPathName: Previous dictionary path name.
        @param file: File name.
        @type oldPathName: String
        @type file: File
        """

        self._files.pop(oldPathName)
        self._files[file.pathName] = file


class _NamedTempFileReaderCloser:
    def __init__(self, fileObject):
        self._isClosed = False
        self._fileObject = fileObject

    def close(self, *args):
        if self._isClosed:
            return
        self._fileObject.close()
        self._isClosed = True


class NamedTempFileReader:
    """ Named Temp File

    This pytmpdir version of the NamedTemporaryFile keeps a strong reference to the
    C{Directory} object, meaning you can pass it around just like a NamedTemporaryFile
    and it will delete when it's done.

    ::

        dir = Directory()
        file = dir.createTempFile()

        # Write the data to the file, this closes it properly, allowing the reader to read
        with file.open(write=True) as f:
            f.write("some thing")

        namedTempReader = file.namedTempFileReader()

        # Pass namedTempReader to other code that takes a NamedTemporaryFile
        somthingElse(namedTempReader)

    """

    def __init__(self, directory: Directory, file: 'File'):
        self._directory = directory
        self._file = file
        self._fileObject = self._file.open()

        self._closer = _NamedTempFileReaderCloser(self._fileObject)
        self.__cleanupRef = weakref.ref(self, self._closer.close)

    @property
    def name(self) -> str:
        """ Delete

        :return The abolote path and file name of this file.
        """
        return self._file.realPath

    @property
    def delete(self) -> bool:
        """ Delete

        :return True if the file will be deleted when all references to the directory
                    including this objects reference, fall out of scope.
        """
        return self._directory.delete

    @delete.setter
    def delete(self, value: bool):
        raise Exception("You can not turn off auto delete for this class")

    def close(self):
        """ Close

        Closes the underlying file object
        """
        self._closer.close()

    def __enter__(self):
        self._fileObject.__enter__()
        return self

    def __exit__(self, exc, value, tb):
        result = self._fileObject.__exit__(exc, value, tb)
        self.close()
        return result

    def __iter__(self):
        for line in self._fileObject:
            yield line


class File(object):
    def __init__(self, directory: Directory, path: str = '', name: str = None,
                 pathName: str = None, exists: bool = False):
        """ File

        Test whether a path exists.  Set the access and modified time of
        path.  Change the access permissions of a file.

        @param directory: Directory instance.  Default as empty string.
        @param path: File path.
        @param name: File name to be used if passed.
        @param pathName: Joined file name and path to be used if passed.
        @param exists: Passed argument.  Default as False.
        @type directory: Directory
        @type path: String
        @type name: String
        @type pathName: String
        @type exists: Boolean
        """

        assert (isinstance(directory, Directory))
        assert (name or pathName)

        self._directory = weakref.ref(directory)

        if name:
            path = path if path else ''
            self._pathName = os.path.join(path, name)

        elif pathName:
            self._pathName = pathName

        self._pathName = self.sanitise(self._pathName)

        if not exists and os.path.exists(self.realPath):
            raise FileClobberError(self.realPath)

        if exists and not os.path.exists(self.realPath):
            raise FileDisappearedError(self.realPath)

        if not os.path.exists(self.realPath):
            with self.open(append=True):
                os.utime(self.realPath, None)
                os.chmod(self.realPath, 0o600)

    # ----- Name and Path setters
    @property
    def path(self) -> str:
        """ Path

        Determines directory name.

        @return: Path as string.
        """

        return os.path.dirname(self.pathName)

    @path.setter
    def path(self, path: str):
        """ Path Setter

        Set path with passed in variable.

        @param path: New path string.
        @type path: String
        """

        path = path if path else ''
        self.pathName = os.path.join(path, self.name)

    @property
    def name(self) -> str:
        """ Name

        Determines working directory.

        @return: Directory name as string.
        """

        return os.path.basename(self.pathName)

    @name.setter
    def name(self, name: str):
        """ Name Setter

        Set name with passed in variable.

        @param name: New name string.
        @type name: String
        """

        self.pathName = os.path.join(self.path, name)

    @property
    def pathName(self) -> str:
        """ Path Name

        Returns stored path name.

        @return: Path Name as string.
        """

        return self._pathName

    @pathName.setter
    def pathName(self, pathName: str):
        """ Path Name Setter

        Set path name with passed in variable, create new directory and move
        previous directory contents to new path name.

        @param pathName: New path name string.
        @type pathName: String
        """

        if self.pathName == pathName:
            return

        pathName = self.sanitise(pathName)
        before = self.realPath
        after = self._realPath(pathName)

        assert (not os.path.exists(after))

        newRealDir = os.path.dirname(after)
        if not os.path.exists(newRealDir):
            os.makedirs(newRealDir, DirSettings.defaultDirChmod)

        shutil.move(before, after)

        oldPathName = self._pathName
        self._pathName = pathName

        self._directory()._fileMoved(oldPathName, self)

    def open(self, append: bool = False, write: bool = False):
        """ Open

        Pass arguments and return open file.

        @param append: Open for writing, appending to the end of the file if
        it exists.  Default as False.
        @param write: Open for writing, truncating the file first.  Default
        as False.
        @type append: Boolean
        @type write: Boolean
        @return: Open file function.
        """

        flag = {(False, False): 'r',
                (True, False): 'a',
                (True, True): 'a',
                (False, True): 'w'}[(append, write)]

        realPath = self.realPath
        realDir = os.path.dirname(realPath)
        if not os.path.exists(realDir):
            os.makedirs(realDir, DirSettings.defaultDirChmod)
        return open(self.realPath, flag)

    def namedTempFileReader(self) -> NamedTempFileReader:
        """ Named Temporary File Reader

        This provides an object compatible with NamedTemporaryFile, used for reading this
        files contents. This will still delete after the object falls out of scope.

        This solves the problem on windows where a NamedTemporaryFile can not be read
        while it's being written to
        """

        # Get the weak ref
        directory = self._directory()
        assert isinstance(directory, Directory), (
            "Expected Directory, receieved %s" % directory)

        # Return the object
        return NamedTempFileReader(directory, self)

    def delete(self):
        """ Delete

        Deletes directory and drops the file name from dictionary.  File on
        file system removed on disk.
        """

        directory = self._directory()
        assert isinstance(directory, Directory)

        realPath = self.realPath
        assert (os.path.exists(realPath))
        os.remove(realPath)

        directory._fileDeleted(self)

    def remove(self):
        """ Remove

        Removes the file from the Directory object, file on file system
        remains on disk.
        """

        directory = self._directory()
        assert isinstance(directory, Directory)
        directory._fileDeleted(self)

    @property
    def size(self) -> str:
        """ Size

        Determines size of directory.

        @return: Total size, in bytes.
        """

        return os.stat(self.realPath).st_size

    @property
    def mTime(self) -> str:
        """ mTime

        Return the last modification time of a file, reported by os.stat().

        @return: Time as string.
        """

        return os.path.getmtime(self.realPath)

    @property
    def isContentText(self):
        """ Is Content Text

        Determine if the file contains text.

        @return: True if file contains text.
        """

        with self.open() as f:
            return not is_binary_string(self.open().read(40000))

    @property
    def realPath(self) -> str:
        """ Real Path

        Get path name.

        @return: Path Name as string.
        """

        return self._realPath()

    def _realPath(self, newPathName: str = None) -> str:
        """ Private Real Path

        Get path name.

        @param newPathName: variable for new path name if passed argument.
        @type newPathName: String
        @return: Path Name as string.
        """

        directory = self._directory()
        assert directory
        return os.path.join(directory.path,
                            newPathName if newPathName else self._pathName)

    def sanitise(self, pathName: str) -> str:
        """ Sanitise

        Clean unwanted characters from the pathName string.

        @param pathName: Path name variable.
        @type pathName: String
        @return: Path name as string.
        """

        assert isinstance(pathName, str)
        assert '..' not in pathName
        assert not pathName.endswith(os.sep)

        while pathName.startswith(os.sep):
            pathName = pathName[1:]

        return pathName
