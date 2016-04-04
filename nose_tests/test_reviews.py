from nose_tests.constants import BEST_IN_THE_WORLD, CHRIS
from nose_tests.nd_test_case import NDTestCase
from flaskapp import app


class ReviewAPITest(NDTestCase):

    def setUp(self):
        super(ReviewAPITest, self).setUp()

    def test_get(self):
        get_uri = '{}/reviews/{}'.format(app.config['BASE_URL'], BEST_IN_THE_WORLD)
        response = self.json_get(get_uri)

        reponse_dict = self.dict_from_response(response)

        self.assertEqual(response.status_code, app.config['OK'])

    def test_get_all(self):
        get_uri = '{}/restrooms/{}/reviews/'.format(app.config['BASE_URL'], CHRIS)
        response = self.json_get(get_uri)

        reponse_dict = self.dict_from_response(response)

        self.assertEqual(response.status_code, app.config['OK'])

        get_uri = '{}/restrooms/{}/reviews'.format(app.config['BASE_URL'], CHRIS)
        response = self.json_get(get_uri)

        reponse_dict_cmp = self.dict_from_response(response)

        self.assertEqual(response.status_code, app.config['OK'])

        self.assertEqual(reponse_dict, reponse_dict_cmp)

    # def test_post_restroom(self):
    #     get_uri = '{}/reviews?page=1&order=asc&pagesize=12'.format(app.config['BASE_URL'])
    #     response = self.json_get(get_uri)
    #
    #     reponse_dict = self.dict_from_response(response)
    #
    #     self.assertEqual(response.status_code, app.config['OK'])
    #
    #     self.assertEqual(reponse_dict[0]['bio'], 'Rapper')