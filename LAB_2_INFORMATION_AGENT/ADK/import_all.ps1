# Enable command echoing
$VerbosePreference = 'Continue'

# Install git lfs
& git lfs install

# Activate orchestrate environment
orchestrate env activate trial-env

# Get script directory
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Import tools
orchestrate tools import -k python `
    -f "$SCRIPT_DIR/tools/get_promotions/get_promotions.py" `
    -r "$SCRIPT_DIR/tools/get_promotions/requirements.txt" `

orchestrate tools import -k python `
    -f "$SCRIPT_DIR/tools/get_products/get_products.py" `
    -r "$SCRIPT_DIR/tools/get_products/requirements.txt" `

orchestrate tools import -k python `
    -f "$SCRIPT_DIR/tools/get_status/get_status.py" `
    -r "$SCRIPT_DIR/tools/get_status/requirements.txt" `

# Import agent
orchestrate agents import -f "$SCRIPT_DIR/agents/information_agent.yaml"
# orchestrate knowledge-bases import -f "$SCRIPT_DIR/knowledge_base/policy_knowledge.yaml"
