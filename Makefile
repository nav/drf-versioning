SHELL := /bin/sh
.DEFAULT_GOAL := help

-include .env
export

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
RUNTIME_ENV?=dev

ifeq (manage,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: help install run repl test
.PHONY: ide/emacs

help:				## Show this help
	@printf "\nUsage: make <command>\n\nThe following commands are available:\n\n"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/ [a-z\/ -]*	//' | sed -e 's/##//'
	@printf "\n"

install: 				## Install dependencies
	@nix-shell --pure --command "poetry install"
	@nix-shell --pure --command "pre-commit install"

run: 					## Run application
	@nix-shell --command "cd src && poetry run python manage.py runserver 0.0.0.0:${PORT}"

shell:				## Start a Python shell
	@nix-shell --command "cd src && poetry run python"

manage:
	@nix-shell --run "cd src && poetry run python manage.py $(RUN_ARGS)"

test:				## Run test suite with coverage report
	@nix-shell --command "poetry run coverage run -m pytest --disable-pytest-warnings -x -v \
	&& poetry run coverage report -m --omit=*test*,/nix/* -i"

##
##- IDE -
ide/emacs:			## Run emacs with Nix
	@nix-shell --command "/opt/homebrew/bin/emacs &>/dev/null &"
