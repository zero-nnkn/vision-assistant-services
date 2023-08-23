CONTAINER_NAME="test"
# CONTAINER_IMG="test"
CONTAINER_IMG="vqa-minigpt4"

docker run \
    -it \
    --rm \
    -p 8080:8000 \
    --gpus all \
    --name $CONTAINER_NAME \
    $CONTAINER_IMG
