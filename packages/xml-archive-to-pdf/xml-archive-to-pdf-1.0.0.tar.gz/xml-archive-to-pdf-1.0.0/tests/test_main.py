import unittest
from xml_archive_to_pdf.utils import build_pdf
import os.path

from xml_archive_to_pdf.main import main


"""
Utils unit tests
"""


class MainTest(unittest.TestCase):

    def setUp(self):
        self.xml_file = "tests/data/pathfinder_1.xml"
        self.pdf_file = "tests/data/pathfinder_1.pdf"
        self.logo_file = "tests/data/logo.png"
        self.args = {
            "--input": self.xml_file,
            "--output": self.pdf_file,
            "--logo": self.logo_file
        }

    def test_main(self):
        main(args=self.args)
        self.assertTrue(os.path.exists(self.pdf_file))
        self.assertTrue(os.path.getsize(self.pdf_file) > 0)
