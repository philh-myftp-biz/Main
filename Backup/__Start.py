

from .Path import Scanner
from philh_myftp_biz.terminal import cls

for p in Scanner.local():

    if not p.remote.exists:

        p.local.delete()

    else:
        print(p)

    

cls()

for p in Scanner.remote():

    if (not p.local.exists) or (p.local.size != p.remote.size):

        p.remote.download(p.local)

    else:
        print(p)