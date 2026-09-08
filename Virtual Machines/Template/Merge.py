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

parts: list[Path] = []

for sibl in file.siblings:

    if sibl.seg().startswith(file.seg()):

        parts += [sibl]

parts = sorted(
    parts,
    key = lambda p: int(p.ext.split('_')[1])
)

print(f'{parts=}')

exit()

#===============================

with file.open('wb') as merged_file:

    for part in parts:
    
        with part.open('rb') as f:
    
            merged_file.write(f.read())
