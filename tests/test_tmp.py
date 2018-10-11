# from mock import MagicMock
#
# class ProductionClass(object):
#     def method(self):
#         self.something(1,2,3)
#
#     def something(self,a,b,c):
#         pass
#
# def test_prd():
#     real = ProductionClass()
#     real.something = MagicMock()
#     real.method()
#     real.something.assert_called_once_with(1,2,3)
#
# mock = MagicMock(side_effect=[4, 5, 6])

import pytest

@pytest.fixture(params=[1,2,3])
def req(request):
    print(request.param)
    print(request)

def test_req(req):
    pass