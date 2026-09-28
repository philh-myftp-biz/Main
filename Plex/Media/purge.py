from philh_myftp_biz.pc import Path

Media = Path(__file__).parent

for f in Media.child('/Movies/').children:
    print(f)
    f.open('w').close()

for f in Media.child('/Shows/').descendants:
    if (f.type == 'video') and (not f.in_use):
        print(f)
        f.delete()
