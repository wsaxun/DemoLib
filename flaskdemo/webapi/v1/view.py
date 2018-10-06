import json
from flask import request
from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy

from common.conf import get_amqp_conf
from common.log import log as logging

LOG = logging.getLogger(__name__)


def rpc_request(action, params=None, task_id=None):
    amqp = get_amqp_conf()
    try:
        with ClusterRpcProxy(amqp) as rpc:
            if action == 'test':
                task_id = rpc.task_service.fibonacci()
                LOG.info('Test get request started.')

            if action == 'get_result':
                result = rpc.task_service.get_result(task_id)
                LOG.info('Get task result, result is %s' % result)
                return json.dumps({'result': result})

            if action == 'add_policy':
                task_id = rpc.task_service.add_policy(params)
                LOG.info('Policy post request started.')

            if action == 'delete_policy':
                task_id = rpc.task_service.delete_policy(params)
                LOG.info('Policy delete request started.')

    except Exception as e:
        LOG.error(str(e))
    return json.dumps({'task_id': task_id})


class Result(MethodView):
    def get(self, task_id):
        """
        Get task result
        ---
        tags:
          - Result
        parameters:
          - in: path
            name: task_id
            type: string
            required: true
        responses:
          200:
            description: task result.
            example: {'result': result}
        """

        action = 'get_result'
        return rpc_request(action, task_id=task_id)


class Index(MethodView):
    def get(self):
        """
        Only test
        ---
        tags:
          - Test
        responses:
          200:
            description: Only test.
            example: {'task_id': task_id}
        """

        action = 'test'
        return rpc_request(action)


class Policy(MethodView):

    def post(self):
        """
        Add policy
        ---
        tags:
          - Policy
        parameters:
          - in: body
            name: params
            type: string
            required:
              - task_name
              - payload
            schema:
              id: add_policy
              type: object
              properties:
                tenent_id:
                  type: string
                  default: 10000
                  description: The task`s params
        responses:
          200:
            description: The task`s id
            example: {"task_id": "c67f957adbae41fc98bc5dd8cb8e1a6c"}
        """
        params = request.json

        action = 'add_policy'
        return rpc_request(action, params=params)

    def delete(self):
        """
        Delete policy
        ---
        tags:
          - Policy
        parameters:
          - in: body
            name: params
            type: string
            required:
              - task_name
              - payload
            schema:
              id: add_policy
              type: object
              properties:
                tenent_id:
                  type: string
                  default: 10000
                  description: The task`s params
        responses:
          200:
            description: The task`s id
            example: {"task_id": "c67f957adbae41fc98bc5dd8cb8e1a6c"}
        """
        params = request.json

        action = 'delete_policy'
        return rpc_request(action, params=params)
