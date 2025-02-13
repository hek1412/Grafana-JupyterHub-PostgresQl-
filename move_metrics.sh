#!/bin/bash

# Исходная директория (где находится файл)
SOURCE_DIR="./metrics"

# Целевая директория (куда нужно перенести файл)
TARGET_DIR="/var/lib/node_exporter"

# Имя файла
FILE_NAME="pg_metrics.prom"

# Создаем целевую директорию, если её нет
mkdir -p "$TARGET_DIR"

# Бесконечный цикл
while true; do
    # Проверяем, существует ли файл
    if [ -f "$SOURCE_DIR/$FILE_NAME" ]; then
        # Переносим файл в целевую директорию
        cp "$SOURCE_DIR/$FILE_NAME" "$TARGET_DIR/$FILE_NAME"
        echo "Файл $FILE_NAME перенесен в $TARGET_DIR"
    else
        echo "Файл $FILE_NAME не найден в $SOURCE_DIR"
    fi

    # Ждем 60 секунд
    sleep 60
done