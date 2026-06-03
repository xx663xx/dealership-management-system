# Container Verification

This project is a Tkinter desktop application, so the graphical interface is launched locally with `make run`.

Docker and Compose are used for reproducible non-GUI checks:

```bash
docker build -t car-dealership-checks:local .
docker run --rm car-dealership-checks:local
docker compose -f infra/compose.yaml run --rm checks
```

The container runs the automated tests and builds the reusable `dealership_core` wheel without opening the GUI.
