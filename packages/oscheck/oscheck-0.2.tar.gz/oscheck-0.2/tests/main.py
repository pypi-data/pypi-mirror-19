import platform
from unittest import TestCase

from oscheck import (
    family,
    OS_OSX,
    OS_LINUX,
    OS_JAVA,
    OS_WINDOWS,
    UnknownOSError
)


class MainTests(TestCase):
    def test_family(self):
        system_family = platform.system()
        if system_family == 'Linux':
            self.assertEqual(family(), OS_LINUX)
        elif system_family == "Darwin":
            self.assertEqual(family(), OS_OSX)
        elif system_family == "Windows":
            self.assertEqual(family(), OS_WINDOWS)
        elif system_family == "Java":
            self.assertEqual(family(), OS_JAVA)
        else:
            with self.assertRaises(UnknownOSError):
                family()
