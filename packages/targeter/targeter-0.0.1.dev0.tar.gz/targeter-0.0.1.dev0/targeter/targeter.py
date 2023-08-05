import re
import os
from os.path import join, relpath, dirname, sep, isfile, basename
import glob
from pprint import pprint as pp

def acquire(rootpath, pattern, depth=1, verbose=False):
    """Find all files under rootpath that match pattern down to a certain
    max depth.

    Args:
        rootpath (string): Directory to acquire in.
        pattern (string): The returned files must match this regular
                          regular expression. This will be matched against
                          the files entire path, not just its basename.
        depth (int): Number of tree levels below rootpath to search in. 
                     The lowest allowed value is 1, meaning only search 
                     rootpath and not any of the directories therewithin.
                     Lower than 1 will raise.
        verbose (bool): If True, print a list of directories that were searched
                        and also a list of the matching files

    Returns:
        A list of the acquired files.

    """
    if depth < 1:
        return []

    all_paths = _walk(rootpath, depth, verbose)
    all_names = [basename(x) for x in all_paths]
    if verbose:
        pp(all_names)
    return [x for x in all_paths if re.match(pattern, x)]


def _walk(rootpath, depth, verbose=False):
    """Return all files in rootpath and it's children down to a level
    specified by depth.
    """
    owd = os.getcwd()
    os.chdir(rootpath)
    files = []
    for i in range(depth):
        names = glob.glob(sep.join('*' * (i + 1)))
        fs = [join(rootpath, x) for x in names]
        dirs = _dirs_searched(fs, rootpath)
        files += [x for x in fs if isfile(x)]
        if verbose:
            print_status(i, dirs)
    os.chdir(owd)
    return files


def _dirs_searched(fs, rootpath):
    try:
        dirs = set([relpath(dirname(x), rootpath) for x in fs])
    except AttributeError:
        dirs = set([dirname(x) for x in fs])
    return dirs


def _print_status(i, dirs):
    print('Targeter at depth {}, looking in:'.format(i))
    pp(dirs)
