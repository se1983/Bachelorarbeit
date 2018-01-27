import os
import webapp
import tempfile
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, webapp.app.config['DATABASE'] = tempfile.mkstemp()
        webapp.app.testing = True
        self.app = webapp.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(webapp.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
