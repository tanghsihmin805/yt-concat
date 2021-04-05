from .step import Step
from yt_concate.settings import VIDEOS_DIR

from pytube import YouTube


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('videos to download=', len(yt_set))
        for yt in yt_set:
            url = yt.url
            if utils.video_file_exist(yt):
                print(f'found existing video file for {url}, skipping')
                continue

            print('downloading', url)
            try:
                YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
            except:
                print(f'**** downloading {url} get error ****')
        return data
