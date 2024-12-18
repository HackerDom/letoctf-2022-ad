#!/bin/bash

gunicorn \
    --bind 0.0.0.0:3131 \
    --workers 4 \
    --worker-connections 1024 \
    main:app
