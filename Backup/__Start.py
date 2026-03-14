from .Path import Scanner

for p in Scanner.local():

    print(p)

    if not p.remote.exists:

        p.local.delete()

for p in Scanner.remote():

    print(p)

    if (not p.local.exists) or (p.local.size != p.remote.size):

        p.remote.download(p.local)
