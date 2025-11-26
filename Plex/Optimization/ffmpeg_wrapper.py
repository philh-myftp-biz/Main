from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.file import ZIP, temp
from philh_myftp_biz.web import download
from tqdm import tqdm

exefile = temp('ffmpeg', 'exe', '0')

if not exefile.exists():

    zipfile = temp('ffmpeg', 'zip')

    download(
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip',
        path = zipfile
    )

    zip = ZIP(zipfile)

    zip.extractFile(
        file = next(zip.search('ffmpeg.exe')),
        path = exefile
    )

def ffmpeg(args:list[str]):

    cmd = [str(exefile), '-hwaccel', 'cuda', *args]

    pbar = tqdm(
        total = 100,
        position = 1,
        desc = "Encoding"
    )
    
    ff = FfmpegProgress(cmd)

    for progress in ff.run_command_with_progress():
        pbar.update(progress - pbar.n)