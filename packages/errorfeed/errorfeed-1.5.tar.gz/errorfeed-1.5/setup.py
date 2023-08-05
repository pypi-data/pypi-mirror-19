from setuptools import setup, find_packages

version = '1.5'
url = 'https://github.com/ErrorFeed/errorfeed-python'

setup(
    name='errorfeed',
    description='ErrorFeed client and WSGI middleware',
    keywords='error feed errorfeed exception tracking api',
    version=version,
    author="Ken Kinder",
    author_email="kkinder@errorfeed.com",
    url=url,
    test_suite='tests',
    packages=find_packages(exclude=['tests']),
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.4",
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Intended Audience :: Developers',
                 ],
    license='Apache License (2.0)'
)
