from philh_myftp_biz.modules import Repo
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.time import now

repo = Repo('E:/Minecraft/Worlds/')

Log.INFO('Tracking Files')
repo.add(A=True)

filecount = len(repo.diff(repo.head.commit))

if filecount == 0:

    Log.WARN('No Modified Files Found')
    
else:

    Log.INFO(f'{filecount} Modified Files Found')

    Log.INFO('Committing')
    new_commit = repo.commit(
        message = f"Automatic Backup",
        skip_hooks = True,
    )

    TAG = int(now().unix)

    Log.INFO(f'Applying Tag: {TAG}')
    repo.new_tag(TAG, new_commit)

    Log.INFO(f'Pushing to Remote')
    repo.REMOTE.push()
