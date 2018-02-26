# -*- coding: utf-8 -*-
import os
import re
import unittest

from versionist import FileVersionist

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

class TestFileVersioninst(unittest.TestCase):


    def setUp(self):
        FileVersionist.set_version_key("version")


    def tearDown(self):
        FileVersionist.set_version_key("version")


    def test_dir_default_match(self):
        pat = "^<version>$"
        directory = os.path.join(TEST_DATA_DIR, "dir_search_test01")
        vernist = FileVersionist(directory, pat, target_type = FileVersionist.kTargetDir)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v003")


    def test_dir_diff_padding_match(self):
        pat = "^dog\_<version>$"
        directory = os.path.join(TEST_DATA_DIR, "dir_search_test02")
        vernist = FileVersionist(directory, pat, padding = 2, target_type = FileVersionist.kTargetDir)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v03")


    def test_dir_diff_prefix_match(self):
        pat = "^<version>$"
        directory = os.path.join(TEST_DATA_DIR, "dir_search_test03")
        vernist = FileVersionist(directory, pat, prefix = "A", padding = 4, target_type = FileVersionist.kTargetDir)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "A0003")


    def test_dir_jumping_version(self):
        pat = "^cat_<version>$"
        directory = os.path.join(TEST_DATA_DIR, "dir_search_test03")
        vernist = FileVersionist(directory, pat, target_type = FileVersionist.kTargetDir)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v007")


    def test_file_default_match(self):
        pat = "^dog_<version>\.txt$"
        directory = os.path.join(TEST_DATA_DIR, "file_search_test01")
        vernist = FileVersionist(directory, pat)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v006")


    def test_file_diff_extension(self):
        pat = "^dog_<version>\.ya?ml$"
        directory = os.path.join(TEST_DATA_DIR, "file_search_test02")
        vernist = FileVersionist(directory, pat)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v004")


    def test_both_default_match(self):
        pat = "^dog_<version>.*$"
        directory = os.path.join(TEST_DATA_DIR, "both_search_test01")
        vernist = FileVersionist(directory, pat, target_type = FileVersionist.kTargetBoth)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v006")




if __name__ == "__main__":
    unittest.main()