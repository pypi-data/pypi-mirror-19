#!/bin/bash
# Some tests only work on certain versions of Ansible.
# Use Ansible's pseudo semver to determine if we can run something.
function semver_compare() {
    cat <<EOF |python
from __future__ import print_function
import sys
from distutils.version import LooseVersion

print(LooseVersion('${1}') ${2} LooseVersion('${3}'))
EOF
}

set -ex
# This script runs ara-specific integration tests.
export PATH=$PATH:/usr/local/sbin:/usr/sbin
LOGROOT=${WORKSPACE:-/tmp}
LOGDIR="${LOGROOT}/logs"
BUILD_DIR="${LOGDIR}/build"
SCRIPT_DIR=$(cd `dirname $0` && pwd -P)
export ANSIBLE_TMP_DIR="${LOGDIR}/ansible"
DATABASE="${LOGDIR}/ansible.sqlite"

# Cleanup from any previous runs if necessary
git checkout requirements.txt
[[ -e "${LOGDIR}" ]] && rm -rf "${LOGDIR}"
[[ -e ".tox/venv" ]] && rm -rf .tox/venv
mkdir -p "${LOGDIR}"

# We might want to test with a particular version of Ansible
# To specify a version, use "./run_tests.sh ansible==2.x.x.x"
if [[ -n "${1}" && "${1}" != "ansible==latest" ]]; then
    sed -i.tmp -e "s/ansible.*/${1}/" requirements.txt
fi

# Install ARA so it can be used from a virtual environment
tox -e venv --notest
source .tox/venv/bin/activate
ansible --version

# Setup ARA
export ANSIBLE_CALLBACK_PLUGINS="ara/plugins/callbacks"
export ANSIBLE_ACTION_PLUGINS="ara/plugins/actions"
export ANSIBLE_LIBRARY="ara/plugins/modules"
export ARA_DATABASE="sqlite:///${DATABASE}"

# Run test playbooks
ansible-playbook -vv ara/tests/integration/smoke.yml
ansible-playbook -vv ara/tests/integration/hosts.yml

# This playbook is meant to fail
ansible-playbook -vv ara/tests/integration/failed.yml || true
# This playbook is meant to be interrupted
ansible-playbook -vv ara/tests/integration/incomplete.yml &
sleep 5
kill $!
# This playbook leverages include_role that landed in 2.2.0.0
ansible_version=$(pip freeze |grep ansible== |cut -f3 -d =)
if [[ $(semver_compare "${ansible_version}" ">=" "2.2.0.0") == "True" ]]; then
    ansible-playbook -vv ara/tests/integration/include_role.yml
fi

# Run test commands
pbid=$(ara playbook list -c ID -f value |head -n1)

ara playbook show $pbid
ara host list -b $pbid
ara host show -b $pbid localhost
ara host facts -b $pbid localhost
ara data list -b $pbid
ara data show -b $pbid foo
ara play show $(ara play list -a -c ID -f value |head -n1)
ara result show $(ara result list -a -c ID -f value |tail -n1) --long
ara stats show $(ara stats list -c ID -f value |head -n1)
ara task show $(ara task list -a -c ID -f value |head -n1)
ara file list -b $pbid
ara file show $(ara file list -b $pbid -c ID -f value|head -n1)
ara generate ${BUILD_DIR} && tree ${BUILD_DIR}

# Database migration tests
for test_db in $(ls ara/tests/integration/databases/*.sqlite)
do
    export ARA_DATABASE="sqlite:///${SCRIPT_DIR}/${test_db}"
    ara-manage db upgrade
done

echo "Run complete, logs and build available in ${LOGDIR}"