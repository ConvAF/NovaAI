# Nova AI

![CI](https://github.com/ConvAF/NovaAI/actions/workflows/build.pipeline.yml/badge.svg)
![Coverage badge](tests/coverage-badge.svg)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

<a href="https://www.loom.com/share/50b3de2c86054ed5a6115247818ab293">
    <p>See a Loom Demo of NovaAI here</p>
    <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/50b3de2c86054ed5a6115247818ab293-with-play.gif">
  </a>

Try out Nova at:

http://nova-ai.net/ (Udpate: no longer active)

## Overview

Nova is an application that uses conversational AI for language learning to help users gain fluency in their target language (work in progress).

Users can chat with Nova, practice specific scenarios, and track their learning progress.

Features:

- A language learning website implemented Flask
- Chats with a conversational AI powered by GPT-3
- Grammar correction and other learning features

## Usage

### Installation

The package uses `python3.9`.

First clone the repo:

```bash
git clone git@github.com:ConvAF/NovaAI.git
cd chatbot
```

It is recommended to also set up and activate a
virtual environment, for example using

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Then, install the application and dependencies as a package in development mode using

```bash
make install
```

which is equivalent to running

```bash
pip install -e .
```

which installs the application as a package in developer (local edit) mode.

### Configuration

Create a file `.env` at the project root (if it doesn't exist yet)
and specify the following variables before running the application:

Several variables are stored in the `.env` file and should be configured
before running the application:

- `OPENAI_API_KEY`: The api key for OpenAi.
- `OPENAI_ENGINE`: Which GPT-3 engine to use. For testing, a simpler engine is used. Can be one of: ada (cheapest), babbage, curie, davinci (most expensive, most powerful)

### Running the application

Before running the application, initialize the user database

```bash
flask init-db
```

Start the application from the root project directory using

```bash
flask run
```

If the application is installed, you can also start
it from anywhere using

```bash
export FLASK_APP=chatbot
flask run
```

## Deployment

### Deploying on AWS EC2

This describes how to deploy the app on an AWS EC2 instance using docker.

First clone the repo:

```bash
git clone git@github.com:ConvAF/NovaAI.git
cd chatbot
```

Then build the image using

```bash
docker build . --tag chatbot
```

To run the app (and keep running in background), start the container as

```bash
docker run -d chatbot:latest
```

Be sure that the correct port (80 by default) is exposed on your instance such that the application is accessible from the outside (see notes below).

# Developer Notes

### Useful commands

- `flask run`: Run the application.
- `flask init-db`: Initialize the database.
- `flask shell`: Start an interactive Python shell in the application context, with an app instance imported

## Testing

### Running Unit Tests

You can run tests using

```bash
pytest
```

Add the `-v` flag to show the result for each test function.

To measure the code coverage of the tests, use the `coverage` command:

```bash
coverage run -m pytest
```

You can view the coverage report using

```bash
coverage report
# or
coverage html
```

### Testing in the Flask shell

The flask application can also be tested from the shell.

Start the shell with

```bash
flask shell
```

In the shell, you can test endpoints like so:

```python
>>> client = app.test_client()
>>> client.get('/')
<WrapperTestResponse streamed [200 OK]>
>>> client.post(
      '/auth/register',
      data={'username': username, 'password': password}
    )
```

### Load testing with locust

To test the application under user traffic, do

```bash
cd tests/
locust
```

which will open a dashboard at `http://0.0.0.0:8089/`. There you can simulate users retrieving different endpoints. More complex fuctionality can be added in `tests/locustfile.py`.

### Profiling with py-spy

To profile the app, first get the process id (`pid`) of the running flask app, for example using

```bash
ps | grep flask
```

Then you can record the app's activity using

```bash
py-spy record -o profile.svg --pid <pid>
```

You can interact with the app for a while (or run a `locust` load test), after a while stop the `py-spy` process, which will save a flame graph of the apps activity.

### Notes on manual deployment on AWS EC 2

The following outlines some steps if not using `docker` as described above

#### Installing pytorch

We encountered a bug when installing `pytorch` on an AWS EC2 instance, where the installation with `pip` did not finish. To circumvent this, use

```bash
pip install --no-cache-dir torch
```

or, for all requirements,

```bash
pip install -e . --no-cache-dir
```

#### Serving the app

```bash
waitress-serve --call 'chatbot:create_app'
```

#### Ports on AWS EC2

waitress serves the app on port 8080. To redirect to port 80, use

```bash
sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

### Docker

Docker image is specified in the docker file.

Build the image using

```bash
docker build . --tag chatbot
```

Start the container (and keep running in background)

```bash
docker run -dp 80:80 chatbot:latest
```

For testing, run the container and delete after user with

```bash
docker run -p 80:80 --rm chatbot:latest
```

(ports are not necessary on the server, but on mac you have to specify the ports `8080:80 ` because `80` is already in use).

or in interactive mode to inspect the contents:

```bash
docker run -it --rm chatbot:latest bash
```
