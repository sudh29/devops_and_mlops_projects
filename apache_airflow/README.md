# Apache Airflow Project

This directory contains Apache Airflow DAGs and related configurations for data pipeline orchestration.

## Setup and Installation

### Prerequisites

- Python 3.8+ installed
- pip or uv package manager
- Docker and Docker Compose (optional, for containerized setup)

### Local Development Environment

1. Create and activate virtual environment:

```bash
# Using uv (recommended)
uv venv --python 3.13
# On Unix/Linux/WSL:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
```

2. Install Apache Airflow:

```bash
# Set the Airflow home directory
export AIRFLOW_HOME=$(pwd)

# Install airflow with required providers
pip install "apache-airflow[postgres,celery,redis]==2.7.1"

# Initialize the database
airflow db init
```

3. Create admin user:

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## Project Structure

```
airflow/
├── dags/                   # DAG definition files
├── plugins/                # Custom plugins
├── logs/                   # Airflow logs
├── config/                 # Configuration files
└── tests/                 # Test files for DAGs and plugins
```

## Running Airflow

### Start Airflow Services (Local)

1. Start the webserver:

```bash
airflow webserver --port 8080
```

2. In a new terminal, start the scheduler:

```bash
airflow scheduler
```

3. Access the Airflow UI at: http://localhost:8080

### Using Docker Compose (Local Stack)

Start services using the included stack:

```bash
docker compose -f docker_compose.yaml up -d
```

## Common Airflow Commands

```bash
# Test a DAG
airflow dags test [dag_id] [execution_date]

# List all DAGs
airflow dags list

# Pause/unpause a DAG
airflow dags pause/unpause [dag_id]

# List tasks in a DAG
airflow tasks list [dag_id]

# Test a specific task
airflow tasks test [dag_id] [task_id] [execution_date]

# Clear task instances
airflow tasks clear [dag_id]
```

## Best Practices

1. **DAG Design**

   - Use meaningful DAG and task IDs
   - Set appropriate retries and retry delays
   - Use tags for better organization
   - Document DAGs with docstrings

2. **Task Dependencies**

   - Use clear task dependencies with >> and <<
   - Avoid circular dependencies
   - Group related tasks using TaskGroups

3. **Testing**

   - Test DAGs before deployment
   - Use Airflow's testing utilities
   - Implement unit tests for custom operators

4. **Monitoring**
   - Set up proper logging
   - Configure alerts for failed tasks
   - Monitor resource usage

## Configuration Tips

1. **Performance**

   - Adjust parallelism settings based on resources
   - Use pools for resource-intensive tasks
   - Configure appropriate timeouts

2. **Security**

   - Use secrets backend for sensitive data
   - Implement proper user authentication
   - Regular security updates

3. **Maintenance**
   - Regular database cleanup
   - Log rotation
   - Periodic backups of metadata database

## Troubleshooting

Common issues and solutions:

1. **Scheduler not picking up DAGs**

   - Check DAG file permissions
   - Verify DAG_FOLDER path
   - Review DAG file syntax

2. **Task failures**

   - Check task logs
   - Verify connections
   - Review resource constraints

3. **Web server issues**
   - Check port availability
   - Verify database connectivity
   - Review webserver logs

## Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [Best Practices Guide](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Airflow GitHub Repository](https://github.com/apache/airflow)
