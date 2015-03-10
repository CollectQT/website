# builtin
import os
# external
import scss
import flask
import flask.ext.misaka as misaka

# basic flask app
app = flask.Flask(__name__)
# markdown
misaka.Misaka(app)
# scss

with open(app.root_path+'/static/scss/main.scss', 'r') as infile:
    scss_content = infile.read()
compiled_css = scss.Scss().compile(scss_content)
with open(app.root_path+'/static/css/main.css', 'w') as outfile:
    outfile.write(compiled_css)

@app.route('/')
def index (): return flask.render_template('paths/index.html')

@app.route('/<path>')
def dynamic (path):
    # get files with that path
    from glob import glob
    files = glob(app.root_path+'/templates/paths/'+path+'*')
    # if none then 404
    if len(files)==0:
        return flask.abort(404)
    # otherwise get the shortest and pass in a relative path
    else:
        _file = min(files, key=len)
        rel_path = _file.split(app.root_path+'/templates/')[1]
        return flask.render_template(rel_path)

@app.route('/static/<path:filename>')
def base_static(filename): return flask.send_from_directory(app.root_path + '/static/', filename)

@app.errorhandler(404)
def page_not_found(e): return flask.render_template('paths/404.html'), 404
