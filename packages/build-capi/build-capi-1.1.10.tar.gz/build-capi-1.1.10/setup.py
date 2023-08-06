import os
import sys

from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (OSError, IOError, ImportError):
    long_description = open('README.md').read()


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner'] if needs_pytest else []

    setup_requires = pytest_runner
    install_requires = []
    tests_require = ['pytest']

    metadata = dict(
        name='build-capi',
        version='1.1.10',
        maintainer="Danilo Horta",
        maintainer_email="horta@ebi.ac.uk",
        description='Build and distribute C/C++ static libraries',
        long_description=long_description,
        license="MIT",
        url='http://github.com/glimix/build-capi',
        packages=find_packages(),
        zip_safe=False,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",
        ],
        entry_points={
            'distutils.commands': [
                'build_capi = build_capi.build:build_capi',
            ],
            'distutils.setup_keywords': [
                'capi_libs = build_capi.ext:capi_libs',
            ],
        }, )

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)


if __name__ == '__main__':
    setup_package()
