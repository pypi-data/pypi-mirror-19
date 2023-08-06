#!/usr/bin/env bash

set -e
[ -n "$DEBUG" ] && set -x

project_path="$1"
env_name="$2"

export PYENV_VIRTUALENV_DISABLE_PROMPT=1

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate "${env_name}"
pytest
