from .World import Worlds

processes = [w.start() for w in Worlds]

# Wait for all subprocesses to complete
for process in processes:
    
    process.wait()
