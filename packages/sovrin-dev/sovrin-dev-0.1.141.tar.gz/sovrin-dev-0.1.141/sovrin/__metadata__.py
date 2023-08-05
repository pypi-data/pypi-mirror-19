"""
Sovrin package metadata
"""
__version_info__ = (0, 1, 141)
__version__ = '{}.{}.{}'.format(*__version_info__)
__author__ = "Evernym, Inc."
__license__ = "Apache 2.0"

__all__ = ['__version_info__', '__version__', '__author__', '__license__']

__dependencies__ = {
    "plenum": ">=0.1.158",
    "anoncreds": ">=0.1.4",
}
