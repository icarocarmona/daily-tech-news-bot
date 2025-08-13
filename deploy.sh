#!/bin/bash
set -e  # para parar o script se algum comando falhar

echo "🔨 Buildando imagens..."
docker compose build --no-cache

echo "📦 Derrubando containers antigos..."
docker compose down

echo "🚀 Subindo containers..."
docker compose up -d

echo "✅ Deploy concluído!"
