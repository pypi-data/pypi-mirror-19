from setuptools import setup, find_packages

import versioneer

setup(
    name='cmdvars',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Read environment variables defined in a shell script into Python.',
    author_email='xoviat@users.noreply.github.com',
    license='Apache2',
    packages=find_packages(),
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    url="http://github.com/xoviat/cmdvars",
    author="Mars Galactic",
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
