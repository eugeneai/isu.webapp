from zope.i18nmessageid import MessageFactory
from .interfaces import IFileStorageView, IFileStorage
from zope.interface import implementer
from isu.webapp.storage.views import StorageView

import logging
logger = logging.getLogger("isu.webapp")


_ = MessageFactory("isu.webapp")


class FileUploadEvent(object):
    def __init__(self, file, request=None, view=None):
        self.file = file
        self.request = request
        self.view = view


class FileStorageView(StorageView):
    title = _('File upload')

    def form(self):
        return self.response()

    def upload(self):
        request = self.request
        post = request.POST
        response = request.response
        response.status_code = 201
        file = post.get('file', None)
        if file is None or file.filename is None:
            response.status_code = 400
            return {
                'error':
                'no file',
                'result':
                'KO',
                'explanation':
                _('check input form if it contains "file" field of type file')
            }
        self.file = file

        self.registry.notify(
            FileUploadEvent(file, request=self.request, view=self))
        if self.on_upload(file=file):
            return {'error': None, 'result': 'OK', 'filename': file.filename}

    def files(self, filter=None):
        storage = self._get_storage()
        storage.set_session(self.registry.dbsession())
        files = storage.files(filter=filter)
        return self.response(files=files, context=files)

    def on_upload(self, file):
        """Run after file being uploaded to server.

        Returns True if file upload post processing was successful,
        else raises an HTTPResponse exception.

        """
        logger.debug("File upload event {}".format(file))
        storage = self._get_storage()
        storage.set_session(self.registry.dbsession())
        storage.store(file)
        return True

    def _get_storage(self):
        return self.registry.getUtility(IFileStorage, 'file-storage')
