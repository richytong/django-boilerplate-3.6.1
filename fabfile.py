import os
from fabric.api import task, local

account  = 'youraccount'
region   = 'us-east-1'
image    = 'pinktest:latest'
endpoint = f'{account}.dkr.ecr.{region}.amazonaws.com/{image}'


####################################################################################
################################## BUILD TASKS #####################################
####################################################################################
'''
Build the single image using the only Dockerfile
required_args: spec -- {'staging', 'production'}, specify which settings to use
'''
@task
def build(spec):
	assert spec in {'staging', 'production'}
	spec = 'config.settings.' + spec
	local(
		'docker build' + 
		' -t ' + image +
		' -f Dockerfile' +
		' --build-arg DJANGO_SETTINGS_MODULE=' + spec +
		' .'
	)

'''
Removes old images with 'none' tag, cleans up your docker images
'''
@task
def clean():
	try:
		local('docker rmi -f $(docker images | grep none | awk \'{print $3}\')')
	except:
		print('No images removed, exiting')


####################################################################################
################################# DEPLOYMENT TASKS #################################
####################################################################################
'''
If AWS not letting you push, execute this from your aws cli environment.
Gets login and executes resulting output
'''
@task
def login():
	local(
		'$(' +
		'aws ecr get-login' +
		' --region ' + region +
		' --no-include-email' +
		')'
	)

'''
Tags image for aws ecs repository then pushes to that repository.
'''
@task
def push():
	local(f'docker push {endpoint}')

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


####################################################################################
################################### RUN TASKS ######################################
####################################################################################
'''
start the server inside the docker container
'''
@task
def start(spec=None):
	if spec == 'dev':
		local('python src/manage.py runserver')
	if spec == 'bash':
		try:
			local(f'docker run -it {image} /bin/bash')
		except:
			print(f'Unable to find {image}, please check the image')
	else:
		try:
			local(f'docker run -p 80:80 {image}')
		except:
			print(f'Unable to find {image}, please check the image')

'''
stop the container running latest image
'''
@task
def stop():
	try:
		local('docker stop $(docker ps | grep ' + image + ' | awk \'{print $1}\')')
	except:
		print(f'No processes with {image} to stop, exiting')

'''
attach to the container running the latest image, run bash
need to have started it already
'''
@task
def attach():
	try:
		local('docker exec -it $(docker ps | grep ' + image + ' | awk \'{print $1}\') /bin/bash')
	except:
		print(f'No processes with {image} to attach, exiting')

