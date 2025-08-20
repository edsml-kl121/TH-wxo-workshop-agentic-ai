orchestrate env activate trial-env
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

orchestrate tools import -k openapi -f "$SCRIPT_DIR/openapi_tools/automation_openapi.json"

orchestrate tools import -k python `
    -f "$SCRIPT_DIR/tools/get_promotions/get_promotions.py" `
    -r "$SCRIPT_DIR/tools/get_promotions/requirements.txt" `

orchestrate tools import -k python `
    -f "$SCRIPT_DIR/tools/get_products/get_products.py" `
    -r "$SCRIPT_DIR/tools/get_products/requirements.txt" `

orchestrate tools import -k python `
    -f "$SCRIPT_DIR/tools/get_status/get_status.py" `
    -r "$SCRIPT_DIR/tools/get_status/requirements.txt" `

foreach ($agent in @('client_operation_agent.yaml', 'information_agent.yaml', 'orchestrator_agent.yaml')) {
	orchestrate agents import -f "$SCRIPT_DIR/../agents/$agent"
}
