from setuptools import setup

VERSION = "0.2.3"

setup(
    name='img2pdf-legacy-python',
    version=VERSION,
    author="Lucas Wiman (fork); Johannes 'josch' Schauer (original author)",
    author_email='lucas.wiman@gmail.com',
    description="Python 2-compatible fork of img2pdf",
    long_description=open('README.md').read(),
    license="LGPL",
    keywords="jpeg pdf converter",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: GNU Lesser General Public License v3 '
        '(LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    url='https://github.com/lucaswiman/img2pdf-legacy-python',
    package_dir={"": "src"},
    py_modules=['img2pdf', 'jp2'],
    include_package_data=True,
    test_suite='tests.test_suite',
    zip_safe=True,
    install_requires=(
        'Pillow',
    ),
    entry_points='''
    [console_scripts]
    img2pdf = img2pdf:main
    ''',
    )
