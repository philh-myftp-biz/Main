from philh_myftp_biz.json import Weights as _Weights
from philh_myftp_biz.web.torrent import NameParser
from typing import Protocol, runtime_checkable
from philh_myftp_biz.text import similarity

@runtime_checkable
class HasName(Protocol):
    name: str

class Weights(_Weights):

    def __call__(self, t:HasName) -> bool:
        
        np = NameParser(t.name)

        return super().__call__(
            TITLE = np.title,
            SEASON = np.season,
            YEAR = np.year,
            EPISODE = np.episode,
        )

    def TITLE(self,
        sample: str | None,
        control: list[str|None]
    ) -> bool:
        return any(similarity(sample, c)>.65 for c in control)

    def SEASON(self,
        sample: list[int], 
        control: int
    ) -> bool:
        return (control in sample)
        
    def YEAR(self,
        sample: list[int], 
        control: int
    ) -> bool:
        return (len(sample) == 0) or (control in sample)

    def EPISODE(self,
        sample: list[int], 
        control: int | None
    ) -> bool:
        if len(sample) > 0:
            return control == sample[0]
        else:
            return control is None

