#!/bin/bash
sudo apt-get update
sudo apt-get install nginx -y
echo "Hello, nginx!" > /var/www/html/index.html