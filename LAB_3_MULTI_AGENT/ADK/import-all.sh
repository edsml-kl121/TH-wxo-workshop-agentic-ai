#!/usr/bin/env bash
set -x

orchestrate env activate TZ-37
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate tools import -k openapi -f "${SCRIPT_DIR}/openapi_tools/automation_openapi.json"

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/get_promotions/get_promotions.py" \
    -r "${SCRIPT_DIR}/tools/get_promotions/requirements.txt"
    --resume_import

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/get_products/get_products.py" \
    -r "${SCRIPT_DIR}/tools/get_products/requirements.txt"
    --resume_import

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/get_status/get_status.py" \
    -r "${SCRIPT_DIR}/tools/get_status/requirements.txt"
    --resume_import

for agent in client_operation_agent.yaml information_agent.yaml orchestrator_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done
