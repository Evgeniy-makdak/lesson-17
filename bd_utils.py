import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def get_connect_bd():  # Подключение к существующей базе данных
    try:
        connection = psycopg2.connect(user="postgres",  # параметры подключения
                                      password="Swaq32123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="my_bd_ads")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # автокоммит изменений
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        return None
    finally:
        print("Успешное подключие к бд")
        print("-" * 30)
    return connection


def disconntct_bd(connection, cursor) -> None:
    cursor.close()
    connection.close()
    print("Соединение с PostgreSQL закрыто")


def get_base_req(req_type: int) -> str:
    """ возвращает текст базового запроса (все опубликованные записи )"""
    req_text = """
        SELECT 
                  ads.id 
                , ads.name
                , ads.price
                , aut.name
                , adr.address
                , ads.description
        FROM ads as ads
        LEFT JOIN author_address as a_a
            ON ads.author_address_id = a_a.id
        LEFT JOIN author as aut
            ON a_a.author_id = aut.id
        LEFT JOIN addresses as adr
            ON a_a.address_id = adr.id
        WHERE ads.is_published is true
        """
    if req_type:
        req_text = """
            SELECT 
                      aut.name 
                    , sum(ads.price)
            FROM ads as ads
            LEFT JOIN author_address as a_a
                ON ads.author_address_id = a_a.id
            LEFT JOIN author as aut
                ON a_a.author_id = aut.id
            WHERE ads.is_published is true
            GROUP BY aut.name
            """

    return req_text
