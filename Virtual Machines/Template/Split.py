from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.pc import Path 
#===============================

args = ParsedArgs()

args.Arg(
    name = 'file',
    handler = Path
)

#===============================

file: Path = args['file']

with file.open('rb') as f:

    x = 0
    
    while True:
        
        chunk = f.read(2147480000)#2147483648)
        
        if not chunk:
            break

        part = file.sibling(file.seg() + f'_{x}')
        
        with part.open('wb') as chunk_file:
            chunk_file.write(chunk)
        
        x += 1
