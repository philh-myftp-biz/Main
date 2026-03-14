from .Path import scanner

for p in scanner():

    print()
    print(f'{p.local=}')
    print(f'{p.remote=}')
    print(f'{p.is_synced=}')
    
    if not p.is_synced:
        p.sync()
