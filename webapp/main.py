# builtin
import os

# external
import flask

# local
import utils


app = flask.Flask(__name__)


@app.before_first_request
def setup_app():
    utils.setup(app)


@app.route('/')
def index():
    return flask.render_template(
        'base.jade', post=utils.readfile('index.html'))


@app.route('/<path>')
def dynamic(path):
    try:
        filename = utils.get_dynamic_path(path)
        return flask.render_template(
            'base.jade', post=utils.readfile(filename))
    except ValueError:
        print('no files with path {}'.format(path))
        return flask.abort(404)


@app.route('/static/<path:filename>')
def base_static(filename): return flask.send_from_directory(
    utils.DIR + '/static/', filename)


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template(
        'base.jade', post=utils.readfile('404.html')), 404


if __name__ == '__main__':
    os.environ['DEBUG'] = 'True'
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT', 5000),
        debug=True,
        use_reloader=True,
    )
