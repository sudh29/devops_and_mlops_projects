# Podman Examples

This repository contains several examples demonstrating how to use Podman with different technologies like Python, Flask, and Selenium.

## Project Structure

- `01_hello/`: Simple Python container example
- `02_flask/`: Flask web application container
- `03_selenium/`: Selenium with Chrome container
- `04_selenium_python/`: Selenium with Python integration
- `05_selenium_grid/`: Selenium Grid setup with Docker Compose

## 1. Hello - Basic Python Container

Simple example of running a Python script in a container.

```bash
# Build the container image
podman build --tag python-podman .

# Run the container
podman run python-podman
```

## 2. Flask Web Application

Example of running a Flask web application in a container.

```bash
# Build the container image
podman build --tag flask-app .

# Run the container with port mapping
podman run --publish 5000:5000 flask-app

# Access the application at:
# http://127.0.0.1:5000
```

## 3. Selenium with Chrome

Example of running Selenium with Chrome in a container.

```bash
# Build the Selenium Chrome image
podman build -t selenium-chrome .

# Run the container with VNC (5900), noVNC (7900), and Selenium (4444) ports
podman run --rm -it \
    -p 4444:4444 \
    -p 5900:5900 \
    -p 7900:7900 \
    --shm-size 2g \
    selenium-chrome

# Alternative: Run with bash shell access
podman run --rm -it \
    -p 4444:4444 \
    -p 5900:5900 \
    -p 7900:7900 \
    --shm-size 2g \
    selenium-chrome bash
```

## 4. Selenium with Python Integration

Example of running Selenium tests with Python in a container.

```bash
# Build the Python Chrome image
podman build -t python-chrome .

# Run the container
podman run -it --rm --shm-size=2g python-chrome

# Alternative: Run with bash shell access
podman run -it --rm --shm-size=2g python-chrome bash
```

## 5. Selenium Grid with Docker Compose

Example of running a Selenium Grid setup using Docker Compose.

```bash
# Start the grid using existing images
podman-compose -f docker_compose_v3.yml up

# Start the grid with forced rebuild
podman-compose -f docker_compose_v3.yml up --build

# Stop and remove the grid
podman-compose -f docker_compose_v3.yml down

# Access containers
podman exec -it selenium-hub /bin/sh      # Access Selenium Hub
podman exec -it selenium-node-chrome /bin/sh  # Access Chrome Node

# Copy test file to Chrome node
podman cp browser_test.py selenium-node-chrome:/home/

# View Chrome node logs
podman-compose logs -f chrome
```

## Podman Command Reference

### Container Management

Common commands for managing containers:

```bash
# List containers
podman ps         # List running containers
podman ps -a      # List all containers (including stopped)

# Container operations
podman run [options] IMAGE [COMMAND]  # Create and start a container
podman stop -a    # Stop all running containers
podman rm -a      # Remove all containers
podman exec -it CONTAINER COMMAND     # Execute command in container

# Container information
podman logs CONTAINER                 # View container logs
podman inspect CONTAINER              # Show detailed container info
podman stats                         # Show resource usage stats
```

### Image Management

Commands for managing container images:

```bash
# List and pull images
podman images                        # List local images
podman pull IMAGE                    # Pull image from registry

# Image cleanup
podman rmi -a --force               # Remove all images forcefully
podman image prune                  # Remove unused images

# Image building and publishing
podman build -t IMAGE_NAME PATH     # Build image from Dockerfile
podman tag SOURCE_IMAGE TARGET      # Tag an image
podman push IMAGE                   # Push image to registry
```

### Volume & Filesystem Management

Commands for managing volumes and container filesystems:

```bash
# Volume operations
podman volume ls                    # List volumes
podman volume create VOLUME_NAME    # Create volume
podman volume rm VOLUME_NAME        # Remove volume

# File operations
podman cp SOURCE DESTINATION        # Copy files between host/container
podman diff CONTAINER              # Show container filesystem changes
```

### Network Management

Commands for managing container networks:

```bash
# Network operations
podman network ls                   # List networks
podman network create NETWORK_NAME  # Create network
podman network rm NETWORK_NAME      # Remove network
podman port CONTAINER              # Show port mappings
```

### Pod Management

Commands for managing pods (groups of containers):

```bash
# Pod operations
podman pod create --name POD_NAME   # Create pod
podman pod ps                      # List running pods
podman pod stop POD_NAME           # Stop pod
podman pod rm POD_NAME             # Remove pod
```

### Miscellaneous Commands

Other useful Podman commands:

```bash
# System information
podman version                      # Show version info
podman info                        # Show system info
podman system prune                # Clean up unused resources

# Registry operations
podman login REGISTRY              # Log in to registry
podman logout REGISTRY             # Log out from registry
podman --help                      # Show help
```

### Advanced Features

#### Port Forwarding

Port forwarding binds container ports to localhost (127.0.0.1):

```bash
# Example: Run Apache HTTP server
podman run --rm -d -p 8080:80 --name httpd docker.io/library/httpd

# Stop the container
podman stop httpd
```

**Note:** When running rootless (default), you must use ports > 1023.

#### API Forwarding

Use Docker API tools with Podman:

```bash
# Example: Run Fedora container using Docker CLI
.\docker.exe run -it fedora echo "Hello Podman!"
```

No special settings needed if no other service is using the Docker API pipe.

#### Rootful vs Rootless Mode

Podman in WSL can run as:

- **Rootless** (default): Non-privileged user mode
- **Rootful**: Root user mode

Important notes:

- Rootful and rootless containers are isolated from each other
- Commands like `podman ps` show different results for each mode

To switch between modes:

```bash
# Switch to rootful mode
podman machine stop
podman machine set --rootful

# Switch back to rootless mode
podman machine stop
podman machine set --rootful=false
```

### Cleanup Commands

```bash
# List all containers
podman ps --all

# Remove specific image
podman rmi -f registry.access.redhat.com/ubi8-micro:latest
```
