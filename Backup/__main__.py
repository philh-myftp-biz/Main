from philh_myftp_biz.terminal import Log
from . import Scan, PathPair

scanner = Scan()

while True:

    try:

        path = next(scanner)
        
        pp = PathPair(path)

        if path.is_dir:
            continue
                
        elif not pp.remote.exists:

            pp.local.delete()

        elif (not pp.local.exists) or (pp.local.size != pp.remote.size):

            pp.remote.download(pp.local)

        else:
            print(pp)

    except ConnectionAbortedError:
        Log.WARN('', exc_info=True)
