#!/bin/bash

set -e

SCRIPT_DIR=$(dirname "$(realpath "$0")")
BOT_NAME="bot"
VENV_DIR="$SCRIPT_DIR/venv"
SERVICE_FILE="/etc/systemd/system/$BOT_NAME.service"

if [ $(id -u) -ne 0 ]; then
  echo "судо ёбни долбоёб"
  exit 1
fi

# Установка Python и venv, если не установлены

echo "ща качнем хлам (python3, venv, pip."
apt update && apt install -y python3 python3-venv python3-pip

# Создание виртуального окружения
if [ ! -d "$VENV_DIR" ]; then
  echo "колдую заворот кишок (venv)..."
  python3 -m venv "$VENV_DIR"
fi

# Активация окружения и установка зависимостей
source "$VENV_DIR/bin/activate"
echo "ебашу на дачу (пакеты)..."
pip install --upgrade pip
pip install python-telegram-bot mcstatus

deactivate

# Создание systemd unit файла
cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $SCRIPT_DIR/bot.py
WorkingDirectory=$SCRIPT_DIR
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOF

echo "я сделал блядский $SERVICE_FILE"

# Запуск сервиса
systemctl daemon-reload
systemctl enable $BOT_NAME
systemctl start $BOT_NAME

echo "готово нахуй. $BOT_NAME работает."
systemctl status $BOT_NAME
