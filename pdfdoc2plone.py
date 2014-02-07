#~/usr/bin/python

import pdb
import fnmatch
import os, sys
from xmlrpclib import ServerProxy
from xmlrpclib import Binary

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def main():
    contents = []
    plone_site_url = 'http://admin:admin@freethefuture.com:8080/Plone2'
    plone_site = ServerProxy(plone_site_url, allow_none=True)
    matches = []
    dirmatches = []
    for root, dirnames, filenames in os.walk('/home/brian/uploadedfiles/'):
        for filename in filenames:
            if filename.endswith(('.pdf', 'PDF', '.doc', '.DOC')):
                matches.append(os.path.join(root, filename))
          
    with open('francislog.txt', 'w') as f:
        for yo in matches:
            if yo.split('.')[-1] not in ('pdf', 'PDF', '.doc', '.DOC'):
                continue
            g = open(yo, 'r')
            binary_data = Binary(g.read())
            g.close()
#            oldobject = {'image': binary_data}
            yoyo = os.path.basename(yo)
            yoyoyo = os.path.dirname(yo)
            stuff = splitall(yoyoyo)
            oldobject = {'file': binary_data, 'title': yoyo}
            for x in stuff:
                y = stuff.index(x) + 1
                relpath = '/'.join(stuff[3:y])
                if relpath:
                    try:
                        plone_site.get_object([relpath])
                    except:
                        plone_site.post_object({relpath: [{'title': x}, 'Folder']})
                        f.write('Created folder ' + relpath + '\n')
                    else:
                        f.write('Skipped folder ' + relpath + '\n')
            newpath = os.path.join(relpath, yoyo)
            pdb.set_trace()
            try:
                plone_site.post_object({newpath: [oldobject, 'File']})
            except:
                f.write('Removed file ' + newpath + '\n')
            else:
                f.write('Added file ' + newpath + '\n')

if __name__ == "__main__":
    main() 
