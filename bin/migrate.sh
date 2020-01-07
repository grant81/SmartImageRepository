#!/bin/bash

sleep 5 && \
migrate \
-source=file://./migrations/ \
-database="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}?sslmode=${SSL_MODE}" \
up