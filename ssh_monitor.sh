#!/bin/bash

DIR="/var/lib/node_exporter"
METRICS_FILE="$DIR/ssh_login_metrics.prom"

# Проверка существования файла логов
if [ ! -f /var/log/auth.log ]; then
  echo "Log file not found!"
  exit 1
fi

# Генерация файла метрик с заголовками
{
  echo "# HELP ssh_login_attempt_info SSH login attempts with username and IP"
  echo "# TYPE ssh_login_attempt_info gauge"

  # Чтение лог-файлов, извлечение username и ip, агрегация данных
  grep 'sshd.*Accepted' /var/log/auth.log | \
  awk '
    {
      for(i=1;i<=NF;i++) {
        if ($i == "for") user=$(i+1)
        if ($i == "from") ip=$(i+1)
      }
      if (user != "" && ip != "") print "username=" user ",ip=" ip
    }
  ' | \
  sort | uniq -c | while read -r COUNT PAIR; do
    # Извлечение username и ip из строки
    USER=$(echo "$PAIR" | cut -d ',' -f 1 | cut -d '=' -f 2)
    IP=$(echo "$PAIR" | cut -d ',' -f 2 | cut -d '=' -f 2)

    # Создание метрики
    echo "ssh_login_attempt_info{username=\"$USER\", ip=\"$IP\"} $COUNT"
  done
} > "$METRICS_FILE"