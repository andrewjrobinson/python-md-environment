#!/bin/bash

# this scripts builds the docs, places them into the gh-pages branch
source "env/env-examples.sh"

# so we get the current version and not the system installed one
export PYTHONPATH="."

export

# do the deployment
mkdocs gh-deploy

