#!/bin/bash
set -e

# ============ CONFIGURAÇÕES ============

CONTAINER="strategy_backend_inventory-strategy_db_inventory-1"
DB_USER="strategy_db_inventory"
DB_NAME="postgre"
DB_PASSWORD="***"


BOT_TOKEN="***"
CHAT_ID="-5140030201"

RAR_PASSWORD="OIBbfBI07fhs9s8"

BACKUP_DIR="/tmp/pg_backup"
DATE=$(date +"%Y-%m-%d_%H-%M")

SQL_FILE="$BACKUP_DIR/backup_$DATE.sql"
RAR_FILE="$BACKUP_DIR/backup_$DATE.rar"

# ======================================

mkdir -p "$BACKUP_DIR"

echo "📦 Criando backup do PostgreSQL..."
docker exec \
  -e PGPASSWORD="$DB_PASSWORD" \
  "$CONTAINER" \
  pg_dump -U "$DB_USER" -d "$DB_NAME" \
  > "$SQL_FILE"

echo "🔐 Compactando e criptografando (RAR)..."
rar a -hp"$RAR_PASSWORD" "$RAR_FILE" "$SQL_FILE" > /dev/null

rm -f "$SQL_FILE"

echo "📤 Enviando para o Telegram..."
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="$CHAT_ID" \
  -F document=@"$RAR_FILE" \
  > /dev/null

echo "✅ Backup enviado com sucesso!"
