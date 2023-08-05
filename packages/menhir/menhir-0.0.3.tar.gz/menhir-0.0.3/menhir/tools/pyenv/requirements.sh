#!/bin/bash
set -e
[ -n "$DEBUG" ] && set -x

project_path="$1"
env_name="$2"

cd "${project_path}"

if ! pyenv virtualenvs --bare | egrep -e "^${env_name}$"  > /dev/null; then
    printf "Create pyenv virtualenv '%s'\n" "${env_name}"
    pyenv virtualenv "${env_name}"
fi

pyenv local "${env_name}"

for f in requirements*.txt; do
    if [ -s "${f}" ]; then
        pip install -r "${f}"
    fi
done
