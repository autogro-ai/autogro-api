# Set base image (host OS)
FROM python:3.12-alpine

# By default, listen on port 5010
EXPOSE 5010/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Copy the content of the local src directory to the working directory
COPY ./*.py .
COPY ./.env .
COPY resources/ ./resources
COPY tools/ ./tools 

# Install any dependencies
RUN pip install -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "./app.py" ]