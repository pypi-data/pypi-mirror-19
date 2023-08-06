from setuptools import setup

# specify requirements of your package here
REQUIREMENTS = ['image2gif', 'Pillow==3.3.1']

# some more details
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Operating System :: POSIX'
    ]

# calling the setup function 
setup(name='iamgif',
      version='0.0.1',
      description='Python library to convert text to GIF',
      long_description=open('README.md').read(),
      url='https://github.com/rahulxxarora/iamgif',
      author='Rahul Arora',
      author_email='coderahul94@gmail.com',
      license='MIT',
      packages=['iamgif'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='GIF PYthon text to image'
      )