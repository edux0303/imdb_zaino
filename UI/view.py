import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Maratona Film"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None
        self._txtV = None
        self._btnCreaGrafo = None
        self._ddFilm1 = None
        self._ddFilm2 = None
        self._btnConnessione = None
        self._txtD = None
        self._btnMaratona = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Maratona di film", color="blue", size=24)
        self._page.controls.append(self._title)

        # PUNTO 1
        self._txtV = ft.TextField(label="Min voti V", width=180, value="50000")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([self._txtV, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._ddFilm1 = ft.Dropdown(label="Film 1", width=350)
        self._ddFilm2 = ft.Dropdown(label="Film 2", width=350)
        self._btnConnessione = ft.ElevatedButton(text="Test Connessione",
                                                 on_click=self._controller.handleConnessione)
        row2 = ft.Row([self._ddFilm1, self._ddFilm2, self._btnConnessione],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # PUNTO 2
        self._txtD = ft.TextField(label="Durata max D (minuti)", width=200)
        self._btnMaratona = ft.ElevatedButton(text="Maratona",
                                              on_click=self._controller.handleMaratona)
        row3 = ft.Row([self._txtD, self._btnMaratona],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
