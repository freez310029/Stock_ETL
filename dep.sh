# 設定專案 ID 及映像名稱
PROJECT_ID="your-gcp-project-id"
IMAGE_NAME="stock-etl"
TAG="latest"
GCR_HOST="asia-east1-docker.pkg.dev"

# 完整的 GCR 映像名稱
IMAGE_URI="$GCR_HOST/$PROJECT_ID/$IMAGE_NAME:$TAG"

docker build -t $IMAGE_NAME .

docker tag $IMAGE_NAME $IMAGE_URI

docker push $IMAGE_URI

