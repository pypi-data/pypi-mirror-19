from .instapaper.instapaper import Instapaper
from .instapaper.instapaper import Bookmark
from jinja2 import Template
import webbrowser
import netrc
import pathlib
import json
import copy
import shutil


HOST = 'instapaper.com'
APP_KEY = '0688495ca0da4a899ad5a6103c47e919'
APP_SECRET = '88ec402343cd4eaa8bc02fd14da5bc96'

INSTAPAPER_ENGINE = Instapaper(APP_KEY, APP_SECRET)

assets_location = pathlib.Path.home().joinpath('.instapaper')
assets_location.mkdir(exist_ok=True)
bookmarks_location = assets_location.joinpath('bookmarks.json')
bookmarks_location.touch()
read_path = assets_location.joinpath('read')
token_path = assets_location.joinpath('token')
token_path.touch()


class AppException(Exception):
    pass


def path_from_package(resource_path):
    import pkg_resources
    resource_package = __name__
    return pkg_resources.resource_filename(resource_package, resource_path)


def copy_read_assets():
    resource_path = '/'.join(('read_assets',))
    path = path_from_package(resource_path)
    src_read_assets_path = pathlib.Path(path)
    try:
        shutil.copytree(str(src_read_assets_path), str(read_path))
    except FileExistsError:
        pass


def credentials_from_netrc():
    parsed_credentials = netrc.netrc().authenticators(HOST)
    if not parsed_credentials:
        raise AppException("""
Can't find credentials. Please set it in .netrc file.
For example:
```
machine instapaper.com
  login contact@email.com
  password verysecure
```
  """)
    username, __, password = parsed_credentials
    return (username, password)


def set_local_token_and_secret(token, secret):
    return token_path.write_text('\n'.join([token, secret]))


def get_local_token_and_secret():
    token_content = token_path.read_text()
    if token_content:
        return token_content.split('\n')


def login(username=None, password=None, forced=False):
    print('Logging In...')

    if not username and not password:
        username, password = credentials_from_netrc()

    if forced:
        token, secret = INSTAPAPER_ENGINE.get_token_and_secret(username, password)
        set_local_token_and_secret(token, secret)

    parsed_tokens = get_local_token_and_secret()

    if parsed_tokens:
        token, secret = parsed_tokens
    else:
        token, secret = INSTAPAPER_ENGINE.get_token_and_secret(username, password)
        set_local_token_and_secret(token, secret)

    INSTAPAPER_ENGINE.login_with_token(token, secret)


class BookmarkJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Bookmark):
            dictionary = copy.copy(obj.__dict__)
            dictionary.pop('parent')
            # dictionary.pop('_Bookmark__html')
            return dictionary

        return json.JSONEncoder.default(self, obj)


class BookmarkJSONDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        return Bookmark(INSTAPAPER_ENGINE, d)


def synced_bookmarks():
    json_content = bookmarks_location.read_text()
    return json.loads(json_content, cls=BookmarkJSONDecoder)


def read_last_synced_bookmark(should_archive=False):
    # last_bookmark = synced_bookmarks()[0]
    unreads = INSTAPAPER_ENGINE.bookmarks(limit=1)
    if unreads:
        last_bookmark = unreads[0]
        read(last_bookmark)
        if should_archive:
            last_bookmark.archive()
    else:
        print('No unread')


def article_template():
    resource_path = '/'.join(('templates', 'read_template.html'))
    path = path_from_package(resource_path)
    template_content = pathlib.Path(path).read_text()
    return Template(template_content)


def write_rendered_article(rendered_content):
    temp_rendered_html_file_path = read_path.joinpath('read.html')
    temp_rendered_html_file_path.write_text(rendered_content)
    return str(temp_rendered_html_file_path)


def read(bookmark):
    """ Render and open a bookmark on web browser
    """
    rendered_content = article_template().render(
        article=bookmark.html,
        article_title=bookmark.title,
        article_link=bookmark.url,
        article_link_text=bookmark.url,
    )
    article_file_path = write_rendered_article(rendered_content)
    webbrowser.open(article_file_path)


def download_bookmarks():
    print('Downloading bookmarks...')
    bookmarks = INSTAPAPER_ENGINE.bookmarks(limit=2)
    [bookmark.html for bookmark in bookmarks]
    save_bookmarks(bookmarks)


def save_bookmarks(bookmarks):
    bookmarks_content = json.dumps(bookmarks, cls=BookmarkJSONEncoder)
    bookmarks_location.write_text(bookmarks_content, encoding='utf-8')


def sync():
    print('Syncing...')
    download_bookmarks()


def put_back():
    """ Unarchive last archived item
    """
    print('Put back last archived item...')
    archiveds = INSTAPAPER_ENGINE.bookmarks(folder='archive', limit=1)
    if archiveds:
        last_archived = archiveds[0]
        last_archived.unarchive()


def folders():
    for folder in INSTAPAPER_ENGINE.folders():
        print(folder)


def unreads():
    for bookmark in INSTAPAPER_ENGINE.bookmarks():
        print(bookmark)


def archiveds():
    for bookmark in INSTAPAPER_ENGINE.bookmarks(folder='archive'):
        print(bookmark)
