#!/usr/bin/make
# Note: gmake syntax
#
# Copyright Bertil Kronlund, 2017 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SHELL  = /bin/bash
PYTHON = python3
CURRENT_DIRECTORY := $(shell pwd)

# Ensure git is installed
GITBIN := $(shell which git)
ifndef GITBIN
$(error Git is not installed, do 'sudo apt-get install git' before proceeding)
endif

help:
	@echo
	@echo "[develop and test]---------------------------------"
	@echo "requirements -- installs the project requirements"
	@echo "develop ------- installs project in develop mode"
	@echo "lint ---------- checks style with flake8"
	@echo "test ---------- run tests with the default $(shell python3 -V)"
	@echo "manifest ------ check completeness of the manifest file"
	@echo "coverage ------ run unit and coverage tests"
	@echo "report -------- run unit test, coverage and creates html report"
	@echo "clean --------- removes all build, test and Python artifacts"
	@echo "[documentation]------------------------------------"
	@echo "html ---------- creates html documentation with sphinx"
	@echo "man ----------- creates man pages with sphinx"
	@echo "[release]------------------------------------------"
	@echo "uninstall ----- removes installed package from Python's site-packages"
	@echo "dist ---------- creates source and binary wheel packages"
	@echo "install ------- installs the package to the active Python's site-packages"
	@echo "install-wheel - installs the wheel binary to Python's site-packages"
	@echo "pypi-test ----- upload source and binary wheel packages to test PyPI"
	@echo "pypi ---------- upload source and binary wheel packages to PyPI"
	@echo

requirements:
	pip install --upgrade -r requirements.txt

develop:
	pip install --editable $(CURRENT_DIRECTORY)

clean: clean-build clean-pyc clean-reports

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-reports:
	rm -fr htmlcov/

html:
	cd docs && sphinx-build -b html . _build/html
	@echo "Documentation build finished. The new HTML pages are in docs/_build/html."

man:
	cd docs && sphinx-build -b man . _build/man
	@echo "Documentation build finished. The new man pages are in docs/_build/man."

# Run final tests in build tree
build: clean
	$(PYTHON) setup.py build
	flake8 build
	green --run-coverage build

lint:
	flake8 modulereport

test: lint
	green -vv modulereport

manifest: clean
	@echo
	@echo "Ensure an initial git repository commit have been done!"
	@echo
	check-manifest

coverage:
	green --run-coverage modulereport

report: coverage
	coverage html
	@echo "Created a new html coverage report in the htmlcov directory"

pypi: dist
	$(PYTHON) setup.py register -r https://pypi.python.org/pypi
	gpg --detach-sign -a $(shell ls -1 dist/*.gz)
	gpg --detach-sign -a $(shell ls -1 dist/*.whl)
	twine upload --skip-existing dist/* -r pypi

pypi-test: dist
	$(PYTHON) setup.py register -r https://testpypi.python.org/pypi
	twine upload --skip-existing dist/* -r test

dist: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

install: dist
	pip install $(shell ls -1 dist/*.gz)

install-wheel: dist
	pip install $(shell ls -1 dist/*.whl)

uninstall: 
	pip uninstall modulereport

.PHONY: requirements develop clean clean-build clean-pyc html man build lint test manifest coverage report pypi pypi-test dist install install-wheel uninstall
