from flask import Flask
from flasgger import Swagger

from common.conf import get_webApi_conf
from common.log import log as loggging

LOG = loggging.getLogger(__name__)

swagger = Swagger(template={'basePath': '/api'})


def create_app():
    app = Flask(__name__)

    conf = get_webApi_conf()
    app.config.update(conf)

    loggging.setup(sub_log_path='flaskDemo/webApi.log')

    swagger.init_app(app)

    from web_api.v1 import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    return app
