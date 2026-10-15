from database.DB_connect import DBConnect
from model.movie import Movie
"""
TEMA D'ESAME - ImdbMaratonaFilm (database imdb)

Si considerano TUTTI i film (qualsiasi genere e anno) con almeno V voti (ratings.total_votes).
Ogni film ha una durata in minuti (movie.duration) e un voto medio (ratings.avg_rating).
Interprete = persona in role_mapping con category = 'actor' oppure 'actress'.

PUNTO 1
a. Campo txtV: numero minimo di voti V (default 50000).
   Errore se V non è un intero >= 0.

b. Bottone "Crea Grafo": grafo SEMPLICE, PESATO, NON ORIENTATO.
   - Nodi: tutti i film con almeno V voti.
   - Archi: tra due film che hanno ALMENO UN INTERPRETE IN COMUNE.
   - Peso: numero di interpreti in comune.

c. Stampare numero di vertici, numero di archi e NUMERO DI COMPONENTI CONNESSE.
   Riempire ddFilm1 e ddFilm2 con tutti i nodi, in ordine alfabetico di titolo.

d. L'utente sceglie due film f1 (ddFilm1) e f2 (ddFilm2).
   Bottone "Test Connessione":
   - verificare se f2 è RAGGIUNGIBILE da f1 nel grafo;
   - se sì, stampare il cammino con il MINOR NUMERO DI ARCHI tra f1 e f2
     (tutti i film attraversati, in ordine) e il numero di archi;
   - se no, stampare un messaggio.
"""
class DAO:
    @staticmethod
    def getNodes(voti):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """SELECT m.id AS id, m.title AS title, m.year AS year,
                          r.avg_rating AS media, r.total_votes AS total_votes,
                          m.duration AS duration
                   FROM movie m, ratings r
                   WHERE m.id = r.movie_id
                     AND r.total_votes >= %s"""
        cursor.execute(query, (voti,))
        for row in cursor:
            results.append(Movie(row["id"], row["title"], row["year"],
                                 float(row["media"]), row["total_votes"], row["duration"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppie(voti):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """SELECT r.movie_id AS mId, r.name_id AS aId
                   FROM role_mapping r
                   WHERE r.category IN ('actor', 'actress')
                     AND r.movie_id IN (SELECT ra.movie_id
                                        FROM ratings ra
                                        WHERE ra.total_votes >= %s)"""
        cursor.execute(query, (voti,))
        for row in cursor:
            results.append((row["mId"], row["aId"]))
        cursor.close()
        conn.close()
        return results
