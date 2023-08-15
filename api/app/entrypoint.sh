#!/bin/sh

echo "Waiting for opensearch... $SEARCH_URL;"

sleep 10

echo "Opensearch started"

curl -X PUT $SEARCH_URL/facilities

python create_user.py

exec "$@"