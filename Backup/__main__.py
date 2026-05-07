from . import Scan, PathPair

paths = []
        
for path in Scan():
        
    if not path.is_file:
        continue
        
    pp = PathPair(path)

    if pp in paths:
        continue
            
    elif not pp.remote.exists:

        paths += [pp]
        pp.local.delete()

    elif (not pp.local.exists) or (pp.local.size != pp.remote.size):

        paths += [pp]
        pp.remote.download(pp.local)

    else:
        print(pp)
