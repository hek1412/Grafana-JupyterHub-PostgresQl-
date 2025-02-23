
```
Grafana/
│
├── docker-compose.yml
│
├── jupyterhub/ Каталог, содержащий настройки и конфигурацию для JupyterHub.
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
│   ├── prometheus.yml
│   ├── prometheus.yml
│   └── alert.rules.yml
│
├── metrics/ Каталог с метрики.
│   ├── container_sizes.prom
│   ├── pg_metrics.prom
│   └── image_sizes.prom
│ 
```
