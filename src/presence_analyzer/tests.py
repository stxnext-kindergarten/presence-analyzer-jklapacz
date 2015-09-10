# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import os.path
import json
import datetime
import unittest

from presence_analyzer import main, utils


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)

TEST_USERS_XML = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_users.xml'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        main.app.config.update({'USERS_XML': TEST_USERS_XML})
        self.client = main.app.test_client()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith('/presence_weekday')

    def test_template_presence_weekday_page(self):
        """
        Test template: presence_weekday.html
        """
        response = self.client.get('/presence_weekday')
        self.assertEqual(response.status_code, 200)

    def test_template_mean_time__weekday_page(self):
        """
        Test template: mean_time_weekday.html
        """
        response = self.client.get('/mean_time_weekday')
        self.assertEqual(response.status_code, 200)

    def test_template_presence_start_end_page(self):
        """
        Test template: presence_start_end.html
        """
        response = self.client.get('/presence_start_end')
        self.assertEqual(response.status_code, 200)

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)
        self.assertDictEqual(
            data[0],
            {
                'user_id': '10',
                'name': 'Adam P.',
                'avatar': 'https://intranet.stxnext.pl/api/images/users/141'
            }
        )

    def test_api_presence_weekday(self):
        """
        Test presence time of given user.
        """
        resp = self.client.get('/api/v1/presence_weekday/10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['success'], True)

    def test_api_presence_weekday_no_user(self):
        """
        Testing wrong user id.
        """
        resp = self.client.get('/api/v1/presence_weekday/100')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertDictEqual(data, {'data': [], 'success': False})

    def test_api_mean_time_weekday(self):
        """
        Test mean presence time of given user.
        """
        resp = self.client.get('/api/v1/mean_time_weekday/10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['success'], True)

    def test_api_mean_time_weekday_no_user(self):
        """
        Testing wrong user id: (string).
        """
        resp = self.client.get('/api/v1/mean_time_weekday/dummy')
        self.assertEqual(resp.status_code, 404)

    def test_api_mean_time_weekday_wrong_user(self):
        """
        Testing wrong user id: (int).
        """
        resp = self.client.get('/api/v1/mean_time_weekday/100')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(data['success'], False)

    def test_api_presence_start_end_weekday(self):
        """
        Test mean start & end time of given user grouped by weekday
        """
        resp = self.client.get('/api/v1/presence_start_end/10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['success'], True)

    def test_api_presence_start_end_weekday_wrong_user(self):
        """
        Testing wrong user id: (int).
        """
        resp = self.client.get('/api/v1/presence_start_end/100')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(data['success'], False)

    def test_api_presence_start_end_weekday_no_user(self):
        """
        Testing wrong user id: (string).
        """
        resp = self.client.get('/api/v1/presence_start_end/dummy')
        self.assertEqual(resp.status_code, 404)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        data = utils.get_data()
        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(
            data[10][sample_date]['start'],
            datetime.time(9, 39, 5)
        )


def suite():
    """
    Default test suite.
    """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
