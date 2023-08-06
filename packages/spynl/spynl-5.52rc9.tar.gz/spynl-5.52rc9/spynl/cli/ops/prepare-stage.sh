#!/bin/bash

# * make a venv with spynl installed
# * create repo-state.txt if needed [$5 == '--mk-repo-state']

SCM_URLS=$1
if [ "$SCM_URLS" == "" ]; then
    echo "SCM URLS NOT GIVEN. EXITING ..."
    exit 2
fi
REVISION=$2
if [ "$REVISION" == "" ]; then
    echo "REVISION NOT GIVEN. EXITING ..."
    exit 2
fi
FBREVISION=$3
if [[ "$FBREVISION" == "" ]]; then
    echo "FALLBACK REVISION NOT GIVEN. EXITING ..."
    exit 2
fi
SPYNLBRANCH=$4
if [[ "$SPYNLBRANCH" == "" ]]; then
    echo "SPYNL BRANCH NOT GIVEN. EXITING ..."
    exit 2
fi

pip3 install virtualenv
virtualenv-3.5 venv
source venv/bin/activate

pip3 install invoke==0.14.0
pip3 install --upgrade setuptools

pip install -e git+ssh://git@github.com/SoftwearDevelopment/spynl.git@${SPYNLBRANCH}#egg=spynl
spynl dev.translations --package spynl

if [ "$5" == "--mk-repo-state" ]; then
    # TODO: install for all scm_urls ... we can even do this if not --mk-repo-state
    for ...
        spynl.dev install --scm_url --revision ${REVISION} --fallbackrevision ${FBREVISION} 
    done
    spynl dev.translations --package _all
    spynl ops.mk_repo_state --packages _all # --revision ${REVISION} --fallbackrevision ${FBREVISION} --revertchanges
fi
