import os
import collections


def files_by_extensions(root_dir='.'):
    results = collections.defaultdict(list)
 

    for dirName, subdirList, fileList in os.walk(root_dir):
        for fname in fileList:
            if fname.count('.') > 1:
                ftype = '.'.join(fname.split('.')[-2:])
                results[ftype].append(os.path.join(dirName, fname)) 

    return results
