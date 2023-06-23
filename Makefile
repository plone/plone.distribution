### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCS_DIR=${BACKEND_FOLDER}/docs

# Python checks
PYTHON?=python3

# installed?
ifeq (, $(shell which $(PYTHON) ))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

# version ok?
PYTHON_VERSION_MIN=3.8
PYTHON_VERSION_OK=$(shell $(PYTHON) -c "import sys; print((int(sys.version_info[0]), int(sys.version_info[1])) >= tuple(map(int, '$(PYTHON_VERSION_MIN)'.split('.'))))")
ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

# Set distributions still in development
DISTRIBUTIONS="default,classic"

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-venv clean-instance clean-frontend ## remove all build, test, coverage and Python artifacts

.PHONY: clean-frontend
clean-frontend: ## Remove frontend dependencies
	rm -rf frontend/dist frontend/node_modules

.PHONY: clean-instance
clean-instance: ## remove existing instance
	rm -fr instance etc inituser var

.PHONY: clean-venv
clean-venv: ## remove virtual environment
	rm -fr bin include lib lib64 env pyvenv.cfg .tox .pytest_cache requirements-mxdev.txt

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

bin/pip bin/tox bin/mxdev:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	$(PYTHON) -m venv .
	bin/pip install -U "pip" "wheel" "cookiecutter" "mxdev" "tox" "pre-commit"
	bin/pre-commit install

.PHONY: config
config: bin/pip  ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	bin/cookiecutter -f --no-input --config-file instance.yaml gh:plone/cookiecutter-zope-instance

.PHONY: install-plone-6.0
install-plone-6.0: config ## pip install Plone packages
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/mxdev -c mx.ini
	bin/pip install -r requirements-mxdev.txt


.PHONY: install-frontend
install-frontend:
	@echo "$(GREEN)==> Install dependencies of the frontend$(RESET)"
	(cd frontend && pnpm i)

.PHONY: install
install: install-plone-6.0 install-frontend ## Install Plone 6.0 and the overview frontend

.PHONY: build-frontend
build-frontend:
	@echo "$(GREEN)==> Build the frontend code$(RESET)"
	(cd frontend && pnpm build)
	(mv frontend/dist/* src/plone/distribution/browser/static/)

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) PYTHONWARNINGS=ignore ./bin/runwsgi instance/etc/zope.ini

.PHONY: format-frontend
format-frontend: ## Format frontend codebase
	@echo "$(GREEN)==> Format frontend codebase$(RESET)"
	(cd frontend && pnpm lint:fix)
	(cd frontend && pnpm prettier:fix)

.PHONY: format
format: bin/tox ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	bin/tox -e format
	make format-frontend

.PHONY: lint-frontend
lint-frontend: ## Lint frontend codebase
	@echo "$(GREEN)==> Lint frontend codebase$(RESET)"
	(cd frontend && pnpm lint)
	(cd frontend && pnpm prettier)

.PHONY: lint
lint: ## check code style
	bin/tox -e lint
	make lint-frontend

# i18n
bin/i18ndude:	bin/pip
	@echo "$(GREEN)==> Install translation tools$(RESET)"
	bin/pip install i18ndude

.PHONY: i18n
i18n: bin/i18ndude ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	bin/update_locale

# Tests
.PHONY: test
test: bin/tox ## run tests
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) bin/tox -e test

.PHONY: test-coverage
test-coverage: bin/tox ## run tests with coverage
	DEVELOP_DISTRIBUTIONS=$(DISTRIBUTIONS) bin/tox -e coverage

# Docs
bin/sphinx-build: bin/pip
	bin/pip install -r requirements-docs.txt

.PHONY: build-docs
build-docs: bin/sphinx-build  ## Build the documentation
	./bin/sphinx-build \
		-b html $(DOCS_DIR) "$(DOCS_DIR)/_build/html"

.PHONY: livehtml
livehtml: bin/sphinx-build  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	./bin/sphinx-autobuild \
		--ignore "*.swp" \
		-b html $(DOCS_DIR) "$(DOCS_DIR)/_build/html"
