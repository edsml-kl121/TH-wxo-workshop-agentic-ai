orchestrate env activate trial-env
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Remove agents
orchestrate agents remove -n customer_multi_agent -k native
orchestrate agents remove -n client_operation_agent_a1 -k native
orchestrate agents remove -n information_agent_a2 -k native

# Remove tools
orchestrate tools remove -n send_email
orchestrate tools remove -n create_calendar_event
orchestrate tools remove -n place_order
orchestrate tools remove -n get_products
orchestrate tools remove -n get_promotions
orchestrate tools remove -n get_status
orchestrate tools remove -n getApiInfo
orchestrate tools remove -n healthCheck

# Run additional cleanup scripts
& "$SCRIPT_DIR/mcp-server/delete_tools.sh"
& "$SCRIPT_DIR/mcp-server/delete_connection.sh"
