import io
from os import path as osp
import numpy as np


from remotools._savers_old import BaseSaver
from remotools.utils import keep_position
from PIL import Image


class ImageSaver(BaseSaver):

    def save(self, obj, key=None, check_exists=False, ext=None, *args, **kwargs):

        key = key or self.default_save_key

        # Try figuring out the format from the file extension
        if not ext and key:
            ext = osp.splitext(key)[1].lower()

        # In case format comes out '' or stays None - use the default which is JPEG
        if not ext:
            ext = ext or '.jpg'

        # PIL quirks Image.EXTENSION is initialized upon import
        if not Image.EXTENSION:
            Image.init()

        f = io.BytesIO()
        with keep_position(f):
            Image.fromarray(obj).save(f, *args, format=Image.EXTENSION[ext], **kwargs)
        return self.remote.upload(f, key, check_exists=check_exists)

    def load(self, key, search_cache=True, *args, **kwargs):
        f = io.BytesIO()
        with keep_position(f):
            self.remote.download(f, key, search_cache=search_cache)
        return np.asarray(Image.open(f, *args, **kwargs))

    def size(self, key):
        f = io.BytesIO()
        with keep_position(f):
            self.remote.download(f, key)
        image = Image.open(f)  # Use PIL's lazy loading to get only the image parameters
        width, height = image.size
        return height, width
