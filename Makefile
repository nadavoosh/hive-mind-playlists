style:
	python $(shell which pylint) lib tests -f colorized -r n

test:
	python $(shell which nosetests) --where=tests --verbosity=2 --rednose
