from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.file import ZIP, temp
from philh_myftp_biz.web import download
from tqdm import tqdm

ffmpeg = temp('ffmpeg', 'exe', '0')
ffprobe = temp('ffprobe', 'exe', '0')

#
if (not ffmpeg.exists()) or (not ffprobe.exists()):

    #
    zipfile = temp('ffmpeg', 'zip')

    #
    download(
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip',
        path = zipfile
    )

    #
    zip = ZIP(zipfile)

    #
    zip.extractFile(
        file = next(zip.search('ffmpeg.exe')),
        path = ffmpeg
    )

    #
    zip.extractFile(
        file = next(zip.search('ffprobe.exe')),
        path = ffprobe
    )

def encode(args:list[str]):

    try:

        cmd = [
            str(ffmpeg),
            '-hwaccel', 'auto',
            *args
        ]

        pbar = tqdm(
            total = 100,
            position = 1,
            desc = "Encoding"
        )
        
        ff = FfmpegProgress(cmd)

        for progress in ff.run_command_with_progress():
            pbar.update(progress - pbar.n)

    except RuntimeError as e:

        stderr: str = e.args[0]

        raise RuntimeError(stderr.strip()) from None
