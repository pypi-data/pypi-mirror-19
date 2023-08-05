import argparse


_PARSER = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
_ARGS = None


class _Args:

    def __getattr__(self, name):
        global _ARGS

        if _ARGS == None:
            _ARGS = _PARSER.parse_args()

        return getattr(_ARGS, name)

ARGS = _Args()


def add_argument(*args, **kwargs):
    _PARSER.add_argument(*args, **kwargs)


def parse_args(*args, **kwargs):
    global _ARGS
    _ARGS = _PARSER.parse_args(*args, **kwargs)
