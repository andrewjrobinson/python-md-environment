#!/bin/bash

# this scripts builds the docs, places them into the gh-pages branch

# load the variables used in the docs
source "enviro/env-examples.sh"

# so we get the current version of mdx_environment and not the system installed one
export PYTHONPATH="."

# do the deployment
mkdocs gh-deploy

# cleanup (causes issue with mkdocs if left behind)
rm -R site
