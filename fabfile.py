import os
import json
from fabric.api import task, local

region   = '<YOUR_AWS_REGION>'
image    = '<YOUR_IMAGE_NAME>' # ex: pinktest:latest
account  = '<YOUR_AWS_ACCOUNT>'
endpoint = f'{account}.dkr.ecr.{region}.amazonaws.com/{image}'
environments = {
	'staging'   : '<YOUR_STAGING_EB_ENVIRONMENT>',
	'production': '<YOUR_PRODUCTION_EB_ENVIRONMENT>'
}


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
	print(f'tagging {image}...')
	local(f'docker tag {image} {endpoint}')
	print(f'tagged image: {endpoint}')
	local(f'docker push {endpoint}')

'''
Deploys using eb deploy, requires the correct .elasticbeanstalk/config.yml
and a Dockerrun.aws.json file. Make sure you are in your aws cli environment
This generates an Dockerrun.aws.json file that is the sole file uploaded using eb
'''
@task
def eb(spec):
	dockerrun_dict = {
		'AWSEBDockerrunVersion': '1',
		'Image': {
			'Name': endpoint,
			'Update': 'true'
		},
		'Ports': [
			{
				'ContainerPort': '80'
			}
		],
		'Logging': '/var/log/nginx'
	}
	with open('Dockerrun.aws.json', 'w') as f:
		f.write(json.dumps(dockerrun_dict, indent=4))

	e = environments[spec]
	print(f'Calling eb deploy for {e}')
	awk = 'awk \'{print $3}\''
	v = local(f'eb status {e} | grep \'Deployed Version\' | {awk}', capture=True)
	v_new = input(f'Current running version is {v}. Specify new version: ')
	local(f'eb deploy -l {v_new} {e}')

	local('rm Dockerrun.aws.json')


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

