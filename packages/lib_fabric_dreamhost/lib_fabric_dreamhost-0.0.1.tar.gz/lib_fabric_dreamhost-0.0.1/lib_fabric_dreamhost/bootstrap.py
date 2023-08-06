# -*- coding:utf-8 -*-
from fabric.api import run, put
from fabric.contrib.files import exists, upload_template
from lib_fabric_dreamhost.helpers import get_filepath, get_templates_folder


def create_virtualenv(project_name):
    virtualenv_path = '~/.virtualenv/{NAME}'.format(NAME=project_name)
    if not exists(virtualenv_path):
        run('mkdir ~/.virtualenv')
        run('virtualenv {PATH}'.format(PATH=virtualenv_path))


def install_bash_it():
    if exists('~/.bash_it'):
        run('~/.bash_it/uninstall.sh')
        run('rm -rf ~/.bash_it')
    run('git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it')
    run('echo "y" | ~/.bash_it/install.sh')
    if exists('~/.bash_profile'):
        run('rm ~/.bash_profile')
    put(get_filepath('.bash_profile'), '~/.bash_profile')


def configure_domain(domain):
    run('mkdir -p ~/{DOMAIN}/public/static'.format(DOMAIN=domain))
    run('mkdir -p ~/{DOMAIN}/tmp'.format(DOMAIN=domain))
    run('mkdir -p ~/logs-app'.format(DOMAIN=domain))


def passenger_wsgi(domain='domain', user='user', project_name='project_name', settings='settings'):
    destination = '~/{DOMAIN}/passenger_wsgi.py'.format(DOMAIN=domain)
    if exists(destination):
        run('rm %s' % destination)
    context = {
        'USER': user,
        'PROJECT_NAME': project_name,
        'DOMAIN': domain,
        'SETTINGS': settings
    }
    upload_template(template_dir=get_templates_folder(), filename='passenger_wsgi.py', destination=destination, context=context, use_jinja=True)


def newrelic(domain='domain', license_key='license_key', project_name='project_name'):
    destination = '~/{DOMAIN}/newrelic.ini'.format(DOMAIN=domain)
    if exists(destination):
        run('rm %s' % destination)
    context = {
        'LICENSE_KEY': license_key,
        'PROJECT_NAME': project_name
    }
    upload_template(template_dir=get_templates_folder(), filename='newrelic.ini', destination=destination, context=context, use_jinja=True)
