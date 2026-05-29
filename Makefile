ifeq ($(OS),Windows_NT)
PYTHON ?= python
else
PYTHON ?= python3
endif

.PHONY: help run test build-lib check

help:
	@printf '%s\n' \
		'run    Run the Tkinter application' \
		'test   Run automated tests' \
		'build-lib  Build the reusable dealership core package' \
		'check  Run the main local verification suite'

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m unittest discover -s tests

build-lib:
	$(PYTHON) -m build --wheel --no-isolation

check: test
