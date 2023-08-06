# -*- coding: utf-8 -*-

from io import StringIO, open
import os
import unittest

import httpretty

from py_w3c.validators.html.validator import HTMLValidator, VALIDATOR_URL

#
# To make real request to W3C comment httpretty.activate decorator.
#

TESTS_DIR = os.path.join('py_w3c', 'tests')
RESPONSES_DIR = os.path.join(TESTS_DIR, 'responses')

# Page without errors. Needed for success check tests.
VALID_URL = 'https://www.w3.org/'


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = HTMLValidator(charset='utf-8')

    @httpretty.activate
    def test_url_validation(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'url-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.GET, VALIDATOR_URL, body=body)

        self.validator.validate(VALID_URL)
        self.assertEqual(self.validator.errors, [])
        self.assertEqual(self.validator.warnings, [])

    @httpretty.activate
    def test_file_validation(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'file-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.POST, VALIDATOR_URL, body=body)
        with open(self._fullpath('file.html')) as f:
            self.validator.validate_file(f)
            self.assertEqual(len(self.validator.errors), 1)
            self.assertEqual(int(self.validator.errors[0].get('lastLine')), 3)

    @httpretty.activate
    def test_validation_by_file_name(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'file-name-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.POST, VALIDATOR_URL, body=body)
        with open(self._fullpath('file.html')) as f:
            self.validator.validate_file(f.name)
            self.assertEqual(len(self.validator.errors), 1)
            self.assertEqual(int(self.validator.errors[0].get('lastLine')), 3)

    @httpretty.activate
    def test_validation_by_file_with_unicode_name(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'unicode-file-name-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.POST, VALIDATOR_URL, body=body)
        with open(self._fullpath(u'мой-файл.html')) as f:
            self.validator.validate_file(f.name)
            self.assertEqual(len(self.validator.errors), 1)
            self.assertEqual(int(self.validator.errors[0].get('lastLine')), 3)

    @httpretty.activate
    def test_in_memory_file_validation(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'in-memory-file-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.POST, VALIDATOR_URL, body=body)
        HTML = u'''<!DOCTYPE html>
            <html>
                <head bad-attr="i'm bad">
                    <title>py_w3c test</title>
                </head>
                <body>
                    <h1>Hello py_w3c</h1>
                </body>
            </html>
        '''
        self.validator.validate_file(StringIO(HTML))
        self.assertEqual(len(self.validator.errors), 1)
        self.assertEqual(int(self.validator.errors[0].get('lastLine')), 3)

    @httpretty.activate
    def test_fragment_validation(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'fragment-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.POST, VALIDATOR_URL, body=body)
        fragment = u'''<!DOCTYPE html>
            <html>
                <head>
                    <title>testing py_w3c</title>
                </head>
                <body>
                    <badtag>i'm bad</badtag>
                    <div>my div</div>
                </body>
            </html>
        '''
        self.validator.validate_fragment(fragment)
        self.assertEqual(len(self.validator.errors), 1)
        self.assertEqual(int(self.validator.errors[0].get('lastLine'),), 7)

    @httpretty.activate
    def test_passing_charset_forces_validator_to_use_given_charset(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'custom-charset-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.GET, VALIDATOR_URL, body=body)
        val = HTMLValidator(charset='windows-1251')
        val.validate(VALID_URL)
        self.assertEqual(len(val.info), 2)
        self.assertIn(
            val.info[0]['message'],
            u'Overriding document character encoding from “utf-8” to “windows-1251”.')

    @httpretty.activate
    def test_passing_wrong_charset_forces_to_sniff(self):
        # To make real request to W3C comment httpretty.activate decorator.
        response_file = os.path.join(RESPONSES_DIR, 'wrong-charset-validation-response.json')
        with open(response_file) as f:
            body = f.read()
        httpretty.register_uri(httpretty.GET, VALIDATOR_URL, body=body)
        val = HTMLValidator(charset='win-1251')
        val.validate(VALID_URL)
        self.assertEqual(len(val.errors), 1)
        self.assertIn('Unsupported character encoding name', val.errors[0]['message'])

    def _fullpath(self, filename):
        """Returns full for file in tests directory."""
        return os.path.join(TESTS_DIR, 'validators', 'html', filename)
