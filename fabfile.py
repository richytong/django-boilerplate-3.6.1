import os
from fabric.api import task, local

region = "us-east-1"
image = "pinktest:latest"
endpoint = "329161652620.dkr.ecr.us-east-1.amazonaws.com/manager:latest"

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
start the server inside the docker container
'''
@task
def start(spec=None):
	if spec == 'local':
		local('python src/manage.py runserver')
	else:
		local('docker run -p 8000:8000 {}'.format(image))

'''
Build the single image using the only Dockerfile
required_args: spec -- {'staging', 'production'}, specify which settings to use
'''
@task
def build(spec):
	spec = 'config.settings.' + spec
	local(
		'docker build' + 
		' -t ' + image +
		' -f Dockerfile' +
		' --build-arg DJANGO_PROJECT_SETTINGS=' + spec +
		' .'
	)

'''
If AWS not letting you push, execute this from your aws cli environment.
Gets login and executes resulting output
'''
@task
def login():
	local(local('''
		aws ecr get-login
			--region {}
			--no-include-email
		'''.format(region), capture=True
	))

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

