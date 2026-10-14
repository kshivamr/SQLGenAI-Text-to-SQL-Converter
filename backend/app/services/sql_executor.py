from backend.app.database.connection import get_connection

def execute_sql(sql):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results