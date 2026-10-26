---
repo: devops_and_mlops_projects
review_date: 2026-10-25
current_score: 9.2
target_score: 9.7
---

# Repository Improvement Plan: `devops_and_mlops_projects`

> **Hiring-Bar Audit Target:** AI Engineer / Staff IC / Systems Architect (~8 years experience)  
> **Evaluation Threshold:** 9.5+ / 10.0  
> **Current Overall Score:** **9.2 / 10.0** (Delta to 9.5 bar: +0.3)

---

## 1. Baseline Scorecard & Gaps

| # | Criterion | Weight | Score | Primary Gap / Finding |
|---|---|:---:|:---:|---|
| 1 | **Correctness & functionality** | 15% | **9.4** | Clean execution across Terraform formatting, Airflow OOP tests (4/4 passed), synthetic data generation (5,000 records), and KS statistical drift calculation. Gap: End-to-end FastAPI integration testing relies on installing external dependencies without a single root installer. |
| 2 | **Architecture & design** | 15% | **9.5** | Multi-discipline architecture decoupled into 4 pillars (`terraform`, `docker_and_podman`, `apache_airflow`, `mlops`) with Mermaid architecture diagrams. Clean OOP abstraction in Airflow and modular Terraform patterns. |
| 3 | **Code quality** | 10% | **8.6** | Terraform HCL formatting is 100% compliant. Gap: `ruff check` detects 72 linting errors across Python files (unsorted imports, deprecated `typing.List`, blind exception handling in [train.py](file:///home/liberprimus/code/devops_and_mlops_projects/mlops/train.py), and unused variables). |
| 4 | **Testing & CI** | 15% | **8.8** | Multi-job GitHub Actions CI for linting, MLOps, Airflow, Docker builds, and automated security scanning (Gitleaks + Trivy). Gap: 72 Ruff errors break the CI `lint` job; lacks static Terraform analysis (`tflint` / `checkov`). |
| 5 | **Security** | 10% | **9.7** | Zero hardcoded secrets across repo and git history. Non-root containers (UID 1000). Automated Gitleaks and Trivy security workflows. |
| 6 | **Reliability & performance** | 10% | **9.4** | Container healthchecks with curl probes. Prometheus metrics exporter at `/metrics`. Two-sample Kolmogorov-Smirnov drift detection. MLflow server unreachable fallback. |
| 7 | **DevEx & ops** | 10% | **9.2** | Unified root [Makefile](file:///home/liberprimus/code/devops_and_mlops_projects/Makefile) and [.pre-commit-config.yaml](file:///home/liberprimus/code/devops_and_mlops_projects/.pre-commit-config.yaml). Gap: Missing root-level `pyproject.toml` or `uv` workspace definition for instant local virtualenv bootstrapping. |
| 8 | **Documentation** | 5% | **9.4** | Comprehensive root [README.md](file:///home/liberprimus/code/devops_and_mlops_projects/README.md) with Mermaid diagrams, quickstart, and dedicated submodule guides. Gap: Lacks formal Architecture Decision Records (ADRs). |
| 9 | **Repo hygiene** | 5% | **9.0** | Clean structure, MIT License, extensive 5.5KB [.gitignore](file:///home/liberprimus/code/devops_and_mlops_projects/.gitignore). Gap: Untracked `AGENTS.md`; Python lint failures. |
| 10 | **Impact & clarity** | 5% | **9.6** | Exceptional Staff IC engineering breadth bridging cloud infrastructure, containers, distributed testing, and production ML pipelines with statistical observability. |

---

## 2. Ranked Gaps (Impact ÷ Effort)

| Rank | Gap Description | Affected Criterion | Impact | Effort | Priority |
|:---:|---|---|:---:|:---:|:---:|
| 1 | Fix all 72 Ruff linting and formatting violations across Python files | Code Quality, Testing & CI | High | S | Phase 1 |
| 2 | Add root-level `pyproject.toml` with `uv` workspace for one-command dev setup | DevEx & Ops, Correctness | High | S | Phase 1 |
| 3 | Integrate `tflint` and `checkov` into GitHub Actions CI pipeline | Testing & CI, Security | High | M | Phase 1 |
| 4 | Add Architecture Decision Records (ADRs) for drift detection & remote backend | Documentation | Medium | S | Phase 2 |
| 5 | Add automated integration test script running Docker Compose stacks | DevEx & Ops, Reliability | Medium | M | Phase 2 |
| 6 | Add Grafana dashboard provisioning for Prometheus metrics visualization | Reliability & Impact | Low | M | Phase 3 |

---

## 3. Phased Action Plan

### Phase 1: MVP-Essential (Target: Cross 9.5 Bar)

Focus on resolving the 72 Ruff lint errors, adding root-level workspace tooling, and integrating static Terraform analysis into CI.

#### Task 1.1: Resolve All 72 Ruff Lint Errors
- **Description:** Run `ruff check --fix .` and `ruff format .` to automatically fix import ordering, deprecated `typing.List` annotations, and unused imports, and refactor blind exception handling in [mlops/train.py](file:///home/liberprimus/code/devops_and_mlops_projects/mlops/train.py).
- **Why:** The repository's own GitHub Actions CI pipeline fails on `ruff check .` due to these 72 violations.
- **Files Affected:** `mlops/train.py`, `mlops/src/config.py`, `mlops/src/pipeline.py`, `mlops/tests/test_api.py`, `mlops/tests/test_pipeline.py`, `mlops/serving/schemas.py`.
- **Acceptance Criteria:** `ruff check .` and `ruff format --check .` exit with code 0.
- **Effort:** Small.
- **Score Delta:** Code Quality: +0.8, Testing & CI: +0.4, Repo Hygiene: +0.4.

#### Task 1.2: Root-Level `pyproject.toml` & `uv` Workspace
- **Description:** Create a root `pyproject.toml` configuring modern Python packaging, pinning dependencies, and declaring workspaces so that running `uv sync` from root configures the complete developer environment.
- **Why:** Eliminates fragmented dependency installation across subdirectories.
- **Files Affected:** `pyproject.toml`, `Makefile`.
- **Acceptance Criteria:** Running `uv sync && uv run pytest` works seamlessly from the repository root.
- **Effort:** Small.
- **Score Delta:** DevEx & Ops: +0.4.

#### Task 1.3: Static Terraform Linting (`tflint`) in CI
- **Description:** Add `tflint` step into [.github/workflows/ci.yml](file:///home/liberprimus/code/devops_and_mlops_projects/.github/workflows/ci.yml) under the `lint` job to validate AWS provider arguments and syntax across all 14 projects.
- **Why:** Upgrades Terraform validation from purely aesthetic (`fmt`) to syntactic and semantic validation.
- **Files Affected:** `.github/workflows/ci.yml`.
- **Acceptance Criteria:** `tflint --recursive` executes and passes in CI.
- **Effort:** Medium.
- **Score Delta:** Testing & CI: +0.3.

---

### Phase 2: Hardening & Documentation (Target: 9.6+)

#### Task 2.1: Architecture Decision Records (ADRs)
- **Description:** Add formal ADRs in `docs/adr/`:
  - `001-two-sample-ks-drift-detection.md`: Rationale for non-parametric Kolmogorov-Smirnov test over PSI/Wasserstein for zero-dependency inference monitoring.
  - `002-s3-dynamodb-remote-state-locking.md`: Architectural pattern for collaborative state consistency and concurrency safety.
- **Why:** Demonstrates Staff IC architectural intentionality and structured technical documentation.
- **Files Affected:** `docs/adr/001-two-sample-ks-drift-detection.md`, `docs/adr/002-s3-dynamodb-remote-state-locking.md`.
- **Acceptance Criteria:** Markdown ADRs with clear context, decision, and consequences.
- **Effort:** Small.
- **Score Delta:** Documentation: +0.4.

#### Task 2.2: Automated Container Integration Smoke Test
- **Description:** Add `make test-containers` or script verifying `docker compose up -d` boots healthy containers and verifies `curl http://localhost:8000/health` before teardown.
- **Why:** Guarantees that container images and Docker Compose networks actually work end-to-end.
- **Files Affected:** `scripts/smoke_test_containers.sh`, `Makefile`.
- **Acceptance Criteria:** Script starts compose stacks, validates 200 OK healthchecks, and tears down cleanly.
- **Effort:** Medium.
- **Score Delta:** DevEx & Ops: +0.2, Reliability: +0.2.

---

### Phase 3: Nice-to-Have (Target: 9.7+)

#### Task 3.1: Prometheus & Grafana Live Observability Dashboard
- **Description:** Add pre-provisioned Grafana dashboards in `mlops/grafana/` charting live inference throughput, P99 request latency, and failure probability distribution from the Prometheus `/metrics` exporter.
- **Why:** Provides an executive visual demonstration of production machine learning observability.
- **Files Affected:** `mlops/docker_compose_mlops.yml`, `mlops/grafana/`.
- **Acceptance Criteria:** Grafana auto-loads dashboards on `make up-mlops`.
- **Effort:** Medium.
- **Score Delta:** Impact & Clarity: +0.2.

---

## 4. Projected Score Progression

| Phase | Milestone | Expected Score | Delta |
|:---:|---|:---:|:---:|
| **Baseline** | Current audit baseline | **9.2** | — |
| **Phase 1** | Clean Ruff lint (72 fixed), root uv workspace, tflint CI | **9.5** | +0.3 |
| **Phase 2** | Architecture Decision Records & smoke test automation | **9.6** | +0.1 |
| **Phase 3** | Grafana dashboard auto-provisioning & observability | **9.7** | +0.1 |

---

## 5. Definition of Done for Reaching 9.5+

- [ ] `ruff check .` passes with 0 errors across all Python files.
- [ ] `ruff format --check .` passes with 0 formatting discrepancies.
- [ ] `terraform fmt -check -recursive terraform/` exits with code 0.
- [ ] `tflint --recursive` integrated into GitHub Actions CI.
- [ ] Unified root `pyproject.toml` enables single-command developer setup.
