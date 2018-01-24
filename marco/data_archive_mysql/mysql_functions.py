class MysqlQuery(object):

    '''
    This class is for submitting psql querys and return the number of results
    and execution time in a readable format.

    The format_query can be easily expanded to extract more information, for
    example the planning time and the index usage.
    '''

    def __init__(self):
        '''
        Nothing to declare
        '''
        pass

    def format_query(self, x):
        '''
        Extract the number of rows returned and the execution time of the
        queryreturned from using EXPLAIN ANALYSE in PostgreSQL. See
        >> ltarchive_allkeys_notes.txt
        for examples of the returned strings.

        Input:
        x - Arrays returned by psycopg2.fetchall()

        Output:
        (1) number of results returned
        (2) execution time
        '''
        return (int((x[0][0].split(' ')[-2]).split('=')[-1]),
                float(x[-1][0].split(' ')[-2])/1000.)

    def run_query(self, conn, query):
        '''
        run the query on the the PostgreSQL through connection - conn
        and return the formatted results.
        '''
        # psycopg2 creates a server-side cursor, which prevents all of the
        # records from being downloaded at once from the server.
        cur = conn.cursor()
        cur.execute(query)
        temp = cur.fetchall()
        cur.close()

        return self.format_query(temp)
