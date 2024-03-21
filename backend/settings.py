import os
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", '127.0.0.1')
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "redis_pass")

PARSER_DIR = "parsers"
AVERON_SITE_URL = "https://averon-td.ru/"
PROBAHILY_SITE_URL = "https://xn--80abwmlfh7b4c.xn--p1ai/"

CACHE_TIME_LIMIT = os.getenv("CACHE_TIME_LIMIT", 60)

API_URL = os.getenv("API_URL", '127.0.0.1')
