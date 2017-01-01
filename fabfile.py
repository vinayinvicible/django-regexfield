from __future__ import absolute_import, unicode_literals

from fabric.api import task, local


@task
def clean():
    local('rm -rf build dist *.egg regexfield/__pycache__ regexfield/*.pyc')


@task
def bump_version(part='patch'):
    local('pip install --upgrade bumpversion')
    local('bumpversion {}'.format(part))
    local('git push')
    local('git push --tags')


@task
def release(part='patch'):
    bump_version(part=part)
    pypi()


@task
def pypi():
    clean()
    local('pip install --upgrade wheel')
    local('python setup.py clean')
    local('python setup.py sdist bdist_wheel')
    local('twine upload dist/*')
