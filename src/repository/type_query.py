def get_query():
    QUERY = {
        "INSERT_TRN": """
                      INSERT INTO silver.TRN (date_trn, type_id, categ_id, sum, cur, sum_rub, description, status, card)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,

        "INSERT_CATEGORY": """
                           INSERT INTO silver.CATEGORY (categ_name)
                           VALUES (%s)
                            """,

        "INSERT_TYPE_OPER": """
                            INSERT INTO silver.TYPE_OPER (type_name)
                            VALUES (%s)
                            """
    }
    return QUERY