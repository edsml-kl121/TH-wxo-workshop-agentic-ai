# Set environment variables from .env file
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^(\w+)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
        }
    }
}

# Orchestrate connection commands
orchestrate connections add -a gg_creds
orchestrate connections configure -a gg_creds --env draft -k key_value -t team
orchestrate connections configure -a gg_creds --env live -k key_value -t team
orchestrate connections set-credentials -a gg_creds --env draft -e "api_key=$env:GOOGLE_API_KEY"
orchestrate connections set-credentials -a gg_creds --env live -e "api_key=$env:GOOGLE_API_KEY"
