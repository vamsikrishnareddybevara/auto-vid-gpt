PEXELS_API_KEY = "JjFJ2eQuHVX6KZypkccCzuPPZCiBHGQoinIUZFcRFosBU3GSm9Stl6IS"

from pexelsapi.pexels import Pexels
import requests
import re

pexel = Pexels(PEXELS_API_KEY)


def get_stock_video(content, keywords):
    search_videos = pexel.search_videos(
        query=" ".join(keywords),
        orientation="portrait",
        size="",
        color="",
        locale="",
        page=1,
        per_page=2,
    )
    if len(search_videos["videos"]):
        video_files = search_videos["videos"][0]["video_files"]

        if len(video_files):
            video_url = search_videos["videos"][0]["video_files"][0]["link"]
            print("content", content, "video_url", video_url)

            response = requests.get(video_url)

            file_name = str(
                re.sub(r"\?|\!|\,|\'|\"|\:|\/|\.|\\+", "", content) + ".mp4"
            ).replace(" ", "")
            open(
                str("./stock-videos/" + file_name),
                "wb",
            ).write(response.content)
            return file_name
        else:
            print("Empty result", video_files)
