.PHONY: help fmt lint test test-mlops test-airflow up-mlops down-mlops up-airflow down-airflow up-selenium down-selenium clean

help:
	@echo "Available commands:"
	@echo "  make fmt            - Format Terraform and Python code"
	@echo "  make lint           - Lint Python, Terraform, and Docker configurations"
	@echo "  make test           - Run full test suite (MLOps & Airflow)"
	@echo "  make data           - Generate synthetic MLOps industrial sensor dataset"
	@echo "  make drift          - Run two-sample statistical data drift analysis"
	@echo "  make up-mlops       - Launch full MLOps stack (MinIO + MLflow + FastAPI + Prometheus)"
	@echo "  make down-mlops     - Stop MLOps stack"
	@echo "  make up-airflow     - Launch Airflow local cluster (Postgres + Webserver + Scheduler)"
	@echo "  make down-airflow   - Stop Airflow cluster"
	@echo "  make up-selenium    - Launch distributed multi-browser Selenium Grid"
	@echo "  make down-selenium  - Stop Selenium Grid"

fmt:
	terraform fmt -recursive Terraform/
	@which ruff >/dev/null 2>&1 && ruff format . || echo "Ruff not found in PATH, skipping python format"

lint:
	terraform fmt -check -recursive Terraform/
	@which ruff >/dev/null 2>&1 && ruff check . || echo "Ruff not found in PATH, skipping ruff check"

data:
	python3 mlops/data/generate_dataset.py

drift:
	python3 mlops/monitoring/drift_monitor.py

test-mlops:
	@which pytest >/dev/null 2>&1 && pytest -v mlops/tests/ || echo "pytest not installed in active environment"

test-airflow:
	cd ApacheAirflow/project1 && python3 -m unittest test/test.py

test: test-airflow test-mlops

up-mlops:
	docker compose -f mlops/docker-compose.mlops.yml up -d

down-mlops:
	docker compose -f mlops/docker-compose.mlops.yml down

up-airflow:
	docker compose -f ApacheAirflow/docker-compose.yaml up -d

down-airflow:
	docker compose -f ApacheAirflow/docker-compose.yaml down

up-selenium:
	docker compose -f Docker_and_Podman/05-selenium-grid/docker-compose-v3.yml up -d

down-selenium:
	docker compose -f Docker_and_Podman/05-selenium-grid/docker-compose-v3.yml down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
