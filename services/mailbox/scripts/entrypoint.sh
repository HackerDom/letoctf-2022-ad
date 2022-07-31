#!/bin/bash

chown -R mailbox /var/data
./create_secret_key.sh
./init_db.sh
exec runuser -u mailbox "$@"
