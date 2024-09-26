#!/bin/sh

# Use the environment variable or default to 8080
LISTEN_PORT=${PORT:-8080}

# Replace the port in the nginx.conf
sed -i "s/listen 8080;/listen ${LISTEN_PORT};/" /etc/nginx/conf.d/default.conf

# Start Nginx
exec nginx -g 'daemon off;'