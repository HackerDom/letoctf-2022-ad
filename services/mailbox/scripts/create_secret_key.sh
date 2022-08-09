#!/bin/bash

FILE=/var/data/secret_key
if test -f "$FILE"; then
    echo "$FILE exists"
else
    dd if=/dev/urandom bs=32 count=1 > $FILE
    echo "$FILE created"
fi
