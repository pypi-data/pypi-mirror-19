from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='TrackingProjectCFT',
      version='0.1',
      description='TrackingProjectCFT',
      long_description=readme(),
      classifiers=['Development Status :: 3 - Alpha',
                   ],
      url='https://bitbucket.org/MaceSteve/trackingprojectcft',
      author='me',
      author_email='me@mywebsite',
      packages=['TrackingProjectCFT'],
      # dependency_links=['https://github.com/something.git'],
      install_requires=['requests',
                        'flake8',
                        'isort',
                        'tox'
                        ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={'console_scripts': ['main=TrackingProject.main:main',
                                        ],
                    },
      include_package_data=True,
      zip_safe=False)
