# -*- coding: utf-8 -*-
import logging
from os import path
from time import sleep
from zipfile import ZipFile, ZIP_DEFLATED

import requests
from io import BytesIO

logger = logging.getLogger('pyscrawl')


class ScrawlError(Exception):
    def __init__(self, message, result):
        super(ScrawlError, self).__init__(message)
        self.result = result


class Scrawl(object):
    """Scrawl API service.

    This allows you to call our API service with ease.

    :param str api_key: Your Scrawl API key.

    .. code-block:: python

        from pyscrawl import Scrawl
        scrawl = Scrawl('my-api-key')

    """
    def __init__(self, api_key):
        self.api_key = api_key

    def upload_zipfile(self, title, filename):
        """Upload a new document to scrawl.

        :param str title: The title of the document.
        :param str filename: Name of the zip-file to upload.

        :rtype: ScrawlResultDocument

        .. code-block:: python

            result = scrawl.upload_zipfile('PyScrawl test', './document.zip')
            result.sleep_until_ready()

        """
        if not path.exists(filename):
            raise ValueError('File does not exist.')

        with open(filename, 'rb') as stream:
            return self.upload_stream(title, stream)

    def upload_container(self, title, container):
        """Upload a new document to scrawl using ScrawlContainer.

        You can use this to construct a zip-file on the fly.

        :param str title: The title of the document.
        :param ScrawlContainer container: The container to upload.

        :rtype: ScrawlResultDocument
        """
        if not isinstance(container, ScrawlContainer):
            raise ValueError('Use ScrawlContainer with `upload_container`.')

        with container as stream:
            return self.upload_stream(title, stream)

    def upload_stream(self, title, stream):
        """Upload a new document using a BytesIO stream.

        We recommand you use :func:`upload_zipfile` or :func:`upload_container`,
        but you can use this when you want to do something more advanced.

        :param str title: The title of the document.
        :param _IOBase stream: The stream to upload.

        :rtype: ScrawlResultDocument
        """
        res = requests.post('http://scrawl.dev/api/upload',
                            data={'title': title},
                            files={'upload': ('document.zip', stream)},
                            headers={'api-key': self.api_key})

        if res.status_code == 200:
            return ScrawlResultDocument(res.json(), self.api_key)
        else:
            raise ScrawlError('Failed to upload stream.',
                              result=res.json())


class ScrawlContainer(object):
    """Scrawl Container (in-memory ZipFile).

    This allows you to programmaticaly build a ZipFile in memory. Use
    :func:`add_file` and :func:`add_content` to build the ZipFile. When
    you are done, you can upload it by calling :meth:`Scrawl.upload_container`.

    :param str api_key: Your Scrawl API key.

    .. code-block:: python

        from pyscrawl import Scrawl, ScrawlContainer
        scrawl = Scrawl('my-api-key')

        # define an index_html using a template engine (for example)
        index_html = '''<html>...</html>'''

        # build a new document
        container = (ScrawlContainer()
                     .add_file('./styles.css')
                     .add_file('./awesome-logo.png')
                     .add_content('index.html', index_html))

        # upload to Scrawl and wait for the conversion.
        result = scrawl.upload_container('PyScrawl test', container)
        result.sleep_until_ready()

    """
    def __init__(self):
        self.filenames = list()
        self.files = dict()
        self.steam = None

    def add_file(self, filename):
        """Add a file from disk to the container.

        :param str filename: The filename on the disk.
        :rtype: ScrawlContainer
        """
        if not path.exists(filename):
            raise ValueError('File does not exist.')

        self.filenames.append(filename)
        return self

    def add_content(self, filename, content):
        """Add content to the container.

        :param str filename: How to represent the content.
        :param str content: The actual content
        :rtype: ScrawlContainer
        """
        self.files[filename] = content
        return self

    def __enter__(self):
        self.stream = self.get_stream()
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stream:
            self.stream.close()

    def get_stream(self):
        """Build a BytesIO in-memory ZipFile based on the files.

        Use :func:`add_file` and :func:`add_content` to prepare the container.
        When done, you can call :func:`get_stream` to build a in-memory ZipFile
        based on the current configuration.

        When using :meth:`Scrawl.upload_container`, this method is automaticly
        called.

        :rtype: BytesIO
        """
        stream = BytesIO()
        zf = ZipFile(stream, 'a', ZIP_DEFLATED, False)

        for filename in self.filenames:
            zf.write(filename, path.basename(filename))

        for filename, content in self.files.items():
            zf.writestr(filename, content)

        zf.close()

        stream.seek(0)
        return stream


class ScrawlResultDocument(object):
    """Scrawl Result Document.

    When calling the API, this result document is returned. It contains
    information about your uploaded document.

    See :meth:`Scrawl.upload_zipfile` or :meth:`Scrawl.upload_container` for
    more information.

    :ivar str api_key: The API key.
    :ivar str info: Information URL.
    :ivar str pdf: URL, for downloading or viewing the PDF.
    :ivar str html: URL, for online viewing the uploaded HTML document.
    :ivar bool converted: `True` when Scrawl has converted the document to PDF.
    :ivar datetime.datetime placed_on: DateTime when the document was added to
        the Scrawler convertion queue.
    :ivar datetime.datetime processed_on: DateTime when the document was
        processed by the Scrawler (`converted` is `True`, when this is set).

    """
    def __init__(self, result, api_key):
        self.api_key = api_key
        self.info = result['info']
        self.pdf = None
        self.html = None
        self.converted = False
        self.placed_on = None
        self.processed_on = None

        self.__update_with(result)

    def sleep_until_ready(self, delay=1):
        """Sleep (in delays) until Scrawl has converted the document.

        Until the :py:data:`converted` bit is set to `True`. You can always
        store the :py:data:`pdf` link, even if the conversion has not yet
        been completed.

        :param int delay: The amount of seconds to sleep (at least 1 second).
        :rtype: bool
        """
        if delay < 1:
            raise ValueError('Delay should not be lower than 1 second.')

        while self.converted is False:
            sleep(delay)
            self.__update()

        return True

    def __update(self):
        res = requests.get(self.info,
                           headers={'api-key': self.api_key})

        self.__update_with(res.json())

    def __update_with(self, json_result):
        if self.info != json_result['info']:
            raise ValueError('API returned a different info link.')

        self.pdf = json_result['pdf']
        self.html = json_result['html']

        self.converted = json_result['converted']

        self.placed_on = json_result['placed_on']
        self.processed_on = json_result['processed_on']
