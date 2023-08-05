import os
import uuid

from .fs import Uploader as FSUploader


class Uploader(FSUploader):

    async def get_upload_path(self):
        path = await super(Uploader, self).get_upload_path()
        folder = uuid.uuid4().hex
        return os.path.join(path, folder)

