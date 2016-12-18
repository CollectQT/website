# builtin
import os
import sys
import pprint


############################################################
# setup
############################################################


# http://flask.pocoo.org/docs/0.11/testing/

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
app_dir = os.path.join(base_dir, 'webapp')
sys.path.append(base_dir)
sys.path.append(app_dir)
from webapp.main import app


def page_contains_content(route, content):
    # essentially just testing that the page builds at all
    client  = app.test_client()
    page    = client.get(route)
    data    = str(page.data)
    pprint.pprint(data)
    return content in data


############################################################
# tests
############################################################


def test_true(): assert True


def test_index():
    assert page_contains_content('/', 'CollectQT')

