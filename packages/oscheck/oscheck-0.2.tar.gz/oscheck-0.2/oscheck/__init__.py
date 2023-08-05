import platform

from .exceptions import UnknownOSError

OS_LINUX = 1
OS_OSX = 2
OS_WINDOWS = 3
OS_JAVA = 4


def family():
    system_family = platform.system()
    if system_family == 'Linux':
        return OS_LINUX
    elif system_family == "Darwin":
        return OS_OSX
    elif system_family == "Windows":
        return OS_WINDOWS
    elif system_family == "Java":
        return OS_JAVA
    else:
        raise UnknownOSError(system_family)
