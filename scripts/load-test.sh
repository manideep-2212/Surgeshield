#!/usr/bin/env bash
set -e
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login -H 'Content-Type: application/json' -d '{"email":"attendee@surgeshield.local","password":"Password@123"}' | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
for i in $(seq 1 120); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST "http://localhost:8080/api/events/1/register" \
    -H "Authorization: Bearer $TOKEN" -H "Idempotency-Key: load-$i" -H "Content-Type: application/json" -d '{}' &
done
wait
curl -s http://localhost:8080/api/events/1
