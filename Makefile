ifeq ($(OS),Windows_NT)
PYTHON ?= python
VENV_PYTHON ?= .venv/Scripts/python.exe
else
PYTHON ?= python3
VENV_PYTHON ?= .venv/bin/python
endif

.PHONY: help run test setup install-build-tool build-lib check docs coverage compose-check compose-down clean

help:
	@printf '%s\n' \
		'help                Show available commands' \
		'setup               Create .venv and install local build tooling' \
		'run                 Run the Tkinter application' \
		'test                Run automated tests' \
		'check               Run the main local verification suite' \
		'install-build-tool  Install standard Python build tooling into .venv' \
		'build-lib           Build the reusable dealership core package' \
		'docs                Check documentation and editable diagram sources' \
		'coverage            Generate test coverage report' \
		'compose-check       Run Docker/Compose non-GUI verification' \
		'compose-down        Stop Docker/Compose verification stack' \
		'clean               Remove generated local artifacts'

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m unittest discover -s tests

setup: install-build-tool

install-build-tool:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install "build>=1.2" "setuptools>=68" "coverage>=7.5"

build-lib:
	$(PYTHON) -c "import shutil; from pathlib import Path; [shutil.rmtree(p, ignore_errors=True) for p in ['build', 'dealership_core.egg-info']]; [p.unlink() for p in Path('.').rglob('.DS_Store') if '.git' not in p.parts]; print('Prepared clean package build state')"
	$(VENV_PYTHON) -c "import build, setuptools" || (echo "Missing build tooling. Run: make setup" && exit 1)
	$(VENV_PYTHON) -m build --wheel --no-isolation

docs:
	$(PYTHON) -c "from pathlib import Path; import xml.etree.ElementTree as ET; docs=['README.md','docs/specification.md','docs/architecture.md','docs/developer-guide.md','docs/traceability.md','docs/diagrams/README.md']; dbml_sources=['docs/diagrams/schema.dbml']; exports=['docs/diagrams/exports/idefA-0_context.png','docs/diagrams/exports/idefA0_decomposition.png','docs/diagrams/exports/idefA4_decomposition.png','docs/diagrams/exports/use-cases.png','docs/diagrams/exports/app-startup-sequence.png','docs/diagrams/exports/sales-sequence.png','docs/diagrams/exports/schema.png']; missing=[p for p in docs+dbml_sources+exports if not Path(p).exists()]; diagrams=sorted(Path('docs/diagrams').glob('*.drawio.xml')); [ET.parse(p) for p in diagrams]; assert len(diagrams) >= 6, 'Expected at least 6 editable diagram XML files'; dbml=Path('docs/diagrams/schema.dbml').read_text(encoding='utf-8'); tables=['clients','suppliers','employees','cars','sales','reservations','service_orders','test_drives']; missing_tables=[t for t in tables if f'Table {t}' not in dbml]; assert not missing_tables, 'Missing DBML tables: '+', '.join(missing_tables); assert dbml.count('Ref: ') >= 11, 'Expected DBML foreign key references'; assert not missing, 'Missing documentation files: '+', '.join(missing); print('Checked', len(docs), 'documentation files,', len(diagrams), 'Draw.io sources,', len(dbml_sources), 'DBML sources and', len(exports), 'diagram exports')"

coverage:
	$(VENV_PYTHON) -c "import coverage" || (echo "Missing coverage tooling. Run: make setup" && exit 1)
	$(VENV_PYTHON) -m coverage run --source=app,packages -m unittest discover -s tests
	$(VENV_PYTHON) -m coverage report
	$(VENV_PYTHON) -m coverage xml

compose-check:
	docker compose -f infra/compose.yaml run --build --rm checks

compose-down:
	docker compose -f infra/compose.yaml down

clean:
	$(PYTHON) -c "import shutil; from pathlib import Path; paths=['build','dist','dealership_core.egg-info','data','contracts','.pytest_cache','.mypy_cache','.ruff_cache','htmlcov']; [shutil.rmtree(p, ignore_errors=True) for p in paths]; [shutil.rmtree(p, ignore_errors=True) for p in Path('.').rglob('__pycache__')]; [p.unlink(missing_ok=True) for p in [Path('.coverage'), Path('coverage.xml')]]; print('Removed generated local artifacts')"

check: test
