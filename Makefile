init:
	pip3 install -r requirements.txt

get-key:
	cat /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_-' | head -c 50; echo

clean-pyc:
	find . -name '*.pyc'
	find . -name '*.pyc' -delete

run:
	flask run

run-prod:
	flask run -h '0.0.0.0' -p $(PORT)

test:
	coverage run tests/test_*.py 
	coverage report
	coverage html

lint:
	pycodestyle app tests config.py pollz.py
	
lint-advanced:
	pycodestyle app tests config.py pollz.py
	pylint app tests config.py pollz.py
