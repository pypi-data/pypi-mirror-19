import os
import contextlib
from invoke.exceptions import Exit

from spynl.main.pkg_utils import get_spynl_package, get_spynl_packages


def resolve_package_names(packages_param, complain_not_installed=True):
    """resolve "packages" string parameter into a list of packages"""
    installed_package_names = [r.project_name for r in get_spynl_packages()]
    installed_package_names.sort()
    if packages_param != '_all':
        given_names = packages_param.split(',')
        for name in given_names:
            if name not in installed_package_names and complain_not_installed:
                raise Exit("Package %s is not installed. Exiting ..." % name)
        return given_names
    return installed_package_names


@contextlib.contextmanager
def package_dir(package_name=None):
    """Change to this package's directory during this context"""
    curdir = os.getcwd()
    try:
        if package_name is not None:
            package = get_spynl_package(package_name)
            if package is not None:
                os.chdir(package.location)
        yield
    finally:
        os.chdir(curdir)


@contextlib.contextmanager
def chdir(dirname=None):
    """Change to this directory during this context"""
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def assert_response_code(response, exp_code):
    """
    Make it easy to expect one or more HTTP status codes
    in a requests library response.
    """
    code = response.status_code
    if isinstance(exp_code, tuple):
        if not code in exp_code:
            raise Exit("Code %s is not in %s when testing %s"
                       % (code, exp_code, response.request.url))
    else:
        if not code == exp_code:
            raise Exit("Code %s was expected to be %s when testing %s "
                       % (code, exp_code, response.request.url))
