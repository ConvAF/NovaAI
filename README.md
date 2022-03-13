# Chatbot

![CI](https://github.com/franksh/chatbot/actions/workflows/build.pipeline.yml/badge.svg)
![Coverage badge](tests/coverage-badge.svg)

A language learning Chatbot

## Overview

tbd

## Usage

### Installation

First clone the repo:

```bash
git clone git@github.com:franksh/chatbot.git
cd chatbot
```

It is recommended to also set up and activate a
virtual environment, for example using

```bash
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

### Useful commands

- `flask run`: Run the application.
- `flask init-db`: Initialize the database.
- `flask shell`: Start an interactive Python shell in the application context, with an app instance imported

### Testing

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
