# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------


## Description
"""
When target strings are specified, this module detects virsion information from the list.
Then it gives latest version number, version name, next version number, and etc.
"""
#-------------------------------------------------------------------------------

__author__ = 'Takatoshi Ono [tono@dfx.co.jp]'
__date__ = '24 May 2016'
__modified__ = '24 May 2016'



#-------------------------------------------------------------------------------
## Version
#-------------------------------------------------------------------------------
__version__ = "1.0"



#-------------------------------------------------------------------------------
## Import
#-------------------------------------------------------------------------------
import os
import re



class VersionObj(object):


    def __init__(self, verNum = None, verName = None, name = None):
        super(VersionObj, self).__init__()
        self._versionNum = verNum
        self._versionName = verName
        self._name = name


    @property
    def versionNum(self):
        """Getter of version number."""
        return self._versionNum

    @property
    def versionName(self):
        """Getter of version name."""
        return self._versionName

    @property
    def name(self):
        """Getter of complete string."""
        return self._name




class Versionist(object):
    """Versionist class explores given name strings and detect latest or next
    version information.
    In order to find version token from the given names, this class uses regular
    expression.
    The regrex should have version group, which has name of 'VERSION_KEY';
    the default value is 'version', but the group can be simply written with 
    version token like '<VERSION_KEY>'. So for example...
    cKTS_(?P<version>v\d{3}).ma can be cKTS_<version>.ma
    The regrex for version token automatically generated with padding and prefix
    parameters.
    """

    VERSION_KEY = "version"
    kMatchType = "match"
    kSearchType = "search"


    @classmethod
    def set_version_key(cls, version_key):
        if isinstance(version_key, str):
            cls.VERSION_KEY = version_key
        else:
            raise ValueError("Version key should be string type")


    #---------------------------------------------------------------------------
    ## Initializes a new instance of Versionist.
    ##
    ## @param targets : <list> of string names.
    ##
    ## @param name_pattern : <str> regular expression to match targets
    ##
    ## @param padding : <int> padding number of version.
    ##                This is used version token regrex replacement.
    ##
    ## @param prefix : <str> version string's prefix. This can be empty string.
    ##
    ## @param initial_number : <int> first number of version.
    ##
    ## @param match_type : <str> match type. This is used to decide regrex
    ##                    matching process.
    def __init__(self, targets,
                       name_pattern,
                       padding = 3,
                       prefix = "v",
                       initial_number = 1,
                       match_type = kMatchType  ## 'match' or 'search'
                       ):
        super(Versionist, self).__init__()
        self._targets = targets
        self._name_pattern = name_pattern
        self._padding = padding
        self._prefix = prefix
        self._initial_number = initial_number
        self._match_type = match_type


    #---------------------------------------------------------------------------
    ## Set new targets. This should be used when the instance is shared for
    ## several targets.
    ##
    ## @ param targets : <list> of target string names.
    ##
    def set_targets(self, targets):
        self._targets = targets


    #---------------------------------------------------------------------------
    ## Convert name pattern. If the given string containts version token,
    ## it is replaced at here.
    ##
    ## @return : <str> actual regular expression pattern.
    def _format_pattern(self):

        if not isinstance(self._name_pattern, (str, unicode)):
            raise RuntimeError("File pattern is not set.")

        if "(?P<%s>" % self.VERSION_KEY in self._name_pattern:
            return self._name_pattern

        elif "<%s>" % self.VERSION_KEY in self._name_pattern:
            groupKey = r"(?P<%s>%s\d{%d})" % (self.VERSION_KEY, self._prefix, self._padding)
            pat = self._name_pattern.replace("<%s>" % self.VERSION_KEY, groupKey)
            return pat

        else:
            raise VersionKeyError("Name pattern needs version key '%s'. Got %s." % (self.VERSION_KEY, self._name_pattern))


