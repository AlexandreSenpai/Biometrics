from sys import version_info
from rin.server import server

major, minor, micro, _, _ = version_info

__package__ = 'rin'
__version__ = '1.0.0'
__author__ = 'alexandrebsramos@hotmail.com'

assert major >= 3 and minor >= 10, "You must run this program in 3.10 or greater environment."
