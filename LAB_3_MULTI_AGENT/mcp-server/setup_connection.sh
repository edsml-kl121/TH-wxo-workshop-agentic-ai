set -a  # Automatically export all variables
source .env
set +a

orchestrate connections add -a tavily_adk
orchestrate connections configure -a tavily_adk --env draft -k key_value -t team
orchestrate connections configure -a tavily_adk --env live -k key_value -t team
orchestrate connections set-credentials -a tavily_adk --env draft \
  -e "TAVILY_API_KEY=$TAVILY_API_KEY"
orchestrate connections set-credentials -a tavily_adk --env live \
  -e "TAVILY_API_KEY=$TAVILY_API_KEY"
