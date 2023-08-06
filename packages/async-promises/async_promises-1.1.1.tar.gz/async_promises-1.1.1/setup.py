from setuptools import setup

setup(
    name='async_promises',
    version='1.1.1',
    description='(Fork of) Promises/A+ implementation for Python',
    long_description=open('README.rst').read(),
    url='https://github.com/p2p-today/promise',
    author='Syrus Akbary',
    author_email='me@syrusakbary.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
    ],

    keywords='concurrent future deferred promise',
    packages=["async_promises"],
    install_requires=[
        'typing',
    ],
    tests_require=['pytest>=2.7.3', 'futures'],
)
