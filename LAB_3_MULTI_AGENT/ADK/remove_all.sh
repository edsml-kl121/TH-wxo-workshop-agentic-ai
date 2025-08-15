#!/usr/bin/env bash
set -x

orchestrate env activate trial-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate agents remove -n customer_multi_agent -k native
orchestrate agents remove -n client_operation_agent_a1 -k native
orchestrate agents remove -n information_agent_a2 -k native

orchestrate tools remove -n send_email
orchestrate tools remove -n create_calendar_event
orchestrate tools remove -n place_order
orchestrate tools remove -n get_products
orchestrate tools remove -n get_promotions
orchestrate tools remove -n get_status
orchestrate tools remove -n getApiInfo
orchestrate tools remove -n healthCheck

bash mcp-server/delete_tools.sh
bash mcp-server/delete_connection.sh