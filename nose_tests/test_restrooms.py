from nose_tests.constants import CHRIS
from nose_tests.nd_test_case import NDTestCase
from flaskapp import app


class RestroomAPITest(NDTestCase):

    def setUp(self):
        super(RestroomAPITest, self).setUp()

    def test_get(self):
        get_uri = '{}/restrooms/{}'.format(app.config['BASE_URL'], CHRIS)
        response = self.json_get(get_uri)

        reponse_dict = self.dict_from_response(response)

        self.assertEqual(response.status_code, app.config['OK'])

    def test_get_all(self):
        get_uri = '{}/restrooms/'.format(app.config['BASE_URL'])
        response = self.json_get(get_uri)

        reponse_dict = self.dict_from_response(response)

        self.assertEqual(response.status_code, app.config['OK'])

        get_uri = '{}/restrooms'.format(app.config['BASE_URL'])
        response = self.json_get(get_uri)

        reponse_dict_cmp = self.dict_from_response(response)

        self.assertEqual(response.status_code, app.config['OK'])

        self.assertEqual(reponse_dict, reponse_dict_cmp)

    # def test_post_restroom(self):
    #     get_uri = '{}/restrooms?page=1&order=asc&pagesize=12'.format(app.config['BASE_URL'])
    #     response = self.json_get(get_uri)
    #
    #     reponse_dict = self.dict_from_response(response)
    #
    #     self.assertEqual(response.status_code, app.config['OK'])
    #
    #     self.assertEqual(reponse_dict[0]['bio'], 'Rapper')