ENV_PATH=.env
source $ENV_PATH

podman buildx build --platform linux/amd64 -t information_agent .
podman tag information_agent $DOCKER_REPOSITORY:$DOCKER_TAG
podman push $DOCKER_REPOSITORY:$DOCKER_TAG