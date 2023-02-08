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

PLONE6=6.0-latest

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

CODE_QUALITY_VERSION=2.0.2
ifndef LOG_LEVEL
	LOG_LEVEL=INFO
endif
CURRENT_USER=$$(whoami)
USER_INFO=$$(id -u ${CURRENT_USER}):$$(getent group ${CURRENT_USER}|cut -d: -f3)
LINT=docker run --rm -e LOG_LEVEL="${LOG_LEVEL}" -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} check
FORMAT=docker run --rm --user="${USER_INFO}" -e LOG_LEVEL="${LOG_LEVEL}" -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} format

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U pip wheel

.PHONY: install-plone-6.0
install-plone-6.0: bin/pip ## Install Plone 6.0
	@echo "$(GREEN)==> Install with Plone 6.0$(RESET)"
	bin/pip install Plone -c https://dist.plone.org/release/$(PLONE6)/constraints.txt
	bin/pip install -e ".[test]"
	bin/mkwsgiinstance -d . -u admin:admin

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

.PHONY: clean
clean: ## Remove old virtualenv and creates a new one
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf bin lib lib64 include share etc var inituser pyvenv.cfg .installed.cfg
	rm -rf frontend/dist frontend/node_modules

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi etc/zope.ini

.PHONY: format-frontend
format-frontend: ## Format frontend codebase
	@echo "$(GREEN)==> Format frontend codebase$(RESET)"
	(cd frontend && pnpm lint:fix)
	(cd frontend && pnpm prettier:fix)

.PHONY: format
format: ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	$(FORMAT)
	make format-frontend

.PHONY: lint-frontend
lint-frontend: ## Lint frontend codebase
	@echo "$(GREEN)==> Lint frontend codebase$(RESET)"
	(cd frontend && pnpm lint)
	(cd frontend && pnpm prettier)

.PHONY: lint
lint: ## check code style
	$(LINT)
	make lint-frontend

.PHONY: lint-black
lint-black: ## validate black formating
	$(LINT) black

.PHONY: lint-flake8
lint-flake8: ## validate black formating
	$(LINT) flake8

.PHONY: lint-isort
lint-isort: ## validate using isort
	$(LINT) isort

.PHONY: lint-pyroma
lint-pyroma: ## validate using pyroma
	$(LINT) pyroma

.PHONY: lint-zpretty
lint-zpretty: ## validate ZCML/XML using zpretty
	$(LINT) zpretty

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
test: ## run tests
	bin/pytest --disable-warnings
