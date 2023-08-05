from setuptools import setup

def readme():
  with open("README.rst") as f:
    return f.read()
setup(name='aetf',
      version='0.0.4',
      description='Python package for autoencoding(Deep Learning) functionality using TensorFlow',
      long_description = readme(),
      classifiers=['Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      url='https://bitbucket.org/HNGML/aetf',
      author='hngml',
      author_email='nilesh.chaudhari@healthnextgen.com',
      license='MIT',
      packages=['aetf'],
      install_requires=[
          'markdown',
      ],
      scripts=['bin/aetf'],#write a separate script file for a command line call
      #entry_points = {'console_scripts':['test-me-again=test_package.terminal_functions:main'],},
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)