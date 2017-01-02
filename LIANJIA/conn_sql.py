import pymysql


config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Deploy123$',
    'db': 'tenement',
    'charset': 'utf8mb4',
}


def conn_sql(sql, data):
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, data)
        conn.commit()
    except pymysql.IntegrityError:
        conn.rollback()
    except Exception as e:
        print(data, sql)
        print(e)
    finally:
        conn.close()
