from ispmanccp.tests import *

class TestMailController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='mail'))
        # Test response...