from unittest import TestCase

import extract


class Test(TestCase):
    def test_parse_page_arg(self):
        tests = [
            ("1,2,3,4,5", {1, 2, 3, 4, 5}, None),
            (1, None, TypeError),
            ("1,3-5", {1, 3, 4, 5}, None),
            ("1-,3,4", None, ValueError),
            ("--", None, ValueError),
            (",", set(), None),
            ("", set(), None),
            ("-", None, ValueError),
            ("1,", {1}, None),
            ("1,a,3,4", None, ValueError),
            ("1", {1}, None),
            ("1.0,2.0", None, ValueError),
            ("1.0-2.0", None, ValueError),
            ("a-c", None, ValueError),
            ("1-3,2-4,3-5", {1, 2, 3, 4, 5}, None),
            ("1,1,1,1,1,2,2,3", {1, 2, 3}, None),
            ("1 2 3 4", None, ValueError),
            ("1-2, 3-4, 5-6", {1, 2, 3, 4, 5, 6}, None)
        ]
        for pages, exp, err in tests:
            print(f"Testing page argument '{pages}'")
            if err is None:
                act = extract.parse_page_arg(pages)
                self.assertEqual(
                    exp,
                    act,
                    f"Test page argument {pages} returns {act} rather than the expected value of {exp}"
                )

            else:
                with self.assertRaises(err):
                    extract.parse_page_arg(pages)
