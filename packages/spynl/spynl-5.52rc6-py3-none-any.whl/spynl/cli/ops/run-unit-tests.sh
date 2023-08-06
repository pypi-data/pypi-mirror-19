#!/bin/bash

# * Install repos at revisions given by repo-state.txt
# * Run unit tests 

# Preparing the stage should maybe not live in this script,
# but activating the virtualenv doesn't stay active across
# sh invocations in pipeline scripts.
# See https://issues.jenkins-ci.org/browse/JENKINS-37116
`dirname $0`/prepare-stage.sh $1 $2 $3 $4 --mk-repo-state || { echo 'prepare-stage.sh failed!' ; exit 1; }

source venv/bin/activate

# for test reports
pip install coverage pylint
mkdir -p pylint-results
# for Junit output
pip install pytest-cov pytest-sugar

# reading in repo-state.txt completely so the open file is not read by a subcommand
readarray REPO_STATE < repo-state.txt  # needs bash4

# TODO: let prepare-stage do this ... ?
# install packages - spynl was already installed by prepare-stage.sh
for line in "${REPO_STATE[@]}"; do
    REPO=`echo $line | cut -d ' ' -sf 1`
    COMMITID=`echo $line | cut -d ' ' -sf 2`
    if [ "$REPO" != "spynl" ]; then
        echo "Installing repo '$REPO' with revision '$COMMITID' ..."
        spynl dev.install --repos $REPO --revision $COMMITID
    else
        echo "Updating repo 'spynl' to revision '$COMMITID' ..."
        # TODO: git or hg - make a ops target for this?
        spynl hg.update --repos spynl --revision $COMMITID 
    fi
done

# now we can test the repos
for line in "${REPO_STATE[@]}"; do
    REPO=`echo $line | cut -d ' ' -sf 1`
    COMMITID=`echo $line | cut -d ' ' -sf 2`
    echo "Testing repo '$REPO' on revision '$COMMITID' ..."
    spynl dev.test --repos $REPO --reports
done
