#!/usr/bin/env bash
set -x

orchestrate env activate TZ-37
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate agents remove -n sales_multi_agent -k native
orchestrate agents remove -n client_operation_agent_a1 -k native
orchestrate agents remove -n information_agent_a2 -k native