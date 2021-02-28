# IN PROGRESS
# INSTALL DOCKER APP FOR EXECUTING THIS - https://docs.docker.com/docker-for-mac/install/
# We are directing docker to select python 3.7 version. It installs the specified version if you don't have already
FROM python:3.7
# Add requirements.txt to docker work directory
ADD requirements.txt /
# Pick up the requirements.txt added to docker work directory and execute it. This downloads all dependencies of required version
RUN pip3 install -r requirements.txt

# Running the HWR web app
# Add entire hwr web app folder to docker work directory
ADD web_app /
# Add CNN model to docker work directory
ADD CNN /CNN
# Add preprocessing folder to docker work directory
ADD preprocessing /preprocessing
# Add unicode folder to docker work directory
ADD Unicode /Unicode
# Add main.py to docker work directory
ADD main.py /

# Execute manage.py
CMD [ "python3", "./hwrkannada/manage.py" ]
# Migrate any db changes if needed
CMD [ "python3", "./hwrkannada/manage.py", "migrate" ]
# Once all db changes are migrated and applied, start the server
CMD [ "python3", "./hwrkannada/manage.py", "runserver", "0.0.0.0:8000" ]

# Executing and Running this docker file -
#   The following builds docker image based on the commands specified in this file
#     1. docker build -t python-hwrapp .
#   The following runs the docker image built in previous step
#     2. docker run -p 8000:8000 python-hwrapp
# Your app should now be available at http://localhost:8000/hwrapp/

# Stop and remove docker
#   Find process docker image
#       1. docker ps
#   Stop docker
#       2. docker stop CONTAINER_ID (select CONTAINER_ID match IMAGE name python-hwrapp)
#   Remove docker
#       3. docker rm CONTAINER_ID
