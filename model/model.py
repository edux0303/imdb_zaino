import networkx as nx
from database.DAO import DAO
from itertools import combinations

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0
        self._D = 0
    # ---------- PUNTO 1 ----------
    def buildGraph(self, voti):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodes(voti)
        for n in self._nodes:
            self.idMap[n.id] = n

        self._grafo.add_nodes_from(self._nodes)

        for s1, s2 in DAO.getCoppie(voti):
            if s1 in self.idMap :
                self.idMap[s1].interpreti.add(s2)

        for c1, c2 in combinations(self._nodes, 2):
            peso = len(c1.interpreti & c2.interpreti)
            if peso > 0:
                self._grafo.add_edge(c1,c2, weight=peso)



    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)
    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda x: x.title)

    def getNumeroConnesse(self):
        return nx.number_connected_components(self._grafo)

    def getCamino(self,f1,f2):
        if not nx.has_path(self._grafo, f1, f2):
            return [],0
        cammino = nx.shortest_path(self._grafo,f1,f2)
        return cammino, len(cammino)-1

    def getComponenteMax(self):
        # la componente più grande, come lista ordinata per nome
        piuGrande = max(nx.connected_components(self._grafo), key=len)
        return sorted(piuGrande, key=lambda r: r.title)

    """
    PUNTO 2
    a. L'utente inserisce in txtD una durata massima D in minuti (intero > 0).

    b. Bottone "Maratona": con un algoritmo RICORSIVO trovare un insieme di film tale che
       - contiene il film f1 scelto in ddFilm1;
       - tutti i film sono nella STESSA COMPONENTE CONNESSA di f1;
       - la DURATA TOTALE è al massimo D minuti;
       - contiene il MAGGIOR NUMERO POSSIBILE di film.
       A parità di numero di film: SOMMA DEI VOTI MEDI (avg_rating) massima.
       A ulteriore parità: DURATA TOTALE minima.

    c. Stampare i film scelti (durata e voto medio), il numero di film,
       la durata totale e la somma dei voti medi (1 decimale).
       Se f1 da solo dura più di D: messaggio.

    VALORI DI CONTROLLO (V=50000)
    Logan  D=300 -> 2 film, 265 min, 16.1  (Logan, La La Land)
    Logan  D=400 -> 3 film, 370 min, 23.7  (+ The Greatest Showman)
    Logan  D=500 -> 4 film, 489 min, 31.3  (+ The Favourite)
    Logan  D=600 -> 5 film, 583 min, 38.7  (+ Lady Bird)
    Avengers: Infinity War D=500 -> 4 film, 500 min, 30.9
       (Avengers: Infinity War, Hidden Figures, The Shape of Water, Good Time)
    Avengers: Infinity War D=600 -> 5 film, 600 min, 36.4
       (Avengers: Infinity War, Justice League, Good Time, Ant-Man and the Wasp, Ralph Breaks the Internet)
    Black Panther D=600 -> 3 film, 380 min, 21.4 (Black Panther, Creed II, Us: la componente ha 3 film)
    Joker D=600 -> solo Joker (è isolato)
    Avengers: Infinity War D=100 -> messaggio (dura 149 minuti)
    """

    def getMaratona(self,f1,D):
        componente = nx.node_connected_component(self._grafo,f1)
        self._candidati = []
        for c in componente:
            if c != f1:
                self._candidati.append(c)

        self._solBest = []
        self._D = D

        if f1.duration > D:
            return []
        self._ricorsione([f1],f1.duration,0)

        return self._solBest

    def _ricorsione(self,parziale,durata,start):
        if self._migliore(parziale):
            self._solBest = list(parziale)

        for i in range(start, len(self._candidati)):
            f = self._candidati[i]
            if f.duration+durata<= self._D:
                parziale.append(f)
                self._ricorsione(parziale,f.duration+durata,i+1)
                parziale.pop()


    def _migliore(self,parziale):
        if len(self._solBest) == 0:
            return True

        if len(parziale) != len(self._solBest):
            return len(parziale) > len(self._solBest)

        voti= round(sum(f.avg_rating for f in parziale),1)
        votiBest = round(sum(f.avg_rating for f in self._solBest),1)
        if voti != votiBest:
            return voti > votiBest

        durata = sum(f.duration for f in parziale)
        durataB = sum(f.duration for f in self._solBest)
        if durata != durataB:
            return durata < durataB



