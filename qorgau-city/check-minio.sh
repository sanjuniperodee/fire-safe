#!/bin/bash

echo "🔍 Checking MinIO buckets..."

# Проверяем bucket'ы через временный контейнер mc
docker run --rm --network qorgau-city_backend \
  minio/mc:latest \
  sh -c "
    mc config host add minio http://minio:9000 minioadmin minioadmin &&
    echo '📦 Available buckets:' &&
    mc ls minio/ &&
    echo '' &&
    echo '🔒 Bucket policies:' &&
    mc anonymous get minio/isec &&
    mc anonymous get minio/public &&
    mc anonymous get minio/static
  "

echo "✅ MinIO check completed!" 