import flask

api_application = api = flask.Flask('api')
admin_application = admin = flask.Flask('admin')


@api.route('/')
def api_index():
    return '<h1>api application test.</h1>'


@admin.route('/')
def admin_index():
    return '<h1>admin application test.</h1>'
