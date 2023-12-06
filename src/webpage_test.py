from urllib.request import urlopen
import unittest


# Test Case to wrap around all tests
class webpage_open_testing(unittest.TestCase):

    # test that the project webpage opens correctly
    def test_webpage(self):
        # the url for the project webpage main page
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

    # test that the setup guide opens correctly
    def test_webpage_setup(self):
        # the url for the setup guide
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/Guide/setup'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

    # test that the setup guide opens correctly
    def test_webpage_GUI(self):
        # the url for the GUI guide
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/Guide/GUI'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

    # test that the file management guide opens correctly
    def test_webpage_fileManagement(self):
        # the url for the file management guide
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/Guide/FileManagement'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

    # test that the packet capture guide opens correctly
    def test_webpage_capture(self):
        # the url for the webpage capture guide
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/Guide/captureGuide'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

    # test that the graphing guide opens correctly
    def test_webpage_graph(self):
        # the url for the graphing guide
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/Guide/graph_guide'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

    # test that the attack analysis guide opens correctly
    def test_webpage_attackAnalysis(self):
        # the url for the attack analysis guide
        url = 'https://ubiquitous-sniffle-y217w7w.pages.github.io/#/Guide/attack_analysis'
        # try opening the url
        resp = urlopen(url)
        # the code response from opening the url
        code = resp.getcode()
        # assert that the response code was OK
        self.assertEqual(200, code)

if __name__ == '__main__':
    unittest.main()
