from django.test import Client, override_settings

from openra.tests.routes.test_route_base import TestRouteBase


class TestRouteSearch(TestRouteBase):

    _route = '/search/mymap'

    def test_search_with_query_redirects_to_maps(self):
        """GET /search/<query> redirects to /maps/?search=<query>"""
        response = self.get()
        self.assertEqual(302, response.status_code)
        self.assertEqual('/maps/?search=mymap', response.url)

    def test_search_query_is_url_encoded(self):
        """Special characters in query are properly encoded"""
        response = self.get(route='/search/hello world')
        self.assertEqual(302, response.status_code)
        self.assertIn('search=', response.url)

    def test_get_without_query_redirects_home(self):
        """GET /search/ with no query redirects to /"""
        response = Client().get('/search/')
        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.url)

    def test_post_with_query_redirects_to_maps(self):
        """POST to /search/ with qsearch value redirects to /maps/?search=<query>"""
        response = self.post(route='/search/', data={'qsearch': 'mymap'})
        self.assertEqual(302, response.status_code)
        self.assertEqual('/maps/?search=mymap', response.url)

    def test_post_with_empty_query_redirects_home(self):
        """POST to /search/ with empty qsearch redirects to /"""
        response = self.post(route='/search/', data={'qsearch': ''})
        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.url)

    def test_post_with_whitespace_query_redirects_home(self):
        """POST to /search/ with whitespace-only qsearch redirects to /"""
        response = self.post(route='/search/', data={'qsearch': '   '})
        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.url)

    @override_settings(SITE_MAINTENANCE=True)
    def test_route_shows_maintenance_page(self):
        self.assert_is_maintenance(self.get())
