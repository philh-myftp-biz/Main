from philh_myftp_biz.remotepc.ftp import FTPPath
from philh_myftp_biz.pc import Path
from typing import Generator
from . import ftp

class PathPair:

    local: Path
    remote: FTPPath

    def __init__(self,
        path: Path|FTPPath
    ) -> None:

        if isinstance(path, Path):

            self.local = Path

            _path = str(path).replace('E:/', '/E/', 1)
            
            self.remote = FTPPath(_path)

        elif isinstance(path, FTPPath):

            self.remote = path

            _path = str(path).replace('/E/', 'E:/', 1)
            
            self.local = Path(_path)

    @property
    def is_synced(self) -> bool:
        if self.local.exists:
            return (self.local.size != self.remote.size)
        else:
            return False

    def sync(self) -> None:
        self.remote.download(self.local)

def _raw_scanner() -> Generator[FTPPath]:

    # E:/Plex/WinTV/
    yield from ftp.Path('/E/Plex/WinTV/').descendants

    # E:/Website/Root/
    for path in ftp.Path('/E/Website/Root/').descendants:
        if path.seg() != 'index.json':
            yield path

    # E:/Virtual Machines/
    for path in ftp.Path('/E/Virtual Machines/').descendants:
        if path.ext() in ['vhdx', 'iso']:
            yield path

    # E:/Users/philh/
    for path in ftp.Path('/E/Users/philh/').children:
        if path.name != 'Administrator':
            yield from path.descendants

def scanner() -> Generator[PathPair]:
    
    for path in _raw_scanner():
            
        if path.is_file:
            
            yield PathPair(path)
