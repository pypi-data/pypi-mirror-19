# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name="nim",
    version_info=(0, 1, 0),
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="python to nim interfacing",
    # keywords="",
    entry_points='nim=nim.__main__:main',
    # entry_points=None,
    license="Copyright Ruamel bvba 2007-2017",
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    install_requires=dict(
        any=["ruamel.appconfig", "ruamel.std.argparse"],
        # py27=["ruamel.ordereddict"],
    ),
)


def _convert_version(tup):
    """Create a PEP 386 pseudo-format conformant string from tuple tup."""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val

version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version
