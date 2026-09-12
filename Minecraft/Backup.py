from philh_myftp_biz.terminal import Log
from philh_myftp_biz.time import now
from . import rWorlds

Log.INFO('Tracking Files')
rWorlds.refresh()

if rWorlds.changes == 0:
    Log.WARN('No Modified Files Found')
    
else:
    Log.INFO(f'{rWorlds.changes} Modified Files Found')

    Log.INFO('Committing')
    new_commit = rWorlds.commit(
        message = f"Automatic Backup",
        skip_hooks = True,
    )

    TAG = now().ISO.split('.')[0].replace('T', '_').replace(':', '-')

    Log.INFO(f'Applying Tag: {TAG}')
    rWorlds.new_tag(TAG, new_commit)

    Log.INFO(f'Pushing to Remote')
    rWorlds.REMOTE.push()

