
class TestView(object):
    def test_index(self,client,index_data):
        client.index = index_data
        response = client.get('/')
        assert response.status_code == 200
        # assert response.data == b'{"msg":"test info."}\n'
        assert response.data == index_data

