from psycopg2.extras import RealDictCursor
from controllers.db import get_db

class Model(object):
    # entity_name = None
    # entity_alias = None
    # select = None # tuple of strings ()
    # join = None # tuple of dictionaries {'join_type': 'JOIN|LEFT JOIN|ETC', 'table': 'location', 'alias': 'l', 'field1': location_id, 'field2': id}
    # where = None # tuple of dictionaries {'comparison': WHERE|AND|OR|<|>, 'field': id, 'condition': '=', 'value': 1}

    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.entity_alias = None
        self.select = None
        self.join = None
        self.where = None

    def get_select(self):
        query = 'SELECT '
        if self.select != None:
            for v in self.select:
                query += v + ', '
            query = query.rstrip(', ') + ' '
        else:
            query += '* '
        return query

    def get_from(self):
        query = 'FROM ' + self.entity_name + ' '
        if self.entity_alias != None:
            query += self.entity_alias + ' '
        if self.join != None:
            for v in self.join:
                if v['table'] and v['alias'] and v['field1'] and v['field2']:
                    if v['join_type']:
                        query += v['join_type'] + ' '
                    else:
                        query += 'JOIN '
                    query += v['table'] + ' '
                    if v['alias']:
                        query += v['alias'] + ' '
                    query += 'ON ' + v['field2'] + ' '
                    if 'condition' in v:
                        query += v['condition'] + ' '
                    else:
                        query += '= '
                    query += v['field1'] + ' '
        return query

    def get_where(self):
        query = ''
        if self.where != None:
            query += 'WHERE '
            for w in self.where:
                if w['field'] and w['value']:
                    query += w['field'] + ' '
                    if w['condition']:
                        query += w['condition'] + ' '
                    query += w['value'] + ' '
        return query

    def select_all(self):
        db = get_db()
        db_cur = db.cursor(cursor_factory=RealDictCursor)
        
        query = self.get_select()
        query += self.get_from()
        query += self.get_where()
        
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