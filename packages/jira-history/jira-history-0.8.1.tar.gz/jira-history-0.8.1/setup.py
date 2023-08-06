from distutils.core import setup
import os


def read(path):
    root = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(root, path)).read()


setup(
    name='jira-history',
    description='Makes working with Jira issue changelogs a breeze!',
    long_description=read('README.rst'),
    url='https://github.com/redtoad/jira-history',
    version='0.8.1',
    author='Sebastian Rahlf',
    author_email='basti@redtoad.de',
    packages=['jira_history'],
    requires=['jira'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='jira changelog ticket history'
)
