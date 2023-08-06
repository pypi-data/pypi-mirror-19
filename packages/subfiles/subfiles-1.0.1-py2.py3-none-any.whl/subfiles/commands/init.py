"""The init command."""


from json import dumps

from .base import Base


class Init(Base):
    """Initialize project."""

    def run(self):
        print('Initialization...')
