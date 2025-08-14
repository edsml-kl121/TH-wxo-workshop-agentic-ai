#!/usr/bin/env bash
set -x

orchestrate env activate trial-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate knowledge-bases remove -n thai_policy_knowledge_base
# orchestrate agents remove -n ibm_agent -k native