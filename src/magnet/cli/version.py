import importlib.metadata


def get_magnet_version() -> str:
    """Get the version number of Magnet running the CLI"""
    return importlib.metadata.version("magnet")
