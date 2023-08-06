import os.path

import six

from .base import Model, Collection, DATA_DIRECTORY


ZIP_CODE_GEOJSON_PATH = os.path.join(DATA_DIRECTORY, 'chicago_zip_codes.geojson')

class ZipCode(Model):
    fields = [
        'zip',
    ]


class ZipCodeCollection(Collection):
    model = ZipCode

    def __init__(self):
        self._by_zip = {}
        super(ZipCodeCollection, self).__init__()

    def add_item(self, item):
        super(ZipCodeCollection, self).add_item(item)
        self._by_zip[item.zip] = item

    def get_by_zip(self, zip_code):
        return self._by_zip[six.text_type(zip_code)]

    def default_sort(self):
        self._items = sorted(self._items, key=lambda p: p.zip)
        return self

    def is_chicago(self, zip_code):
        return six.text_type(zip_code) in self._by_zip


ZIP_CODES = ZipCodeCollection().from_geojson(ZIP_CODE_GEOJSON_PATH)
