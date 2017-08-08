import os
from fabric.api import task, local

region = "us-east-1"
production_image = "instigate_manager:latest"
endpoint = "329161652620.dkr.ecr.us-east-1.amazonaws.com/manager:latest"
production_env = 'instigate-manager'
staging_env = 'instigate-manager-staging'

'''
push to production
'''
@task
def make(spec=False):
	login()
	build(spec)
	push()
	clean()
	eb(spec)

'''
shorthand for running server
'''
@task
def start(spec=False):
	if spec == 'gunicorn':
		local('gunicorn --workers=1 --log-level=DEBUG --bind 0.0.0.0:6000 server.wsgi_testing:application')
	else:
		local('python manage.py runserver 0.0.0.0:6000 --settings="settings.test_dev"')

'''
If AWS not letting you push, execute this from your aws cli environment.
Gets login and executes resulting output
'''
@task
def login():
	local(local("aws ecr get-login --region {} --no-include-email".format(region), capture=True))

'''
Build the single image using the only Dockerfile
'''
@task
def build(spec=False):
	if spec == 'production':
		local("docker build -t {} -f Dockerfile.prod .".format(production_image))
		local("docker tag {} {}".format(production_image, endpoint))

	else:
		local("docker build -t {} -f Dockerfile .".format(production_image))
		local("docker tag {} {}".format(production_image, endpoint))

'''
Tags image for aws ecs repository then pushes to that repository.
'''
@task
def push():
	local("docker push {}".format(endpoint))

'''
Removes old images with "none" tag, cleans up your docker images
'''
@task
def clean():
	local("docker rmi -f $(docker images | grep none | awk '{print $3}')")

'''
Deploys using eb deploy, requires the correct .elasticbeanstalk/config.yml
and a Dockerrun.aws.json file. Make sure you are in your aws cli environment
'''
@task
def eb(spec=None):
	if spec == 'production':
		v = local("eb status {}".format(production_env), capture=True).split("\n")[3].split(":")[1].strip().split("-")
		v_new = "{}.{}.{}".format(v[0], v[1], str(int(v[2]) + 1))
		v_new = 'P-D2-3'
		local('eb deploy -l {} {}'.format(v_new, production_env))

		# python 3.6.1: local(f'eb deploy -l {v_new} {production_env}')

	else:
		v = local("eb status {}".format(staging_env), capture=True).split("\n")[3].split(":")[1].strip().split("-")
		v_new = "{}-{}-{}".format(v[0], v[1], str(int(v[2]) + 1))
		local("eb deploy -l {} {}".format(v_new, staging_env))

