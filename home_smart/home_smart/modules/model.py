from psycopg2.extras import RealDictCursor
from home_smart.controllers.db import get_db

class Model(object):
    entity_name = '';

    def __init__(self, entity_name):
        self.entity_name = entity_name

    def select_all(self):
        db = get_db()
        db_cur = db.cursor(cursor_factory=RealDictCursor)
        query = 'SELECT * FROM ' + self.entity_name
        db_cur.execute(query)
        rows = db_cur.fetchall()
        db_cur.close()

        return rows

    def select_by_id(self, id):
        db = get_db()
        db_cur = db.cursor(cursor_factory=RealDictCursor)
        db_cur.execute(
            'SELECT * '
            'FROM ' + self.entity_name + ' '
            'WHERE id = %s '
            'ORDER BY name ASC',
            (id,)
        )
        row = db_cur.fetchone()
        if row is None:
            abort(404, "{0} id {1} doesn't exist.".format(self.entity_name, id))

        return row

    def insert(self, data):
        insert_id = 0
        with get_db() as db:
            with db.cursor(cursor_factory=RealDictCursor) as db_cur:
                count = 0
                data_count = len(data)

                insert_string = 'INSERT INTO ' + self.entity_name + ' ('
                values_string = ') VALUES ('
                
                for k in data:
                    insert_string += k
                    values_string += '%s'
                    count += 1
                    if count < data_count:
                        insert_string += ', '
                        values_string += ', '
                
                insert_string += values_string + ') RETURNING id'
                
                db_cur.execute(insert_string, list(data.values()))
                # insert_id = db_cur.fetchone()[0]
                db.commit()

        return insert_id

    def update(self, data):
        with get_db() as db:
            with db.cursor(cursor_factory=RealDictCursor) as db_cur:
                count = 0
                data_count = len(data)

                update_string = 'UPDATE ' + self.entity_name + ' SET '
                
                for k in data:
                    count += 1
                    if k != 'id':
                        update_string += k + ' = ' + '%(' + k + ')s'
                        if count < (data_count - 1):
                            update_string += ', '
                
                update_string += ' WHERE id = %(id)s '
                
                db_cur.execute(update_string, data)
                db.commit()

    def delete(self, id):
        db = get_db()
        db_cur = db.cursor()
        query = 'DELETE FROM ' + self.entity_name + ' WHERE id = %s'
        db_cur.execute(query, (id,))
        db.commit()

    # def get_fields_by_fields(self, select_fields, join_tables, where_fields):
    #     db = get_db()
    #     db_cur = db.cursor(cursor_factory=RealDictCursor)
    #     query = 'SELECT * FROM ' + self.entity_name
    #     db_cur.execute(query)
    #     rows = db_cur.fetchall()
    #     db_cur.close()

    #     return rows