#!/bin/bash

chown -R mailbox /var/data
./scripts/create_secret_key.sh
exec runuser -u mailbox "$@"
