# Инсерт в bronze.sber_oper
def insert_bronze_sber_oper():
    query = """
            INSERT INTO bronze.sber_oper (oper_date, type_oper, category, amount, cur, amount_rub, description, status, \
                                          card)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    return query