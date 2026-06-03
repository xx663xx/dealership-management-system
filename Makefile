ifeq ($(OS),Windows_NT)
PYTHON ?= python
else
PYTHON ?= python3
endif

.PHONY: help run test install-build-tool build-lib check

help:
	@printf '%s\n' \
		'run    Run the Tkinter application' \
		'test   Run automated tests' \
		'install-build-tool  Install standard Python build tooling' \
		'build-lib  Build the reusable dealership core package' \
		'check  Run the main local verification suite'

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m unittest discover -s tests

install-build-tool:
	$(PYTHON) -m pip install "build>=1.2" "setuptools>=68"

build-lib:
	$(PYTHON) -c "import build, setuptools" || (echo "Missing build tooling. Run: make install-build-tool" && exit 1)
	$(PYTHON) -m build --wheel --no-isolation

check: test
