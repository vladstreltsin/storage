import io
import pickle

from remotools._savers_old import BaseSaver
from remotools.utils import keep_position


class PickleSaver(BaseSaver):

    def save(self, obj, key=None, check_exists=False, *args, **kwargs):
        key = key or self.default_save_key
        f = io.BytesIO()
        with keep_position(f):
            pickle.dump(obj, f, *args, **kwargs)
        return self.remote.upload(f, key, check_exists=check_exists)

    def load(self, key, search_cache=True, *args, **kwargs):
        f = io.BytesIO()
        with keep_position(f):
            self.remote.download(f, key, search_cache=search_cache)
        return pickle.load(f, *args, **kwargs)
