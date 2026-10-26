# AGENTS.md — Universal Agent Operating Standard: devops_and_mlops_projects

> **Repository:** `/home/liberprimus/code/devops_and_mlops_projects`  
> **Workspace Authority:** `sudh29` (`liberprimus`)  
> **Tier:** Tier B (Production Infrastructure, Kubernetes & MLOps Architecture)  
> **Active Branch:** `dev`  
> **Applicable Agents:** Antigravity, Claude Code, Cursor, Gemini, Codex


---

## 1. Repository Purpose & Architecture

- **Overview:** `devops_and_mlops_projects` serves as an enterprise reference implementation for cloud infrastructure as code (Terraform), container orchestration (Kubernetes, Docker Compose), distributed data pipelines (Apache Airflow), model lifecycle management (MLflow, MinIO, FastAPI), statistical data drift monitoring, and Selenium Grid testing.
- **Key Directory Map:**
  - `terraform/`: Infrastructure-as-code modules for multi-cloud deployments.
  - `mlops/`: End-to-end MLOps pipeline:
    - `mlops/data/`: Industrial sensor dataset generators.
    - `mlops/monitoring/`: Kolmogorov-Smirnov statistical data drift monitors.
    - `mlops/tests/`: Unit and integration test suites for inference servers.
    - `docker_compose_mlops.yml`: MinIO + MLflow + FastAPI + Prometheus stack.
  - `apache_airflow/`: Production Airflow DAGs, custom operators, and unittests.
  - `Makefile`: Canonical orchestration targets.
- **Architectural Invariants:**
  - **IaC Idempotency:** Terraform configurations must format cleanly (`terraform fmt`) and declare explicit providers.
  - **Zero Unmocked External Cloud Calls:** Automated test suites must run deterministically without requiring live AWS/GCP credentials.
  - **Reproducible Pipelines:** Docker Compose service definitions must expose explicit health checks and volume mounts.

### Key Architecture & Entry Points

- **Build Orchestration:** [`Makefile`](file:///home/liberprimus/code/devops_and_mlops_projects/Makefile)
- **Infrastructure as Code:** [`terraform/`](file:///home/liberprimus/code/devops_and_mlops_projects/terraform/)
- **MLOps Service Stack:** [`mlops/`](file:///home/liberprimus/code/devops_and_mlops_projects/mlops/)
- **Airflow DAGs:** [`apache_airflow/project1/`](file:///home/liberprimus/code/devops_and_mlops_projects/apache_airflow/project1/)

---

## 2. Coding Style & Engineering Conventions

- Terraform: Standard 2-space indentation, explicit type definitions, idiomatic module structure.
- Python: PEP 8 / Ruff compliant with type annotations.
- Docker: Lightweight base images (`alpine` or `slim`), explicit environment flags.

---

## 3. Toolchain & Environment Matrix

- **Tools:** Terraform, Docker, Docker Compose, Python 3.12, Pytest, Ruff
- **Build System:** GNU Make

### Canonical Commands
All commands run from `/home/liberprimus/code/devops_and_mlops_projects`:

| Action | Command | Purpose |
|:---|:---|:---|
| **Run All Tests** | `make test` | Execute both Airflow and MLOps test suites |
| **Test MLOps** | `make test-mlops` | Run pytest across `mlops/tests/` |
| **Test Airflow** | `make test-airflow` | Run unittest suite for Airflow DAGs |
| **Lint Everything** | `make lint` | Check Terraform (`terraform fmt -check`) and Python (`ruff check`) |
| **Format Everything** | `make fmt` | Format Terraform (`terraform fmt`) and Python (`ruff format`) |
| **Generate Dataset** | `make data` | Generate synthetic industrial sensor dataset |
| **Run Drift Monitor** | `make drift` | Execute statistical data drift analysis |
| **Launch MLOps Stack**| `make up-mlops` | Launch MinIO, MLflow, FastAPI, Prometheus via Docker |
| **Stop MLOps Stack**  | `make down-mlops` | Tear down MLOps Docker containers |

### Quick-Start Workflow

```bash
# Quality & Formatting
make lint                   # Check Terraform formatting and Ruff Python linting
make fmt                    # Auto-format Terraform files and Python files

# Testing
make test                   # Run full test suite (Airflow + MLOps)
make test-mlops             # Run MLOps unit/integration tests
make test-airflow           # Run Airflow DAG unit tests
make drift                  # Run data drift monitoring check

# Docker Stacks
make up-mlops               # Start MinIO, MLflow, FastAPI, Prometheus
make down-mlops             # Stop MLOps services
make up-airflow             # Start local Airflow cluster
make down-airflow           # Stop Airflow cluster
```

---

## 4. Operational Safety & Agent Boundaries

1. **Blast Radius Containment:** Confine all changes strictly to `/home/liberprimus/code/devops_and_mlops_projects`.
2. **Verification Mandate:** Always run `make lint && make test` before declaring tasks complete.
3. **Branch Discipline:** Active working branch is `dev`.
4. **Secret Hygiene:** Never commit `.tfvars` containing secrets, AWS keys, or database credentials.

---

## 5. Definition of Done
- [ ] `make lint` passes cleanly (Terraform + Ruff).
- [ ] `make test` passes (Airflow + MLOps test suites).
- [ ] Docker Compose configurations are valid syntax.
- [ ] Working tree is clean.
