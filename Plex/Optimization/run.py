from __init__ import this, QueueItem, encode, args
from philh_myftp_biz.db import MimeType

#
queue: list[QueueItem] = []

#
for src in this.dir.child('/Media/').descendants():

    #
    if len(queue) == args['limit']:
        break

    #
    elif MimeType.Path(src) == 'video':

        #
        if src.ext() != 'mp4':

            queue += [QueueItem(src)]

#
for i in queue:
    
    #
    print()
    print(i.src)
    print(i.dst)

    try:

        #
        encode(i)

        #
        i.src.delete()

    #
    except Exception as e:

        i.dst.delete()

        raise e
