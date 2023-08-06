from fabric.api import *
from fabric.contrib.files import exists, upload_template
from lib_fabric_dreamhost.helpers import get_templates_folder


def git_clone(project_name, repository):
    if not exists("~/{PROJECT_NAME}".format(PROJECT_NAME=project_name)):
        run("git clone {REPOSITORY} ~/{PROJECT_NAME}".format(REPOSITORY=repository, PROJECT_NAME=project_name))
        with cd("~/{PROJECT_NAME}".format(PROJECT_NAME=project_name)):
            run("git submodule update --init")


def git_update(project_name, branch='master'):
    with cd("~/{PROJECT_NAME}".format(PROJECT_NAME=project_name)):
        run("git fetch")
        run("git pull")
        run("git checkout {BRANCH}".format(BRANCH=branch))
        run("git submodule update --init")


def pip_install(project_name):
    with cd("~/{PROJECT_NAME}".format(PROJECT_NAME=project_name)):
        with prefix('source ~/.virtualenv/{VIRTUALENV}/bin/activate'.format(VIRTUALENV=project_name)):
            run('pip install -r requirements/production.txt')


def collectstatic(project_name, settings):
    with cd("~/{PROJECT_NAME}/source".format(PROJECT_NAME=project_name)):
        with prefix('source ~/.virtualenv/{VIRTUALENV}/bin/activate'.format(VIRTUALENV=project_name)):
            run('python manage.py collectstatic --settings={SETTINGS} --noinput'.format(SETTINGS=settings))


def db_migrate(project_name, settings):
    with cd("~/{PROJECT_NAME}/source".format(PROJECT_NAME=project_name)):
        with prefix('source ~/.virtualenv/{VIRTUALENV}/bin/activate'.format(VIRTUALENV=project_name)):
            run('python manage.py migrate --settings={SETTINGS} --noinput'.format(SETTINGS=settings))


def restart(domain):
    run('pkill python || true')
    run('touch ~/{DOMAIN}/tmp/restart.txt'.format(DOMAIN=domain))
