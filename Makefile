init:
	pip3 install -r requirements.txt

get-key:
	cat /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_-' | head -c 50; echo

run:
	export FLASK_APP=pollz.py; python3 -m flask run

run-prod:
	export FLASK_APP=pollz.py; python3 -m flask run -h '0.0.0.0' -p $(PORT)

test:
	coverage run tests/test_*.py 
	coverage report
	coverage html

lint-basic:
	pycodestyle app tests
	
lint-advanced:
	pycodestyle app tests
	pylint app tests
