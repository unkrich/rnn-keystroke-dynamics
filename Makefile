init:
	virtualenv -p python3 venv
	source venv/bin/activate
	pip3 install -r requirements.txt

run:
	# source venv/bin/activate
	python3 model/main.py

test:
	# source venv/bin/activate
	nosetests tests