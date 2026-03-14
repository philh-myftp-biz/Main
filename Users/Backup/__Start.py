from . import get_paths

for src, dst in get_paths():

    print()
    print(f'{src=}')
    print(f'{dst=}')
    
    if (not dst.exists) or (src.size != dst.size):

        src.download(dst)
