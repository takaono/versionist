# -*- coding: utf-8 -*-
import os
import re
import unittest

from versionist import Versionist, VersionKeyError

class TestVersioninst(unittest.TestCase):

    TEST_NAME_LIST1 = ["dog_v001", "dog_v002", "dog_v003", "dog_v004_cat",
                       "cat_v001", "cat_v005", "cat_v008",
                       "dog_big_v001", "dog_small_v002",
                       "rat_v01", "rat_v02", "rat_v03",
                       "dog_ver001", "dog_ver002", "dog_ver003",
                       "pig_001", "pig_005"]

    def setUp(self):
        Versionist.set_version_key("version")


    def tearDown(self):
        Versionist.set_version_key("version")


    def test_default_match(self):
        pat = "^dog\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v003")


    def test_default_match_get_ver_num(self):
        pat = "^dog\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        latest_version_num = vernist.get_latest_version_num()
        self.assertEqual(latest_version_num, 3)


    def test_default_match_get_next_name(self):
        pat = "^dog\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v004")


    def test_search_type_get_next_name(self):
        pat = "dog\_<version>"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat, match_type = Versionist.kSearchType)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v005")


    def test_regex_match(self):
        pat = "^dog\_\w+\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v002")


    def test_regex_match_without_token(self):
        pat = "^rat\_(?P<version>v\d{2})$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v03")


    def test_no_version_exists(self):
        pat = "^rabbit\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        latest_version_name = vernist.get_latest_version_name()
        self.assertIsNone(latest_version_name)


    def test_get_next_from_no_version(self):
        pat = "^rabbit\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v001")


    def test_get_next_from_no_version_for_zero_start(self):
        pat = "^rabbit\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat, initial_number = 0)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v000")


    def test_get_latest_with_skipping_versions(self):
        pat = "^cat\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v008")


    def test_get_next_with_skipping_versions(self):
        pat = "^cat\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        next_version_name = vernist.get_next_version_name()
        self.assertEqual(next_version_name, "v009")


    def test_diff_padding(self):
        pat = "^rat\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat, padding = 2)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v03")


    def test_diff_prefix(self):
        pat = "^dog\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat, prefix="ver")
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "ver003")


    def test_empty_prefix(self):
        pat = "^pig\_<version>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat, prefix="")
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "005")


    def test_diff_version_key(self):
        pat = "^dog\_<version_name>$"
        targets = self.TEST_NAME_LIST1
        Versionist.set_version_key("version_name")
        vernist = Versionist(targets, pat)
        latest_version_name = vernist.get_latest_version_name()
        self.assertEqual(latest_version_name, "v003")


    def test_no_version_key(self):
        pat = "^dog\_<version_name>$"
        targets = self.TEST_NAME_LIST1
        vernist = Versionist(targets, pat)
        with self.assertRaises(VersionKeyError):
            latest_version_name = vernist.get_latest_version_name()



if __name__ == "__main__":
    unittest.main()