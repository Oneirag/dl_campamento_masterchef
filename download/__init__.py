from ong_utils import OngConfig
from fake_useragent import UserAgent
import httpx

_cfg = OngConfig("campamento_masterchef")
config = _cfg.config
logger = _cfg.logger

# ua = UserAgent(os="Mac OS X", platforms='desktop').random
ua = UserAgent().random

headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Accept-Language": "es-ES,es;q=0.9",
    # "Cache-Control": "no-cache",
    # "Connection": "keep-alive",
    # "Host": "blogs.campamentosmasterchef.com",
    # "Pragma": "no-cache",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": ua,
    # #"sec-ch-ua": "\"Not\\)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"macOS\""
}

http = httpx.Client(headers={'User-Agent': ua}, follow_redirects=True)
