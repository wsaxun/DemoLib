from . import api_blueprint
from .view import Test, Policy, Result

api_blueprint.add_url_rule('/', view_func=Test.as_view('test'))

api_blueprint.add_url_rule('/result/<string:task_id>',
                           view_func=Result.as_view('result'), methods=['GET'])
api_blueprint.add_url_rule('/policy', view_func=Policy.as_view('policy'),
                           methods=['POST', 'DELETE'])
