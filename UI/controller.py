import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # PUNTO 1 ----------------------------------------------------------
    # Metodo per riempire il dropdown
    def fillDDYear(self):
        years = self._model.getYears()

        yearssDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddAnno1.options = yearssDD
        self._view._ddAnno2.options = yearssDD

        self._view.update_page()
    # FINE PUNTO 1 ------------------------------------------------------

    # PUNTO 2 ----------------------------------------------------------
    def handleCreaGrafo(self,e):

        self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
        n = self._model.getNumNodes()
        m = self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))

        self._view.update_page()
    # FINE PUNTO 2 ----------------------------------------------------------

    # PUNTO 3 ----------------------------------------------------------
    def handleDettagli(self, e):

        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore: "))
        top_3 = self._model.get_top_3_archi()
        for u, v, data in top_3:
            self._view.txt_result.controls.append(
                ft.Text(f"{u.constructorRef} -> {v.constructorRef} ({data['weight']} piloti condivisi)"))

        numComp, componente_max, comp_max_ordinata = self._model.getConnectedComponents()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numComp} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(componente_max)} nodi):"))
        for c in componente_max:
            self._view.txt_result.controls.append(ft.Text(f"{c}"))

        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa in ordine decrescente di grado dei nodi."))
        for d in comp_max_ordinata:
            self._view.txt_result.controls.append(ft.Text(f"{d[0]} (grado = {d[1]})"))

        self._view.update_page()
    # FINE PUNTO 3 ----------------------------------------------------------



    def handleCerca(self, e):
        pass

