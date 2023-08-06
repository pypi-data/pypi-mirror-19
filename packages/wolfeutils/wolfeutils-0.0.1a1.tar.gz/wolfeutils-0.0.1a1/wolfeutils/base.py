import bz2
import gzip


def openFunc(fname):
    '''Open a file with apprproiate open compression function.'''
    if fname.endswith('.gz'):
        opener = gzip.open
    elif fname.endswith('.bz2'):
        opener = bz2.decompress
    else:
        opener = open
    return opener
