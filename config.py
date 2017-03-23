import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

verify_token = os.environ['VERIFY_TOKEN']
page_access_token = os.environ['PAGE_ACCESS_TOKEN']
fb_url = os.environ['FB_URL']
