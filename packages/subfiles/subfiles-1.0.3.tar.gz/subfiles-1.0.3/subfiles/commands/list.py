"""The list command."""


from json import dumps

from .base import Base

from .utils import files_by_extensions

class List(Base):

    def run(self):

        results = files_by_extensions('.')

        for key, val in enumerate(results):
            print("[*.{key}]".format(**{'key':val}))
            for item in results[val]:
                print(item)
            print("\n"),
