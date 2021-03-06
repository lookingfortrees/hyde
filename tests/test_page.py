from pathlib import Path
import datetime
from bs4 import BeautifulSoup

import unittest

from hyde.pages import Metadata, ContentPage
from hyde.errors import HydeError
from .utils import *


class TestContentPage(unittest.TestCase):
    def setUp(self) -> None:
        self.m_post = Metadata("test title", "test-title-stub")

    def test_page_init(self):
        p = ContentPage(self.m_post, None)
        self.assertEqual(p.content, None)
        self.assertEqual(p.template_file, "post.html.jinja2")
        self.assertEqual(p.url, "/test-title-stub.html")

    def test_page_from_file(self):
        test_file = TEST_PAGE_FILES[0]
        p = page_from_file_str(test_file)

        self.assertEqual(p.meta.title, "Test post")
        self.assertEqual(p.meta.template, "post")
        self.assertEqual(p.meta.content_group, "posts")
        self.assertEqual(p.meta.date, datetime.date(year=2021, month=3, day=1))
        self.assertEqual(p.meta.author, "Hyde")
        self.assertEqual(p.meta.urlstub, "test-title-stub")
        self.assertEqual(p.content, test_file["html"])
        self.assertEqual(p.template_file, "post.html.jinja2")
        self.assertEqual(p.url, "/test-title-stub.html")

    def test_page_render_has_navbar(self):
        test_file = TEST_PAGE_FILES[0]
        p = page_from_file_str(test_file)

        html_doc = p.render(get_jinja2_env(), nav_bar_pages=nav_bar_pages)
        soup = BeautifulSoup(html_doc, features="html.parser")

        assert_expected_hrefs_in_soup(soup, ["/index.html"])        

    def test_page_path_to_content_file_cannot_be_more_than_one_level_deep(self):
        test_file = INVALID_PATH_FILE

        with self.assertRaises(SystemExit):
            page_from_file_str(test_file)


if __name__ == '__main__':
    unittest.main()