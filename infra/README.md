# Container Verification

This project is a Tkinter desktop application, so the graphical interface is launched locally with `make run`.

Docker and Compose are used for reproducible non-GUI checks:

```bash
docker build -t car-dealership-checks:local .
docker run --rm car-dealership-checks:local
docker compose -f infra/compose.yaml run --rm checks
docker compose -f infra/compose.yaml down
```

The container runs the automated tests and builds the reusable `dealership_core` wheel without opening the GUI.

The image uses full `python:3.11` instead of `python:3.11-slim`. The checks do not open a GUI window, but the test suite imports application modules that import `tkinter`; the slim image does not include the Tk libraries required for those imports.

Compose uses the default command from the Dockerfile, so the non-GUI verification command has a single source of truth.
