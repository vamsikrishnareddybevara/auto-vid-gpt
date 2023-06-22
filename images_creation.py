from icrawler.builtin import GoogleImageCrawler
import re


def generate_images(content, keywords):
    folder_name = str(re.sub(r"\?|\!|\,|\'|\"|\:|\/|\.|\\+", "", keywords)).replace(
        " ", ""
    )
    google_crawler = GoogleImageCrawler(storage={"root_dir": "./images/" + folder_name})

    filters = dict(license="commercial")
    google_crawler.crawl(
        keyword=keywords + " vertical image", max_num=2, filters=filters
    )
    print("foldername", folder_name, "keywords", keywords)
    return folder_name + ".jpg"
