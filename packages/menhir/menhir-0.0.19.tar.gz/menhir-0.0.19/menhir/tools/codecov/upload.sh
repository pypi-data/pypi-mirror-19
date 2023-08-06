#!/bin/bash
set -e
[ -n "$DEBUG" ] && set -x

bash <(curl -s https://codecov.io/bash) -F "${MENHIR_PROJECT}" -s "$(pwd)"
