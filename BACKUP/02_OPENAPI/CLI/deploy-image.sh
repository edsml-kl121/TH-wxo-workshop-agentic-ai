ENV_PATH=.env
source $ENV_PATH

ibmcloud login --apikey $WATSONX_API_KEY -r us-south
ibmcloud target -g $CODE_ENGINE_RESOURCE_GROUP
ibmcloud ce project select -n $CODE_ENGINE_PROJECT
ibmcloud ce secret create --name $CODE_ENGINE_CREDENTIALS --from-env-file $ENV_PATH

ibmcloud ce registry create --name $DOCKERHUB_SECRET \
  --server https://index.docker.io/v1/ \
  --username $DOCKERHUB_USERNAME \
  --password $DOCKERHUB_PASSWORD

ibmcloud ce secret get --name $DOCKERHUB_SECRET

# ibmcloud ce application create --name $DEPLOYED_SERVICE_NAME --cpu 2 --memory 4G --es 4G --min-scale 1 --env-from-secret $CODE_ENGINE_CREDENTIALS -v public \
# --image docker.io/$DOCKER_REPOSITORY:$DOCKER_TAG \
# --port 8000 \
# --registry-secret $DOCKERHUB_SECRET
ibmcloud ce application update --name $DEPLOYED_SERVICE_NAME --cpu 2 --memory 4G --es 4G --min-scale 1 --env-from-secret $CODE_ENGINE_CREDENTIALS -v public \
--image docker.io/$DOCKER_REPOSITORY:$DOCKER_TAG \
--port 8000 \
--registry-secret $DOCKERHUB_SECRET
