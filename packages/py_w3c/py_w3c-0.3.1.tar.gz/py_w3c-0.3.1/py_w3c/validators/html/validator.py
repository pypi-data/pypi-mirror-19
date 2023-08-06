from io import IOBase
import json

import sys

from py_w3c.multipart import Multipart
from py_w3c.exceptions import AccessForbidden
from py_w3c import __version__

if sys.version_info >= (3, 0):
    # Py3
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
else:
    # Py2
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

try:
    # Py2
    unicode
except NameError:
    # Py3
    unicode = str

VALIDATOR_URL = 'https://validator.w3.org/nu/'


class HTMLValidator(object):
    def __init__(self, validator_url=VALIDATOR_URL, charset=None, verbose=False):
        self.validator_url = validator_url
        self.uri = ''
        self.uploaded_file = ''
        self.output = 'json'
        self.charset = charset
        self.errors = []
        self.warnings = []
        self.info = []
        self.verbose = verbose

    def validate(self, uri):
        """Validates by uri."""
        get_data = {'doc': uri, 'out': self.output}
        if self.charset:
            get_data['charset'] = self.charset
        get_data = urlencode(get_data)
        return self._validate(self.validator_url + '?' + get_data)

    def validate_file(self, filename_or_file, name='file'):
        """Validates file by filename or file content."""
        m = Multipart()
        m.field('out', self.output)
        if self.charset:
            m.field('charset', self.charset)
        if isinstance(filename_or_file, (str, unicode)):
            with open(filename_or_file, 'r') as w:
                content = w.read()
        elif isinstance(filename_or_file, IOBase):
            content = filename_or_file.read()
        else:
            raise Exception(
                'File name or file only. Got %s instead' % type(filename_or_file))
        m.file('uploaded_file', name, content, {'Content-Type': 'text/html'})
        ct, body = m.get()
        return self._validate(self.validator_url, headers={'Content-Type': ct}, post_data=body)

    def validate_fragment(self, fragment):
        """Validates fragment.

        Note:
            Full html fragment only.

        Args:
            fragment (str): html text to validate.

        """
        m = Multipart()
        m.field('out', self.output)
        if self.charset:
            m.field('charset', self.charset)

        m.field('fragment', fragment)
        ct, body = m.get()
        return self._validate(self.validator_url, headers={'Content-Type': ct}, post_data=body)

    def _send_request(self, url, headers=None, post_data=None):
        """Sends HTTP request to the validator

        Args:
            url (str): URL where to send request.
            headers (dict, optional): HTTP headers.
            post_data (bytes, optional): POST data. If empty, send GET request.

        Returns:
            boolean: True if validation was success, otherwise raises exception.

        """
        if not headers:
            headers = {}
        if sys.version_info >= (3, 0):
            if isinstance(post_data, str):
                post_data = post_data.encode('utf-8')
        else:
            # Python2
            if isinstance(post_data, unicode):
                post_data = post_data.encode('utf-8')
        req = Request(url, headers=headers, data=post_data)
        try:
            resp = urlopen(req)
        except HTTPError as exc:
            if exc.code == 403:
                raise AccessForbidden('Access forbidden by W3C. Response data: \n {}'.format(resp.read()))
            else:
                raise
        return resp

    def _validate(self, url, headers=None, post_data=None):
        resp = self._send_request(url, headers=headers, post_data=post_data)
        self._process_response(resp.read())
        return True

    def _process_response(self, response):
        """Converts http response to the errors or warnings."""
        resp = json.loads(response.decode('utf-8'))

        for message in resp.get('messages', []):
            if message['type'] == 'error':
                self.errors.append(message)
            elif message['type'] == 'warning':
                self.warnings.append(message)
            elif message['type'] == 'info':
                self.info.append(message)

        if self.verbose:
            print('Errors: %s' % len(self.errors))
            print('Warnings: %s' % len(self.warnings))


def main(argv=None):
    usage = '  Usage: \n    w3c_validate http://yourdomain.org'
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        print(usage)
        sys.exit(2)
    if argv[1] in ('-v', '--version'):
        print(__version__)
        sys.exit(0)
    val = HTMLValidator(verbose=False)
    val.validate(argv[1])
    print('---warnings---(%s)' % len(val.warnings))
    for warning in val.warnings:
        msg = 'firstLine: %s, lastLine: %s, hiliteLength: %s\n    message: %s' \
            % (warning.get('firstLine'), warning.get('lastLine'),
               warning.get('hiliteLength'), warning.get('message'))
        print(msg)
        print()

    print('---errors---(%s)' % len(val.errors))
    for error in val.errors:
        msg = 'firstLine: %s, lastLine: %s, hiliteLength: %s\n    message: %s' \
            % (error.get('firstLine'), error.get('lastLine'),
               error.get('hiliteLength'), error.get('message'))
        print(msg)
        print()
    sys.exit(0)
