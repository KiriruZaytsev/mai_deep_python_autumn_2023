meta:
	python3 meta.py
descriptor:
	python3 descriptor.py
test_meta:
	python3 -m unittest test_meta
test_descriptor:
	python3 -m unittest test_descriptor
lint:
	pylint descriptor.py
	pylint meta.py
coverage:
	coverage run -m unittest discover
	coverage report -m