#-------------------------------------------------------------------------------
# These methods might not be useful because it needs first version at least in the targets.
#
#     def getNextVersionFilePath(self):
#         nextFile = self.getNextVersionFile()
#         if nextFile is None:
#             return None
#
#         return os.path.join(self._directory, nextFile)
#
#
#     def getNextVersionFile(self):
#         versionInfo = self._get_latest_version()
#         versionFile = versionInfo.get("fileName")
#         versionName = versionInfo.get("versionName")
#         if versionFile is None or versionName is None:
#             return None
#
#         nextName = versionFile.replace(versionName, self.get_next_version_name())
#         return nextName


    #---------------------------------------------------------------------------
    ## Returns next version name. If no version exists, returns initial version name.
    ##
    ## @return : <str> next version name
    def get_next_version_name(self):
        next_number = self.get_next_version_num()
        return "%s%s" % (self._prefix, str(next_number).zfill(self._padding))


    #---------------------------------------------------------------------------
    ## Returns next version number. If no version exists, returns initial number.
    ##
    ## @return : <int> next version number
    def get_next_version_num(self):
        latest_num = self.get_latest_version_num()
        if not isinstance(latest_num, int):
            return self._initial_number

        nextNum = latest_num + 1
        return nextNum


    #---------------------------------------------------------------------------
    ## Returns latest version name. If no version exists, returns None type.
    ##
    ## @return : <str> latest version name
    def get_latest_version_name(self):
        ver_obj = self._get_latest_version()
        return ver_obj.versionName


    #---------------------------------------------------------------------------
    ## Returns latest version number. If no version exists, returns None type.
    ##
    ## @return : <str> latest version name
    def get_latest_version_num(self):
        ver_obj = self._get_latest_version()
        return ver_obj.versionNum


    #---------------------------------------------------------------------------
    ## Returns latest version's string. If no version exists, returns None type.
    ##
    ## @return : <str> latest string
    def get_latest_name(self):
        ver_obj = self._get_latest_version()
        return ver_obj.name


    def _get_latest_version(self):

        formatted_pattern = self._format_pattern()
        compiled = re.compile(formatted_pattern)
        max_version = self._initial_number -1
        max_version_name = None
        max_name = None

        for name in self._targets:

            if self._match_type == self.kMatchType:
                matchFunc = compiled.match

            else:
                matchFunc = compiled.search

            mObj = matchFunc(name)

            if mObj is None:
                continue

            version_name = mObj.group(self.VERSION_KEY)
            version_num = int(version_name.replace(self._prefix, ""))

            if version_num > max_version:
                max_version = version_num
                max_version_name = version_name
                max_name = name

        if max_version == -1:
            return VersionObj()

        else:
            return VersionObj(verNum=max_version, verName=max_version_name, name=max_name)



class FileVersionist(Versionist):
    """FileVersionist class explores given directory and detect latest or next
    version information.
    In order to find version token from the given names, this class uses regular
    expression.
    The regrex should have version group, which has name of VERSION_KEY, but the
    group can be simply written with version token like '<VERSION_KEY>'.
    So for example...
    cKTS_(?P<version>v\d{3}).ma can be cKTS_<version>.ma
    The regrex for version token automatically generated with padding and prefix
    parameters.
    """

    kTargetFile = "file"
    kTargetDir = "dir"
    kTargetBoth = "both"

    #---------------------------------------------------------------------------
    ## Initializes a new instance of FileVersionist.
    ##
    ## @param directory : <str> Directory which containts target file names
    ##
    ## @param name_pattern : <str> regular expression to match targets
    ##
    ## @param padding : <int> padding number of version.
    ##                This is used version token regrex replacement.
    ##
    ## @param prefix : <str> version string's prefix. This can be empty string.
    ##
    ## @param initial_number : <int> first number of version.
    ##
    ## @param match_type : <str> match type. This is used to decide regrex
    ##                    matching process.
    ##
    ## @param target_type : <str> This affects how to obtain target names from
    ##                     specified directory. You can choose ""file", "dir" or "both".
    ##
    def __init__(self, directory = None,
                       name_pattern = None,
                       padding = 3,
                       prefix = "v",
                       initial_number = 1,
                       match_type = Versionist.kMatchType,
                       target_type = kTargetFile ## 'file', 'dir' or 'both'
                       ):
        super(FileVersionist, self).__init__(targets = [],
                                             name_pattern = name_pattern,
                                             padding = padding,
                                             prefix = prefix,
                                             initial_number = initial_number,
                                             match_type = match_type)
        self._directory = directory
        self._target_type = target_type

        if self._directory is not None:
            targets = self._find_targets()
            self.set_targets(targets)


    #---------------------------------------------------------------------------
    ## Set directory to search versions. Internally this methods explors the target
    ## directory and holds the strings found in there.
    ##
    ## @param directory : <str> target directory path to seach version files.
    def set_directory(self, directory):
        self._directory = directory
        targets = self._find_targets()
        self.set_targets(targets)


    #---------------------------------------------------------------------------
    ## Depending on the target type, this method finds appropriate names.
    ##
    ## @return : <str> search target names.
    def _find_targets(self):
        if self._directory is None:
            raise RuntimeError("Search target directory is not set.")

        if not os.path.exists(self._directory):
            return []

        files = os.listdir(self._directory)

        if self._target_type == "dir":
            check_func = os.path.isdir

        elif self._target_type == "file":
            check_func = os.path.isfile

        else:
            check_func = None

        targets = []

        for name in files:
            if check_func is None:
                targets.append(name)

            else:
                actualPath = os.path.join(self._directory, name)

                if check_func(actualPath):
                    targets.append(name)

        return targets


    #---------------------------------------------------------------------------
    ## returns latest version file or directory's complete path.
    ##
    ## @return : <str> latest version path.
    def get_latest_namePath(self):
        latest_name = self.get_latest_name()
        if latest_name is None:
            return None

        return os.path.join(self._directory, latest_name)


class VersionKeyError(Exception):
    pass



if __name__ == '__main__':

    pass


#-------------------------------------------------------------------------------
# END
#-------------------------------------------------------------------------------