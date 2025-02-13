import os
import psycopg2

# Настройки подключения к PostgreSQL
DB_HOST = os.getenv("DB_HOST", "postgrestest")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Путь к файлу для записи метрик
METRICS_FILE = "/metrics/pg_metrics.prom"

def collect_and_write_metrics():
    try:
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Создаем строку для записи метрик
        metrics_data = ""

        # Запрос для получения размеров таблиц
        cursor.execute("""
            SELECT relname AS table_name, pg_total_relation_size(relid) AS table_size
            FROM pg_stat_user_tables;
        """)
        table_sizes = cursor.fetchall()

        # Добавляем метрики размеров таблиц
        metrics_data += "# HELP pg_table_size_bytes Size of tables in bytes\n"
        metrics_data += "# TYPE pg_table_size_bytes gauge\n"
        for table_name, size in table_sizes:
            metrics_data += f'pg_table_size_bytes{{table_name="{table_name}"}} {size}\n'

        # Запрос для получения количества операций
        cursor.execute("""
            SELECT 
                relname AS table_name, 
                seq_scan, 
                seq_tup_read, 
                idx_scan, 
                idx_tup_fetch, 
                n_tup_ins, 
                n_tup_upd, 
                n_tup_del
            FROM pg_stat_user_tables;
        """)
        table_operations = cursor.fetchall()

        # Добавляем метрики операций
        metrics_data += "# HELP pg_table_seq_scan_total Total sequential scans\n"
        metrics_data += "# TYPE pg_table_seq_scan_total counter\n"
        metrics_data += "# HELP pg_table_seq_tup_read_total Total tuples read sequentially\n"
        metrics_data += "# TYPE pg_table_seq_tup_read_total counter\n"
        metrics_data += "# HELP pg_table_idx_scan_total Total index scans\n"
        metrics_data += "# TYPE pg_table_idx_scan_total counter\n"
        metrics_data += "# HELP pg_table_idx_tup_fetch_total Total tuples fetched via index\n"
        metrics_data += "# TYPE pg_table_idx_tup_fetch_total counter\n"
        metrics_data += "# HELP pg_table_inserts_total Total inserts into the table\n"
        metrics_data += "# TYPE pg_table_inserts_total counter\n"
        metrics_data += "# HELP pg_table_updates_total Total updates to the table\n"
        metrics_data += "# TYPE pg_table_updates_total counter\n"
        metrics_data += "# HELP pg_table_deletes_total Total deletes from the table\n"
        metrics_data += "# TYPE pg_table_deletes_total counter\n"

        for table_name, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch, n_tup_ins, n_tup_upd, n_tup_del in table_operations:
            metrics_data += f'pg_table_seq_scan_total{{table_name="{table_name}"}} {seq_scan}\n'
            metrics_data += f'pg_table_seq_tup_read_total{{table_name="{table_name}"}} {seq_tup_read}\n'
            metrics_data += f'pg_table_idx_scan_total{{table_name="{table_name}"}} {idx_scan}\n'
            metrics_data += f'pg_table_idx_tup_fetch_total{{table_name="{table_name}"}} {idx_tup_fetch}\n'
            metrics_data += f'pg_table_inserts_total{{table_name="{table_name}"}} {n_tup_ins}\n'
            metrics_data += f'pg_table_updates_total{{table_name="{table_name}"}} {n_tup_upd}\n'
            metrics_data += f'pg_table_deletes_total{{table_name="{table_name}"}} {n_tup_del}\n'

        # Записываем метрики в файл
        with open(METRICS_FILE, "w") as f:
            f.write(metrics_data)

        print("Metrics successfully written to file.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    collect_and_write_metrics()