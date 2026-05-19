from philh_myftp_biz.pc import Path

Movies = Path('E:/Plex/Media/Movies/')
Shows = Movies.sibling('/Shows/')

for f in Movies.children:

    if f.ext != 'todo':

        print(f)

        todo = Movies.child(f.name + '.todo')

        todo.open('w').close()

        f.delete()

for f in Shows.descendants:

    if f.is_file:

        print(f)

        f.delete()
