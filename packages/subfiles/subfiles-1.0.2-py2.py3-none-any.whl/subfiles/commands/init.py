"""The init command."""


from json import dumps

from .base import Base

import os
import collections

class Init(Base):
    """Initialize project."""

    def run(self):

        results = collections.defaultdict(list)
         
        rootDir = '.'

        for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                if fname.count('.') > 1:
                    ftype = '.'.join(fname.split('.')[-2:])
                    results[ftype].append(os.path.join(dirName, fname)) 

        for key, val in enumerate(results):
            print "[*.{key}]".format(**{'key':val})
            for item in results[val]:
                print item
            print "\n",
