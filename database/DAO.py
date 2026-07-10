from database.DB_connect import DBConnect
from model.Constructor import Constructor

class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT distinct year "
                 "FROM seasons s  "
                 "ORDER BY year")

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    # PUNTO 2a ----------------------------------------------------------
    # I nodi sono costituiti da tutti i costruttori (constructors) che hanno partecipato ad almeno una
    # gara nel corso del periodo selezionato nel punto 1), estremi inclusi.
    # Si considerino solo le partecipazioni valide, ovvero dove almeno un pilota del costruttore ha ù
    # correttamente tagliato il traguardo (campo position della tabella results NOT NULL).
    @staticmethod
    def getAllNodes(year1, year2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.constructorId, c.constructorRef, c.name, c.nationality
                    from constructors c , races ra , results r 
                    where r.`position` is not null
                    and ra.`year` between %s and %s
                    and c.constructorId = r.constructorId 
                    and r.raceId = ra.raceId
                    order by c.constructorId"""

        cursor.execute(query, (year1, year2,))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results
    # FINE PUNTO 2a ------------------------------------------------------

    # PUNTO 2b ----------------------------------------------------------
    # Due nodi sono connessi da un arco se e solo se i due costruttori hanno condiviso almeno un pilota
    # durante il periodo selezionato (campo driverId della tabella results).
    # Un pilota si considera "condiviso" se ha corso per entrambi i costruttori in gare diverse
    # all'interno del range di anni selezionato.
    # Il peso dell'arco è pari al numero di piloti distinti che hanno corso per entrambi i costruttori
    # nel periodo considerato. Si considerino solo le gare in cui il pilota ha correttamente tagliato il traguardo.
    @staticmethod
    def getAllEdges(year1, year2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select res1.constructorId as c1, res2.constructorId as c2, count(DISTINCT res1.driverId) as peso
                    from results res1 , results res2, races ra1 , races ra2
                    where res1.driverId = res2.driverId
                    and ra2.raceId = res2.raceId 
                    and ra1.raceId = res1.raceId
                    and res1.constructorId > res2.constructorId
                    and ra1.`year` between %s and %s
                    and ra2.`year` between %s and %s
                    AND res1.position IS NOT null
                    and res2.position IS NOT null
                    GROUP BY res1.constructorId, res2.constructorId
                    order by peso desc"""

        cursor.execute(query, (year1, year2, year1, year2,))

        for row in cursor:
            results.append((row["c1"], row["c2"], row["peso"]))

        cursor.close()
        conn.close()
        return results
    # FINE PUNTO 2b ------------------------------------------------------

