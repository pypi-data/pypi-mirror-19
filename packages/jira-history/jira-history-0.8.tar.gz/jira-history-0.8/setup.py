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
    version='0.8',
    author='Sebastian Rahlf',
    author_email='basti@redtoad.de',
    packages=['jira_history'],
    requires=['jira'],
    license='MIT'
)