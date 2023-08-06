from rest_framework import status

class HTTPStatusTestCaseMixin(object):

    def assertHTTP200(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def assertHTTP201(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def assertHTTP204(self, response):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assertHTTP400(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertHTTP401(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertHTTP403(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertHTTP404(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
