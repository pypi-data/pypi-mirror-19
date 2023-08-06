# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name="nim_install",
    version_info=(0, 2, 1),
    __version__='0.2.1',
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="install nim compiler in Linux virtualenv assumes gcc",
    # keywords="",
    entry_points='nim_install',
    # entry_points=None,
    license="MIT",
    since=2016,
    # data_files="",
    # universal=True,
    install_requires=dict(
        any=[],
        py27=['backports.lzma'],
    ),
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']


def main():
    import sys
    import os
    import tarfile
    if sys.version_info < (3, ):
        from backports import lzma
        from urllib2 import urlopen
    else:
        import lzma
        from urllib.request import urlopen
    nim_version = version_info
    nim_version = (0, 16, 0)
    nim_download = 'http://nim-lang.org/download/nim-{}.tar.xz'.format(
        '.'.join([str(x) for x in nim_version]))
    print('getting', nim_download)
    inst_dir = os.path.dirname(os.path.dirname(sys.executable))
    print('inst_dir', inst_dir)
    os.chdir(inst_dir)
    if True:
        from io import BytesIO
        response = urlopen(nim_download)
        data = BytesIO()
        data.write(lzma.decompress(response.read()))
        data.seek(0)
        with tarfile.open(fileobj=data, mode='r') as tar:
            for tarinfo in tar:
                if '/' not in tarinfo.name:
                    continue
                name = tarinfo.name.split('/', 1)[1]
                if tarinfo.isdir():
                    if not os.path.exists(name):
                        os.mkdir(name)
                    continue
                # print('tarinfo', tarinfo.name, name, tarinfo.isdir())
                with open(name, 'wb') as fp:
                    fp.write(tar.extractfile(tarinfo).read())

    os.system('make -j8')
    os.system('./bin/nim c koch')
    os.system('./koch tools')

if __name__ == '__main__':
    main()
