#!/usr/bin/env bash
set -x

git lfs install

orchestrate env activate TZ-37
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/get_policies/get_policies.py" \
    -r "${SCRIPT_DIR}/tools/get_policies/requirements.txt"
    --resume_import

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/get_products/get_products.py" \
    -r "${SCRIPT_DIR}/tools/get_products/requirements.txt"
    --resume_import

# orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_base/policy_knowledge.yaml
orchestrate agents import -f ${SCRIPT_DIR}/agents/information_agent.yaml