from tastypie.test import ResourceTestCase

class ApiValidTest(ResourceTestCase):

    def test_get_api_json(self):
        resp = self.api_client.get('/api/lyrdaq/validate_tasks/', format='json')
        self.assertValidJSONResponse(resp)