import json
import os

AUTHOR = 'PLFM Group'
SITENAME = 'PLFM @ EPFL'
SITEURL = ''

PATH = 'content'
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['news', 'seminar']
THEME = '.'
THEME_STATIC_DIR = 'static'

TIMEZONE = 'Europe/Zurich'
DEFAULT_LANG = 'en'

# URL structure
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'

# Disable auto-generated pages we don't need
FEED_ALL_ATOM = None
CATEGORY_FEEDS_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAG_SAVE_AS = ''
TAGS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
INDEX_SAVE_AS = ''

DEFAULT_PAGINATION = 20
RELATIVE_URLS = True

# Site metadata exposed to templates
DESCRIPTION = 'Programming Language and Formal Methods group at EPFL'
GROUP_NAME = 'PLFM'
SCHOOL = 'School of Computer and Communication Sciences'
UNIVERSITY = 'EPFL'

# Load people data
import yaml
_here = os.path.dirname(os.path.abspath(__file__))
_people_path = os.path.join(_here, 'data', 'people.yaml')
if os.path.exists(_people_path):
    with open(_people_path) as f:
        PEOPLE = yaml.safe_load(f)
else:
    PEOPLE = []

# Load publications data
_pubs_path = os.path.join(_here, 'data', 'publications.json')
if os.path.exists(_pubs_path):
    with open(_pubs_path) as f:
        PUBLICATIONS = json.load(f)
else:
    PUBLICATIONS = []

# Custom Jinja2 filters
def unique_years(articles):
    return sorted({a.date.year for a in articles}, reverse=True)

JINJA_FILTERS = {
    'unique_years': unique_years,
}
