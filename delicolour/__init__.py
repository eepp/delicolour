__version__ = '1.3.0'


def _split_version_suffix():
    return __version__.split('-')


def get_version_tuple():
    version, suffix = _split_version_suffix()
    parts = version.split('.')

    return (int(parts[0]), int(parts[1]), int(parts[2]))


def get_version_suffix():
    return _split_version_suffix()[1]
