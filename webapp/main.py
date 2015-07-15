# builtin
import os
from glob import glob
# external
import scss
import flask
import dotenv
import misaka

DIR = os.path.dirname(__file__)
dotenv.load_dotenv('.env')
app = flask.Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
scss.config.LOAD_PATHS = [
    DIR+'/static/scss/',
]

def markdown(text):
    return misaka.html(text,
        extensions=misaka.EXT_LAX_HTML_BLOCKS | misaka.EXT_AUTOLINK)

def build_markdown():
    post_files = glob(DIR+'/posts/**')
    for post_file in post_files:
        with open(post_file, 'r') as f:
            text = markdown(f.read())
        filename = post_file.split('/')[-1]
        with open(DIR+'/templates/posts/'+filename, 'w') as f:
            f.write(text)
    print('creating posts')

def monitor_markdown():
    # change monitor class
    from watchdog.events import FileSystemEventHandler
    class If_markdown_changes (FileSystemEventHandler):
        def on_modified (self, event):
            print('change in posts/ detected')
            build_markdown()
    # activate change monitor
    from watchdog.observers import Observer
    watch = Observer()
    watch.schedule(If_markdown_changes(), DIR+'/posts/')
    watch.start()
    build_markdown()

def build_css():
    with open(DIR+'/static/scss/main.scss', 'r') as infile:
        scss_content = infile.read()
    compiled_css = scss.Scss().compile(scss_content)
    with open(DIR+'/static/css/main.css', 'w') as outfile:
        outfile.write(compiled_css)
    print('created css')

def monitor_css():
    # change monitor class
    from watchdog.events import FileSystemEventHandler
    class If_scss_changes (FileSystemEventHandler):
        def on_modified (self, event):
            print('change in static/scss/ detected')
            build_css()
    # activate change monitor
    from watchdog.observers import Observer
    watch = Observer()
    watch.schedule(If_scss_changes(), DIR+'/static/scss/')
    watch.start()
    build_css()

def readfile(path):
    filepath = DIR+'/templates/posts/'+path
    try:
        with open(filepath, 'r') as f:
            text = flask.Markup(f.read())
        return text
    except IOError:
        print('no file with path {}'.format(filepath))
        return flask.abort(404)

if os.environ.get('DEBUG', False):
    monitor_css()
    monitor_markdown()
else:
    build_css()
    build_markdown()

@app.route('/')
def index ():
    return flask.render_template('base.jade', post=readfile('index.html'))

@app.route('/<path>')
def dynamic (path):
    try:
        paths = glob(DIR+'/templates/posts/'+path+'*')
        filename = min(paths, key=len).split('/')[-1]
        return flask.render_template('base.jade', post=readfile(filename))
    except ValueError:
        print('no files with path {}'.format(path))
        return flask.abort(404)

@app.route('/static/<path:filename>')
def base_static(filename): return flask.send_from_directory(DIR + '/static/', filename)

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('base.jade', post=readfile('404.html')), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
