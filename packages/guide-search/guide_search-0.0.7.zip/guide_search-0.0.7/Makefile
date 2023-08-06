.PHONY: clean-pyc clean-build

test:
	@py.test --cov=guide_search unit_tests


clean: clean-build clean-pyc


clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
	@rm -fr cover/
	@rm -fr test-reports


clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

dist:
	@python setup.py sdist

publish:
	@twine upload dist/*
