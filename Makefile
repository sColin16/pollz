init:
	pip install -r requirements.txt
	python app/setupdb.py

run:
	python app/app.py

run-prod:
	python app/setupdb.py
	python app/app.py

test:
	coverage run tests/test_basics.py 
	coverage report --omit=venv/*,tests/*
	coverage html --omit=venv/*,tests/*

lint-basic:
	pycodestyle app tests
	
lint-advanced:
	pycodestyle app tests
	pylint app tests
