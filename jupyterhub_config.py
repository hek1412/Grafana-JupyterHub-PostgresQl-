from dockerspawner import DockerSpawner
import os, nativeauthenticator
c = get_config()

# Основные настройки JupyterHub
c.JupyterHub.bind_url = 'http://:8000'
c.JupyterHub.hub_bind_url = 'http://0.0.0.0:8081'
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator" # Назначаем класс аутентификации
c.NativeAuthenticator.check_common_password = True # Включает проверку на наличие распространенных паролей
c.NativeAuthenticator.allowed_users = {'admin'} # Устанавливает, что только указанный пользователь может использовать систему
c.NativeAuthenticator.admin_users = {'admin'} # Задает администратора JupyterHub.
c.NativeAuthenticator.allowed_failed_logins = 3 # Определяет число неудачных попыток входа, после которых пользователь будет временно заблокирован
c.NativeAuthenticator.seconds_before_next_try = 1200 # Устанавливает время блокировки в секундах после превышения попыток входа (20 минут).
c.Authenticator.open_signup = True # позволяют пользователям регистрироваться самостоятельно 
c.Authenticator.allow_all = True # всем зарегистрированным пользователям позволяет входить в систему
c.JupyterHub.shutdown_on_logout = True # автоматически останавливает сервер пользователя, как только он выходит из системы
c.DockerSpawner.remove_containers = True

# Настраиваем Spawner для использования Docker
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = "jupyter/scipy-notebook" # Указывает образ Docker, который будет использоваться для запуска каждого пользователя
c.Spawner.http_timeout = 180 # указывает максимальное время (в секундах), в течение которого JupyterHub будет ожидать, что спаунер (Spawner) запустит сервер пользователя
c.JupyterHub.start_timeout = 360 # параметр задает максимальное время (в секундах), в течение которого JupyterHub ожидает, что будет произведён успешный запуск контролируемого процесса
c.JupyterHub.shutdown_no_activity_timeout = 600 #  Таймаут для автоматического завершения работы контейнеров при отсутствии активности (10 минут)
c.JupyterHub.shutdown_on_logout = True # автоматически останавливает сервер пользователя, как только он выходит из системы
c.DockerSpawner.use_internal_ip = True # параметр управляет использованием внутренних IP-адресов Docker
c.DockerSpawner.network_name = "jupyterhubtest" # Имя сети Docker, которое будет использоваться
c.Spawner.start_timeout = 240
data_dir = '/srv/jupyterhubtest/data'
c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret') # определяем директорию для секретов
c.JupyterHub.db_url = "sqlite:////srv/jupyterhubtest/data/jupyterhub.sqlite" # Указывает использовать SQLite для хранения данных JupyterHub
c.JupyterHub.log_level = 'DEBUG' # Устанавливает уровень логирования на DEBUG

# Настройки метрик
c.JupyterHub.metrics_enabled = True
c.JupyterHub.metrics_port = 8000
c.JupyterHub.authenticate_prometheus = False