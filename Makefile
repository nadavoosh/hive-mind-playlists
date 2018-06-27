install-deps:
	pip install -r requirements.txt
	python -m nltk.downloader punkt averaged_perceptron_tagger
run:
	python main/__init__.py
style:
	python $(shell which pylint) lib main tests -f colorized -r n
test:
	python $(shell which nosetests) --where=tests --verbosity=2 --rednose
