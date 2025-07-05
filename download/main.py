import os
from download import http, logger, config
from ong_utils import get_cookies, cookies2header
from bs4 import BeautifulSoup


passwd = config("password")
url = config("url", "https://blogs.campamentosmasterchef.com/madrid-1-2-2022/")


def get_last_name_url(url) -> str:
    """Gets the last name of an url. It will be the last part after / if not empty, otherwise the previous one"""
    return url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]


def main(force_download=False, subdir_name="images"):
    """
    Downloads images of the masterchef camp to the "images" subdirectory of the the current file
    :param subdir_name: subdirectory of the current directory where files will be saved
    :param force_download: True to download information again even if files already exist
    :return: None
    """
    dest_dir = os.path.join(os.path.dirname(__file__), subdir_name)
    os.makedirs(dest_dir, exist_ok=True)
    camp_name = get_last_name_url(url)
    # First request: get page, find submit form and extract URL from it
    first_req = http.request("get", url)
    first_req.raise_for_status()
    first_req_soup = BeautifulSoup(first_req, "html.parser")
    url_post = first_req_soup.body.find("form").attrs['action']
    # Next: do login and get cookie
    logger.debug(f"Logging in {url_post}")
    req = http.request("post", url_post, data={"post_password": passwd, "Submit": "Enter", "redirect_to": url})
    # req_bad = http.request("post", url_post, fields={"post_password": passwd + "hola", "submit": "Enter"})
    if req.status_code >= 400:
        logger.error(f"Error connecting to {url_post}")
        return
    # Read article list
    logger.info(f"Reading article list for {camp_name}")
    req_article_list = http.request("get", url)
    soup_article_list = BeautifulSoup(req_article_list, 'html.parser')
    # Iterate in article list to navigate to each
    for article in soup_article_list.find("article").findAll("a", class_="title"):
        href = article.attrs['href']
        article_name = href.split("/")[-2]
        logger.info(f"Reading article: {article_name}")
        req_article = http.request("get", href)
        img_soup = BeautifulSoup(req_article, "html.parser")
        # Get images of the article and download everyone
        article_text = img_soup.find("main").find(class_="entry-content").text.strip()
        for img in img_soup.find("main").find_all("img"):
            src = img.attrs['src']
            src_set = [s.split(" ") for s in img.attrs['srcset'].split(", ")]
            src_set = [[src, ""]]  # Use just the img shown in src
            for img_url, img_size in src_set:
                img_dir = os.path.join(dest_dir, camp_name, img_size, article_name)
                os.makedirs(img_dir, exist_ok=True)
                img_name = img_url.split("/")[-1]
                img_filename = os.path.join(img_dir, img_name)
                if not os.path.isfile(img_filename) or force_download:
                    req_img = http.request("get", img_url)
                    img_name = img_url.split("/")[-1]
                    # Save image
                    logger.info(f"processing {img_url} to {img_filename}")
                    with open(img_filename, "wb") as f:
                        f.write(req_img.content)
                else:
                    logger.info(f"Skipping {img_name}: already downloaded")
            # save description (if not previously saved)
            description_filename = os.path.join(img_dir, article_name + ".txt")
            if not os.path.isfile(description_filename) or force_download:
                with open(description_filename, "w") as fd:
                    fd.write(article_text)


if __name__ == '__main__':
    main()
    pass