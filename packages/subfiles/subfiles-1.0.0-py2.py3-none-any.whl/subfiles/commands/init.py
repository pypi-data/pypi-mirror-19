"""The init command."""


from json import dumps

from .base import Base


class Hello(Base):
    """Initialize project."""

    def run(self):
        print('Initialization...')
        import ipdb; ipdb.set_trace();
