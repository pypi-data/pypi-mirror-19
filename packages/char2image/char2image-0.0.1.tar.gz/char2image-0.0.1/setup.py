import re
import setuptools


setuptools.setup(
    name='char2image',
    version=re.search(r"__version__ *= *'([0-9]+\.[0-9]+\.[0-9]+)' *\n",
                      open('char2image/__init__.py').read()).group(1),
    description='Creates a dictionary of character to font image in JSON format.',
    long_description=open('README.md').read(),
    license='Public Domain',
    author='Yota Toyama',
    author_email='raviqqe@gmail.com',
    url='https://github.com/raviqqe/char2image.py/',
    packages=['char2image'],
    entry_points={
            'console_scripts': [
                'char2image=char2image.__main__:main',
                'chars2images=char2image.chars2images_main:main'
            ],
    },
    install_requires=['docopt', 'numpy', 'pillow'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Fonts',
    ],
)
