ENV_PATH=.env
source $ENV_PATH

podman buildx build --platform linux/amd64 -t google-automation .
podman tag google-automation $DOCKER_REPOSITORY:$DOCKER_TAG
podman push $DOCKER_REPOSITORY:$DOCKER_TAG