#!/usr/bin/env python
"""
 Authors: Gaurav Kumar <aavrug@gmail.com>

"""

import os
import pwd
import re
import random

def _get_username():
    return pwd.getpwuid(os.getuid()).pw_name

def _bash_file():
    return '/home/'+_get_username()+'/.bashrc'

def setpath(path, alias, delete):
    if delete:
        return _delete_confirmation(path, alias)
    message = _check(path, alias)
    if message != 'All good!':
        return message
    return _write_alias(path, alias)+'Successfully, set your path\'s short name!'

def _check(path, alias):
    if not _path_exist(path):
        return 'Sorry, no such path exist!'
    if _search_path(path):
        return 'Sorry, this path already have a short name!'
    if alias:
        if _alias_exist(alias):
            return 'Sorry, this short name already assigned to a different path!'
    return 'All good!'

def _path_exist(path):
    return os.path.exists(path)

def _search_path(path):
    f = open(_bash_file(), 'r')
    for line in f.readlines():
        if re.search("^alias[\sa-z0-9=']*"+path+"'$", line) or re.search("^alias[\sa-z0-9=']*"+_trailing_slash_path(path)+"'$", line):
            return True
    return False

def _alias_exist(alias):
    f = open(_bash_file(), 'r')
    for line in f.readlines():
        if re.findall('\\balias '+alias+'\\b', line):
            return True
    return False

def _command_exist(path, alias):
    f = open(_bash_file(), 'r')
    for line in f.readlines():
        if re.search("^alias "+alias+"='cd "+path+"'$", line) or re.search("^alias "+alias+"='cd "+_trailing_slash_path(path)+"'$", line):
            return True
    return False

def _write_alias(path, alias):
    if not alias:
        alias = _generate_alias(path)
    shortPath = _create_short_path(path, alias)
    return _write_command(shortPath, path, alias)

def _generate_alias(path):
    alias = path.rstrip('/').rsplit('/', 1)[1]+str(random.randrange(0, 999, 3))
    if _alias_exist(alias):
        _generate_alias(path)
    return alias

def _create_short_path(path, alias):
    return "\nalias "+alias+"='cd "+path+"'"

def _write_command(shortPath, path, alias):
    f = open(_bash_file(), 'a')
    f.write(shortPath)
    return 'For cd '+path+', now you can also use '+alias+'\n'

def _trailing_slash_path(path):
    if path[-1:] == '/':
        return path.rstrip('/')
    else:
        return path+'/'

def _delete_confirmation(path, alias):
    if raw_input('Are you sure you want to delete this shortpath?[y,N]: ') == 'y':
        return _delete(path, alias)
    return 'Aborted!'

def _delete(path, alias):
    if path and alias:
        if _command_exist(path, alias) and _search_path(path) and _alias_exist(alias):
            return _delete_by_path_and_alias(path, alias)
    return 'This path and shortname combination doesn\'t exist!'

def _delete_by_path_and_alias(path, alias):
    fileData = _get_file_data()
    f = open(_bash_file(), 'w')
    command = _get_command(path, alias)
    tCommand = _get_command(path, alias, True)
    for line in fileData:
        if not command in line and not tCommand in line:
            f.write(line)
    f.close()
    return 'Successfully, deleted your shortpath!'

def _get_file_data():
    f = open(_bash_file(), 'r')
    fileData = f.readlines()
    f.close()
    return fileData

def _get_command(path, alias, trail = False):
    command = "alias "+alias+"='cd "
    if trail:
        path = _trailing_slash_path(path)
    command += path+"'"

    return command