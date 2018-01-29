
# Pollz

![Build Passing](https://travis-ci.org/sColin16/pollz.svg?branch=master)

Pollz is an open source survey and polling web application, built using Flask. The goal is to host fun and simple polls that are effortless to create.

## Getting Started

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
1. Navigate to the [original repository](https://github.com/sColin16/pollz)
2. Click the "Clone or Download" button, and copy the link, as before
3. In the same terminal, within your local fork of the repository, type `git remote add upstream` followed by the link you just copied:
```
git remote add upstream https://github.com/sColin16/pollz.git
```
4. Verify both remotes now exist:
```
git remote -v
```
and make sure you see labels that say both `origin` and `upstream`

**Congrats, you've downloaded the code!** :tada:

### Prerequisites

For the dev configuration, sqlite is used. If not already installed install it with
```
sudo apt-get install sqlite3
```
or a similar command

### Installing

Many commands are abstracted into the Makefile, for easier typing

Install the python packages:
```
make init
```

Run the dev server:
```
make run
```

And head to [localhost:5000] in your browser to ineract with the dev server.

**If everything seems to have worked, you're ready to develop** :tada:

## Running the tests

Explain how to run the automated tests for this system
Coming soon...

### Break down into end to end tests

Explain what these tests test and why
Coming soon...

```
Give an example
```

### And coding style tests

Explain what these tests test and why
Coming soon...
```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system
Coming soon...

## Built With
Coming soon...

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.
Coming Soon...

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
