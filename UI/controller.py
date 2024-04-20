import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        umidita_media = self._model.get_umidita_media(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"L'umidita media nel mese selezionato é:"))
        for citta_media in umidita_media:
            self._view.lst_result.controls.append(ft.Text(f"{citta_media[0]}: {citta_media[1]}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza_ottima, costo = self._model.get_sequenza_ottima(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
        for stop in sequenza_ottima:
            self._view.lst_result.controls.append(ft.Text(stop))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

