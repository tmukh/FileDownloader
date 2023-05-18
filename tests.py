import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from main import FileDownloader

class FileDownloaderTestCase(unittest.TestCase):
    # Initialize an object from main with testing_urls.txt
    def setUp(self):
        self.main = FileDownloader("testing_urls.txt")

    # Delete everything the tests did
    def tearDown(self):
        # Clean up any files/folders created during testing
        if os.path.exists("images"):
            for file in os.listdir("images"):
                path = os.path.join("images", file)
                os.remove(path)
            os.rmdir("images")
        if os.path.exists("testing_urls.txt"):
            os.remove("testing_urls.txt")

    # Testing the URL parser, we put in an array of URLs that are expected to be read, and then we write them and test the parser
    def testUrlParser(self):
        expected_urls = ["https://i.imgur.com/AD3MbBi.jpeg", "https://i.imgur.com/plKtFBM.jpeg"]
        with open("testing_urls.txt", "w") as file:
            file.write("\n".join(expected_urls))

        actual_urls = self.main.parse_urls()
        # Test on Equality of content
        self.assertEqual(actual_urls, expected_urls)

    # Test to create the images folder (Note that TearDown removes it later on, so we go by assertTrue here)
    def test_make_folder(self):
        self.main.make_folder()

        self.assertTrue(os.path.exists("images"))
        self.assertTrue(os.path.isdir("images"))

    # Patch wget onto the mock object, and test whether or not the images download
    @patch('main.wget')
    @patch('main.FileDownloader.is_image')
    def test_download_images(self, mock_is_image, mock_wget):
        urls = ["https://i.imgur.com/AD3MbBi.jpeg", "https://i.imgur.com/plKtFBM.jpeg"]
        # Create a Mock Object
        self.main.parse_urls = MagicMock(return_value=urls)

        # Set the mock objects value of is_image to true.
        mock_is_image.return_value = True
        self.main.download_images()

        self.assertEqual(mock_wget.download.call_count, 2)
        mock_wget.download.assert_called_with(urls[1], out=os.path.join("images", "plKtFBM.jpeg"))

        # Set mock objects value of is_image to False, expect it to not download.
        mock_is_image.return_value = False
        self.main.download_images()

        # Takes the download call count into account (here 4, 2 from the previous one, 2 now)
        self.assertEqual(mock_wget.download.call_count, 4)
        self.assertEqual(mock_wget.download.call_args_list[2], ((urls[0],), {'out': os.path.join("images", "AD3MbBi.jpeg")}))
        self.assertEqual(mock_wget.download.call_args_list[3], ((urls[1],), {'out': os.path.join("images", "plKtFBM.jpeg")}))
        self.assertFalse(os.path.exists(os.path.join("images", "AD3MbBi.jpeg")))
        self.assertFalse(os.path.exists(os.path.join("images", "plKtFBM.jpeg")))

    def test_name_file(self):
        url = "https://i.imgur.com/AD3MbBi.jpeg"
        expected_file_name = "AD3MbBi.jpeg"
        actual_name = self.main.name_file(url)

        self.assertEqual(actual_name, expected_file_name)

    # Full disclosure, asked ChatGPT about patching in unittests, I did not get it.
    # The @patch decorator is used to patch objects or functions with mock objects during the execution of the decorated test method. It is part of the unittest.mock module. 
    @patch('main.mimetypes.guess_type')
    def test_is_image(self, mock_guess_type):
        mock_guess_type.return_value = ("image/jpeg", None)

        path = "images/image.jpeg"
        is_image = self.main.is_image(path)

        self.assertTrue(is_image)

        mock_guess_type.return_value = ("application/pdf", None)

        path = "images/document.pdf"
        is_image = self.main.is_image(path)

        self.assertFalse(is_image)

if __name__ == '__main__':
    unittest.main()
