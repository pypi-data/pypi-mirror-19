from setuptools import setup, find_packages

setup(
    name = 'extopen',
    version = '0.1',
    description = "Cross platform helper for opening a file with the default external application.",
    author = 'Tim Savage',
    author_email = 'tim@savage.company',
    license = 'BSD',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: BSD License',

        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe = True,

    py_modules = ['extopen']
)
