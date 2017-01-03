from conn_sql import conn_sql


if __name__ == '__main__':
    sql = "create table lianjia(" \
          "url VARCHAR(200),title VARCHAR(200), name VARCHAR (20),updatetime DATE ,createtime DATE ,price DOUBLE ," \
          "status INTEGER ,longitude DOUBLE ,latitude DOUBLE ,area INTEGER ,room INTEGER ,lroom INTEGER ,toilet INTEGER ," \
          "sfzz INTEGER ,height INTEGER ,direction VARCHAR (10), distance DOUBLE ,district VARCHAR (10),targe VARCHAR(10))"
    conn_sql(sql,[])