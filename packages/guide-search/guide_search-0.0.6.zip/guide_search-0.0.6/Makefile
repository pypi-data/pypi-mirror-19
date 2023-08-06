.PHONY: clean-pyc clean-build

test:
	@py.test --junitxml=test-reports/test-results.xml --cov-report term-missing --cov-report xml --cov=guide_ui unit_tests

coverage:
	@rm -f .coverage
	@nosetests --with-coverage --cover-package=guidemd --cover-html

clean: clean-build clean-pyc


clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
	@rm -fr cover/


clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +


publish:
	@twine upload dist/*.tar.gz
	@twine upload dist/*.whl
