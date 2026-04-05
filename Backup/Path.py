from philh_myftp_biz.web.ftp import FTPPath
from philh_myftp_biz.pc import Path
from typing import Generator
from . import ftp

class PathPair:

    def __init__(self,
        path: Path|FTPPath
    ) -> None:

        if isinstance(path, Path):

            self.local = path

            _path = str(path).replace('E:/', '/E/', 1)
            
            self.remote = ftp.Path(_path)

        elif isinstance(path, FTPPath):

            self.remote = path

            _path = str(path).replace('/E/', 'E:/', 1)
            
            self.local = Path(_path)

    def __str__(self) -> str:
        return f'\nlocal={self.local}\nremote={self.remote}'

class Scanner():

    @staticmethod
    def _remote() -> Generator[FTPPath]:

        # E:/Plex/WinTV/
        yield from ftp.Path('/E/Plex/WinTV/').descendants

        # E:/Website/Root/
        for path in ftp.Path('/E/Website/Root/').descendants:
            if path.seg() != 'index.json':
                yield path

        # E:/Users/philh/
        for path in ftp.Path('/E/Users/philh/').children:
            if path.name != 'Administrator':
                yield from path.descendants

    @staticmethod
    def remote() -> Generator[PathPair]:
        
        for path in Scanner._remote():
                
            if path.is_file:
                
                yield PathPair(path)

    @staticmethod
    def local() -> Generator[PathPair]:

        # E:/Virtual Machines/
        for path in Path('E:/').children:

            if path.name == 'Backup':
                continue

            for d in path.descendants:
            
                if d.is_dir:
                    pass

                elif '/$RECYCLE.BIN/' in d.path:
                    pass

                elif '/.git/' in d.path:
                    pass

                else:
                    yield PathPair(d)
