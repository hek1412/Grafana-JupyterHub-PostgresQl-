ДЗ2. Мониторинг
В рамках выполнения ДЗ мы развернем необходимые сервисы, создадим скрипты и настроим дашборды в графане для отображения информации о:
- активности пользователей в юпитер (количество операций в день)
- топовых тетрадках (сколько подъедают)
- топовых таблицах в постресе с их владельцами
Создадим и настроим:
Алерт оповещающего при заходе пользователя на сервер по ssh на почту.
Алерт оповещающего при потребление общим количеством контейнеров мощности более чем на 80 %.

Структура директории с проектом:

```
Grafana/
│
├── docker-compose.yaml 
│
├── jupyterhub/ Каталог, содержащий конфигурацию для JupyterHub (он был уже развернут по ДЗ1).
│   ├── docker-compose.yaml
│   ├── Dockerfile.jupyterhub
│   └── jupyterhub_config.py
│
├── prometheus/ Каталог с конфигурацией Prometheus.
│   ├── prometheus.yml
│   └── alert.rules.yml
│
├── grafana/ Каталог для Grafana
│
├── alertmanager/ Каталог с конфигурацией Alertmanager.
│   └── alertmanager.yml
│
├── script/ Каталог для скриптов
│   ├── sum_container_sizes.sh
│   ├── 
│   └── 
│
├── metrics/ Создаваемая сервисами дирекpия с метрики.
│   ├── container_sizes.prom
│   ├── pg_metrics.prom
│   └── image_sizes.prom
│
├── pg_metrics_exporter/ Каталог со скриптом на питоне для осуществления запросов в POSTGRES_DB.
│   ├── Dockerfile.exporter
│   └── pg_metrics_exporter.py 
│
```

Учитывая что юпитер хаб у нас уже развернут в рамках выполнения другого задания, то переходим сразу к запуску остальных сервисов.

UP (Важно отметить): 
Нужно добавить в файл конфигурации хаба параметры по сбору метрик:
c.JupyterHub.metrics_enabled = True
c.JupyterHub.metrics_port = 8000
c.JupyterHub.authenticate_prometheus = False

Итак переходим в директорию с проектом и запускаем сервисы

docker compose up --build -d

![image](https://github.com/user-attachments/assets/9989da70-518a-4dc4-9bb8-eb60a8e05ad1)

docker inspect prometheustest
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' prometheustest
Получаем результат
172.20.0.19
переходим веб интерфейс графаны по адресу: 
http://skayfaks.keenetic.pro:35006/
Выбираем источник данных прометей
![image](https://github.com/user-attachments/assets/a593b693-cbda-4760-b8ce-c70e438a2acc)
Используем полученный адрес 172.20.0.19 (он меняется если контейнер убить) и порт 9090
![image](https://github.com/user-attachments/assets/66bd3d3b-8afd-4d75-af21-7f4161e17811)

Тестируем и если все ок, идем создавать дашборды, делаем Import dashboard
grafana/JupyterHub сведения о контейнерах 2.json
Пока у нас запушенных контейнеров пользователей нет, проверим это например в панели юпитер хаба
![image](https://github.com/user-attachments/assets/8ebba85f-379d-4ed3-bcbb-e32232782d6a)

Теперь запустим 3 сервера
![image](https://github.com/user-attachments/assets/a9d7e787-4695-4b26-a8ea-7b63f0701270)
Возвращаемся в графану и анализируем полученные результаты)
![image](https://github.com/user-attachments/assets/4d64bb49-91df-4565-9642-84dde9a78d4b)
http://skayfaks.keenetic.pro:35100/d/bedxa8g8anqiof/jupyterhub-svedenija-o-kontejnerah-2?orgId=1&from=now-15m&to=now&timezone=browser&refresh=1m

Получили первый дашборд, отлично, но мне не понравилось что юпитер хаб не дает реальный размер контейнеров с учетом слоев образа.
Используем написанный скрипт
script/sum_container_sizes.sh
ССЫЛКА НА РИДМИ
Делаем Import dashboard grafana/Сведения о размерах контейнеров и томов.json
с его помощью получаем полные размеры всех контейнеров и не только юпитера 
![image](https://github.com/user-attachments/assets/03ed3408-d57f-48a5-b822-cd58b1f19106)
если нужно только спедения по юпитеру то используем другой дашборд (теперь сразу видно кто сжирает все место на серваке)
![image](https://github.com/user-attachments/assets/e611db6f-36d8-4c4c-9aed-ca7f44f8628f)
Так же добавил отображения размера томов контейнеров)
![image](https://github.com/user-attachments/assets/ad421893-713c-4807-a6e4-cedffd83fc98)

http://skayfaks.keenetic.pro:35100/d/aedxfkzowsyyoa/svedenija-o-razmerah-kontejnerov-i-tomov?orgId=1&from=now-6h&to=now&timezone=browser

Следующий этап, это PosgresQL и получение сведений о таблицах с их владельцами.

С этой задачей справляется скрипт pg_metrics_exporter.py который запускается в контейнере pg_metrics_exporter каждые 10 минут.
Так же как и получение сведений о размерах контейнеров и томов, этот скрипт выводит все метрики в директорию с метриками в файл pg_metrics.prom и далее они копируются в /var/lib/node_exporter.
Важно не забыть наполнить БД необходимыми таблицами для тестов).


