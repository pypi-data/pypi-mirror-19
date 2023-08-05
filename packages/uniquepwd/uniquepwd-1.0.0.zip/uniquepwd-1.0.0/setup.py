from setuptools import setup

setup(
    name='uniquepwd',
    version='1.0.0',
    description='A module for getting short unique paths',
    url='https://github.com/jaredwindover/uniquepwd',
    author='Jared Windover',
    author_email='jaredwindover@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    keywords='pwd path short unique',
    py_modules=['uniquepwd'],
    entry_points={
        'console_scripts': [
            'uniquepwd=uniquepwd:main'
        ]
    },
    install_requires=[])
