from philh_myftp_biz.process import SubProcess
from philh_myftp_biz.terminal import Log
from __init__ import Worlds, Tasks

processes: list[SubProcess] = []

#========================================================================================================

for world in Worlds():

    #====================================================

    Log.INFO(f"Selected World: {world}")

    #==================================================
    # Clear Previously Generated Files

    for child in world.GenFiles():

        child.delete()

    #==================================================
    # COPY FILES

    # Iter through all files for this edition
    for src, dst in world.WebFiles():

        # Copy the src file to the dst path
        src.copy(dst)

    #====================================================
    # START PROCESS

    process = world.Start()
    
    Tasks[world.name()] = process._task

    processes += [process]

    #==================================================

#========================================================================================================

# Wait for all subprocesses to complete
for process in processes:
    process.wait()
