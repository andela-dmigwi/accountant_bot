''' Created by Migwi Ndung'u
    @ The Samurai Community 2017
'''
import os
from dotenv import load_dotenv, find_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(find_dotenv())

verify_token = os.environ['VERIFY_TOKEN']
page_access_token = os.environ['PAGE_ACCESS_TOKEN']
fb_url = os.environ['FB_URL']
main_url = 'http://samurai-community.herokuapp.com'
JWT_SECRET = os.environ['SECRET']
JWT_ALGORITHM = 'HS256'


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'confidential_top_secret!'
    TRAP_HTTP_EXCEPTIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/accountant.db'.format(BASEDIR)
    DEBUG = True
