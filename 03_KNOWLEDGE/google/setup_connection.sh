set -a  # Automatically export all variables
source .env
set +a

orchestrate connections add -a gg_creds #create connecton assest
orchestrate connections configure -a gg_creds --env draft -k key_value -t team
orchestrate connections configure -a gg_creds --env live -k key_value -t team
orchestrate connections set-credentials -a gg_creds --env draft \
  -e "api_key=$GOOGLE_API_KEY"
orchestrate connections set-credentials -a gg_creds --env live \
  -e "api_key=$GOOGLE_API_KEY"