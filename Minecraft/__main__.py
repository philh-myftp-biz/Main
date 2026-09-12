from philh_myftp_biz.terminal import Args
from .World import Worlds

if Args['force']:
    [w.install() for w in Worlds]

[w.start() for w in Worlds]

[w.task.wait() for w in Worlds]

