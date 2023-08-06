from setuptools import setup

# specify requirements of your package here
REQUIREMENTS = ['requests', 'BeautifulSoup4>=4.5.3', 'lxml>=3.6.4']

# some more details
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Operating System :: POSIX'
    ]

# calling the setup function 
setup(name='wordster',
      version='0.0.1',
      description='A small wrapper around official Merriam Webster dictionary',
      long_description=open('README.md').read(),
      url='https://github.com/rahulxxarora/wordster',
      author='Rahul Arora',
      author_email='coderahul94@gmail.com',
      license='MIT',
      packages=['wordster'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='dictionary merriam webster meaning'
      )