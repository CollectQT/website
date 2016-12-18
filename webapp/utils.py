# builtin
import os
from glob import glob
from distutils.util import strtobool

# external
import scss
import flask
import misaka
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


DIR = os.path.dirname(__file__)


def setup(app):
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    scss.config.LOAD_PATHS = [
        DIR+'/static/scss/',
    ]
    if strtobool(os.environ.get('DEBUG', 'False')):
        monitor_content(build_css, '/static/scss/')
        monitor_content(build_markdown, '/posts/')
    else:
        build_css()
        build_markdown()

def monitor_content(builder, subdir):
    # change monitor class
    class ModifiedEventHandler (FileSystemEventHandler):
        def on_modified (self, event):
            print('change in {} detected'.format(subdir))
            builder()
    # activate change monitor
    watch_dir = DIR+subdir
    watch = Observer()
    watch.schedule(ModifiedEventHandler(), watch_dir)
    watch.start()
    print('Watching {}'.format(watch_dir))
    builder()

def build_markdown():
    post_files = glob(DIR+'/posts/**')
    for post_file in post_files:
        with open(post_file, 'r') as f:
            text = misaka.html(
                f.read(),
                extensions=misaka.EXT_LAX_HTML_BLOCKS | misaka.EXT_AUTOLINK,
            )
        filename = post_file.split('/')[-1]
        with open(DIR+'/templates/posts/'+filename, 'w') as f:
            f.write(text)
    print('creating posts')

def build_css():
    with open(DIR+'/static/scss/main.scss', 'r') as infile:
        scss_content = infile.read()
    compiled_css = scss.Scss().compile(scss_content)
    with open(DIR+'/static/css/main.css', 'w') as outfile:
        outfile.write(compiled_css)
    print('created css')

def readfile(path):
    filepath = DIR+'/templates/posts/'+path
    try:
        with open(filepath, 'r') as f:
            text = flask.Markup(f.read())
        return text
    except IOError:
        print('no file with path {}'.format(filepath))
        return flask.abort(404)

def get_dynamic_path(path):
    paths = glob(DIR+'/templates/posts/'+path+'*')
    filename = min(paths, key=len).split('/')[-1]
    return filename
