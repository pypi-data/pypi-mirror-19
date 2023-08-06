#!/usr/bin/env bash

set -e
[ -n "$DEBUG" ] && set -x

cwd=$(pwd)
env_name=$(basename "${cwd}")

export PYENV_VIRTUALENV_DISABLE_PROMPT=1

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate "${env_name}"
pytest "$@"
