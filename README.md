
# Pollz

![Build Status](https://travis-ci.org/sColin16/pollz.svg?branch=master)
[![codecov](https://codecov.io/gh/sColin16/pollz/branch/master/graph/badge.svg)](https://codecov.io/gh/sColin16/pollz)

Pollz is an open source survey and polling web application, built using Flask. The goal is to host fun and simple polls that are effortless to create.

## Getting started
Interested in making modifications, or playing with the app? Follow these instructions:

### Getting the code

**Create your local fork**
1. Click the "Fork" button to create your own copy of the repository
2. Inside your fork, click the "Clone or Download" button, and copy the link
3. In a terminal type `git clone` followed by the link you just copied:
```
git clone https://github.com/<username>/pollz.git
```
4. Enter the repository directory:
```
cd pollz
```

**Configure git to sync local fork with original repository**
1. In the same terminal, within your local fork of the repository, type `git remote add upstream` followed by the link of the original repository (not your fork):
```
git remote add upstream https://github.com/sColin16/pollz.git
```
2. Verify both remotes now exist:
```
git remote -v
```
and make sure you see labels that say both `origin` and `upstream`

**Congrats, you've downloaded the code!** :tada:

*All of the following instructions assume you are within the root of repository directory*

### Prerequisites

For the dev configuration, postgresql and sqlite (only for testing) are used. If not already installed, install both with
```
sudo apt-get install sqlite postgresql
```
or a similar command

If you plan to use the dev instance within a virtualenv (which is highly recomended):
```
pip3 install virtualenv
```

### Installing
1. Create a virtualenv
```
pyhton3 -m virtualenv venv
source venv/bin/activate
```

2. Install the python packages:
```
make init
```

3. Set the FLASK_APP variable
```
export FLASK_APP=pollz.py
```

4. Run the dev server:
```
flask run
```

5. Head to localhost:5000 in your browser to interact with the dev server.

**If everything seems to have worked, you're ready to develop** :tada:

## Contributing
Coming Soon...
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the process of making changes, and submitting pull requests.

## Running the tests

### To run the test suite
```
make test
```
This command will run the unit tests, and generate a coverage report both in the command line, and as an html folder, called htmlcov. If you're interested in viewing the html coverage report open htmlcov/index.html.
These tests must pass in order for the Travis CI build to succeed

### To run the linters

**To run basic linting**
```
make lint
```
This command will use the `pycodestyle` tool to test stylistic elements of the app code, and the test code.
This linting must pass (i.e. not show any error messages) for the Travis CI build to succeed

**To run thorough linting**
```
make lint advanced
```
In addition to running basic linting, this command will use `pylint` to perform a thorough linting of the code.
This linting is not required to pass the Travis CI check (since it can discourage development - especially in early stages). However, it is recomended that some effort is put into minimizing the errors from this lint.

## Deployment
The production version of pollz is run on the Heroku Cloud. You can deploy your copy to Heroku like any other app (as long as Postresql is included as an add on), with a few basic modifications.

run `make get-key` to get a randomly generated secret key for production

Within the app dashboard, click "Settings" and "Reveal Config Vars"

Add the following variables for the app to function:

```
APP_MODE prod
FLASK_APP pollz.py
SECRET_KEY <result of 'make get-key'>
```

A full tutorial for deploying on Heroku is coming soon

## Built With
* [Flask](http://flask.pocoo.org/) - The web development framework

## Contributors

* **Colin Siles**

Any contributions to the project, whether code or a bug report will get your name added to the list!
See also the list of [contributors](https://github.com/sColin16/pollz/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
