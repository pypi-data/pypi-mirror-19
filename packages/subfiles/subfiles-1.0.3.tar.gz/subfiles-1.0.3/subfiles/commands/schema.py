"""The schema command."""


from json import dumps

from .base import Base

from .utils import files_by_extensions

class Schema(Base):
    """Initialize project."""

    def run(self):

        results = files_by_extensions('.')

        for key, val in enumerate(results):
            print("[*.{key}]".format(**{'key':val}))
            print("\n"),
