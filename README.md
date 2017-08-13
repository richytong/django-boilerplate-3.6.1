Django Boilerplate for Python 3.6.1
===================================

This Django Boilerplate quickly encapsulates your source code in a Docker container running Gunicorn behind an Nginx reverse proxy. This project uses Fabric3 to handle most of the deployment and administration tasks.

![container-diagram.png](/container-diagram.png?raw=true)

Prerequisites
-------------
pip - You can install pip with [Homebrew](https://brew.sh/)
	
	brew install pip

I recommend you use [pyenv](https://github.com/pyenv/pyenv) to manage your versions of python as well as any dependencies installed by pip.

	brew install pyenv pyenv-virtualenv

Docker - Install docker [here](https://docs.docker.com/engine/installation/)

Setup
-----
	pip install -r requirements.txt

You configure
-------------
[installed apps](https://github.com/richytong/django-boilerplate-3.6.1/tree/master/src/config/settings/__init__.py) - /src/config/settings/__init__.py

	You can find your installed apps in INSTALLED_APPS.
	When you add a Django app, remember to specify it here.

[project-wide credentials and keys](https://github.com/richytong/django-boilerplate-3.6.1/blob/master/src/config/settings/defaults/credentials.py) - /src/config/settings/defaults/credentials.py

	Place credentials for any external services used here.
	For example: APIAI_CLIENT_ACCESS_TOKEN = 'alsdfalsjlakjf'

[database declaration](https://github.com/richytong/django-boilerplate-3.6.1/blob/master/src/config/settings/defaults/database.py) - /src/config/settings/defaults/database.py

	Specify your database configurations in DATABASES. Default here is sqlite but
	it is highly recommended to use a relational database like PostGresQL.

[settings modules](https://github.com/richytong/django-boilerplate-3.6.1/tree/master/src/config/settings) - /src/config/settings/

	Your deployment-specific settings. Ensure DB_MAIN corresponds to keys you specified in
	database.py DATABASES. DB_MAIN specifies the database used by the different deployments
	{'test_dev', 'staging', 'production'} of your application. This is convenient for
	isolated deployments of your application at the data layer, but you can also point
	DB_MAIN to the same database for all deployments of your application.

[Fabric3](https://github.com/richytong/django-boilerplate-3.6.1/blob/master/fabfile.py) - /fabfile.py

	Fabric is a simple, Pythonic tool for remote execution and deployment. It is more powerful
	than a simple bash script or Makefile. Read more [here](https://github.com/mathiasertl/fabric/).

		region       - Region on AWS hosting your servers

		image        - Title of your image. This follows the format __name__:__version__.
		               Version defaults to 'latest'
		
		account      - Your AWS account. This is given to you when you created your account with AWS
		               and is necessary to log in to the AWS console.
		
		endpoint     - AWS path representation of your AWS docker repository.
		               Images are pushed here and tagged as this.

		environments - Dictionary mapping {'staging, 'production'} to the environments you
		               created on the AWS console.


Build your project
------------------
Start adding apps to the src directory.

	python src/manage.py startapp __your_custom_app__


Run your project locally
------------------------
This is shorthand for python src/manage.py runserver

	fab start:dev

Run a container locally
-----------------------
Build the Docker image. You must specify which deployment {'staging', 'production'} to build.
Here we build a staging image.

	fab build:staging

Clean up old images. If this is your first build you will not need to use this.

	fab clean

Run your container. The container will run on port 80 by default. You can find your project on
http://localhost/. Check static files are serving correctly with http://localhost/admin
(if it is ugly, something went wrong)

	fab start

Optionally, attach to your running container and run bash at your leisure. You can exit your
container at any time using `exit`

	fab attach

Ctrl + c does not stop your container so it will run in the background unless you stop it manually.

	fab stop

Deploy your project to AWS Elastic Beanstalk
--------------------------------------------
Login to AWS

	fab login

Transfer your Docker image to the AWS repository

	fab push

Use eb cli to deploy your project for a specified deployment {'staging', 'production'}. If this is your first deployment you must run `aws configure` and `eb config` and supply the necessary arguments and credentials.
This command also generates the Dockerrun.aws.json file needed for AWS Elastic Beanstalk deployment

	fab eb:staging

References
----------
http://kimh.github.io/blog/en/docker/gotchas-in-writing-dockerfile-en/
https://medium.com/@rohitkhatana/deploying-django-app-on-aws-ecs-using-docker-gunicorn-nginx-c90834f76e21
https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04
https://docs.docker.com/engine/reference/builder/
https://github.com/moby/moby/issues/6822#issuecomment-168170031
https://www.twoscoopspress.com/products/two-scoops-of-django-1-8
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html


