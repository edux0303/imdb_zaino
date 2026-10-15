import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        v =  self._view._txtV.value
        try:
            v = int(v)
        except ValueError:
            self._errore("v deve essere un numero intero!")
            return
        if v <= 0:
            self._errore("v deve essere maggiore di 0!")
            return

        self._model.buildGraph(v)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con almeno {v} voti"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view._ddFilm1.options.clear()
        self._view._ddFilm2.options.clear()
        self._view._ddFilm1.value = None
        self._view._ddFilm2.value = None
        for r in self._model.getNodiOrdinati():
            self._view._ddFilm1.options.append(ft.dropdown.Option(key=r.id, text=r.title))
            self._view._ddFilm2.options.append(ft.dropdown.Option(key=r.id, text=r.title))
        self._view.update_page()

    def handleConnessione(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {self._model.getNumeroConnesse()}"))
        componente = self._model.getComponenteMax()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente più grande ha {len(componente)} film:"))

        f1 = self._view._ddFilm1.value
        f2 = self._view._ddFilm2.value
        if f1 is None or f2 is None:
            self._errore("Seleziona un film")
            return
        film1 = self._model.idMap[f1]
        film2 = self._model.idMap[f2]
        cammino, archi = self._model.getCamino(film1,film2)
        if len(cammino) == 0:
            self._errore(f"Nessun cammino tra {film1} e {film2}")
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino minimo da {film1} a {film2}: {len(cammino) - 1} archi"))

        for f in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{f}"))
        self._view.update_page()



        # 1. grafo vuoto? -> errore
        # 2. leggi _ddFilm1.value e _ddFilm2.value: se uno è None -> errore
        # 3. f1 e f2 con self._model._idMap[...]
        # 4. cammino = self._model.getCammino(f1, f2)
        # 5. se cammino è vuoto -> "nessun cammino tra f1 e f2"
        #    altrimenti stampa i film in ordine e il numero di archi (len(cammino) - 1)
        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleMaratona(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        f1 = self._view._ddFilm1.value
        if f1 is None:
            self._errore("Seleziona il film di partenza in Film 1!")
            return
        film1 = self._model.idMap[f1]

        try:
            D = int(self._view._txtD.value)
        except (ValueError, TypeError):
            self._errore("D deve essere un numero intero!")
            return
        if D <= 0:
            self._errore("D deve essere maggiore di 0!")
            return

        if film1.duration > D:
            self._errore(f"{film1} dura {film1.duration} minuti: più di {D}!")
            return

        scelti = self._model.getMaratona(film1, D)

        self._view.txt_result.controls.append(ft.Text(f"Maratona con {film1} in al massimo {D} minuti:"))
        for f in scelti:
            self._view.txt_result.controls.append(
                ft.Text(f"{f} - {f.duration} min, voto {f.avg_rating}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di film: {len(scelti)}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Durata totale: {sum(f.duration for f in scelti)} min"))
        self._view.txt_result.controls.append(
            ft.Text(f"Somma dei voti: {sum(f.avg_rating for f in scelti):.1f}"))
        self._view.update_page()
