from philh_myftp_biz.modules import Repo
from philh_myftp_biz.time import now

WORLDS = Repo('E:/Minecraft/Worlds')
    
new_commit = WORLDS.index.commit(
    message = f"Automatic Backup",
    skip_hooks = True
)

WORLDS.create_tag(
    now().ISO, 
    ref = new_commit
)

#WORLDS.origin.push()

print(f"Successfully created commit: {new_commit.hexsha}")
print(f"Files included in commit: {new_commit.stats.files.keys()}")
