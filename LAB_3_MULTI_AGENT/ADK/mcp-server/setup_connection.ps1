# Setup automation connection
# Load environment variables from .env
if (Test-Path .env) {
	Get-Content .env | ForEach-Object {
		if ($_ -match '^(\w+)=(.*)$') {
			[System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
		}
	}
}

orchestrate connections add -a tavily_adk
orchestrate connections configure -a tavily_adk --env draft -k key_value -t team
orchestrate connections configure -a tavily_adk --env live -k key_value -t team
orchestrate connections set-credentials -a tavily_adk --env draft -e "TAVILY_API_KEY=$env:TAVILY_API_KEY"
orchestrate connections set-credentials -a tavily_adk --env live -e "TAVILY_API_KEY=$env:TAVILY_API_KEY"
