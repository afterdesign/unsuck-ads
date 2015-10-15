SHELL 				:= /bin/bash
VENV_DIRECTORY_NAME := "venv"
PYTHON_USER_BASE := $(shell python -m site --user-base)

#COLORS
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RED	   := $(shell tput -Txterm setaf 1)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

install_virtualenv = \
	@pip install --user virtualenv -U

setup_venv = \
	@$(PYTHON_USER_BASE)/bin/virtualenv -p python2.7 $(VENV_DIRECTORY_NAME); \
	source venv/bin/activate; \
	pip install -r requirements

cleanup = \
	@rm -rf venv; \
	find . -name "*.pyc" -delete

help:
	@echo -e "${YELLOW}init:${RESET}\n initialize project"

init:
	$(call install_virtualenv)
	$(call setup_venv)

clean:
	$(call cleanup)

.PHONY: init help clean
