import os
import sys

INTERP = '/home/{{USER}}/.virtualenv/{{PROJECT_NAME}}/bin/python'
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '/home/{{USER}}/{{PROJECT_NAME}}/source')

import newrelic.agent
newrelic.agent.initialize('/home/{{USER}}/{{DOMAIN}}/newrelic.ini')
os.environ['DJANGO_SETTINGS_MODULE'] = '{{SETTINGS}}'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
application = newrelic.agent.wsgi_application()(application)
