ifeq ($(OS),Windows_NT)
PYTHON ?= python
else
PYTHON ?= python3
endif

.PHONY: help run test check

help:
	@printf '%s\n' \
		'run    Run the Tkinter application' \
		'test   Run automated tests' \
		'check  Run the main local verification suite'

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m unittest discover -s tests

check: test
