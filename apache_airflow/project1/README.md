# Apache Airflow ETL Project

This guide will help you set up and run the sample Airflow DAG for ETL workflows.

## Prerequisites

- Python 3.8+
- [Apache Airflow](https://airflow.apache.org/) installed (recommended in a virtual environment)
- WSL (Windows Subsystem for Linux) or Linux environment

## Setup Instructions

### 1. Clone the Repository & Navigate to Project

```bash
cd devops_and_mlops_projects/apache_airflow
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Airflow DAGs Directory

```bash
mkdir -p ~/airflow/dags
cp project1/src/first_airflow.py ~/airflow/dags/
```

### 5. Initialize Airflow Database

```bash
airflow db init
```

### 6. Create Airflow Admin User

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### 7. Start Airflow Webserver & Scheduler

```bash
airflow webserver &
airflow scheduler &
```

Access the Airflow UI at [http://localhost:8080](http://localhost:8080).

## Notes

- Always activate your virtual environment before running Airflow commands.
- Place your DAG files in the `~/airflow/dags/` directory.
- Default credentials: username `admin`, password `admin`.

## Troubleshooting

- If you encounter permission issues, ensure your user has access to the `~/airflow` directory.
- For missing dependencies, re-run `pip install -r requirements.txt`.
- For more help, see the [Airflow documentation](https://airflow.apache.org/docs/).

---

**Project Structure:**

```
apache_airflow/
├── project1/
│   ├── src/
│   │   └── first_airflow.py
│   └── test/
│       └── test.py
├── requirements.txt
└── ...
```
