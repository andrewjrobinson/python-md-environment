#!/bin/bash

# this scripts builds the docs, places them into the gh-pages branch


# so we get the current version and not the system installed one
export PYTHONPATH="."

# do the deployment
mkdocs gh-deploy

