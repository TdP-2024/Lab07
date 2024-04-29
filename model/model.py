import copy

from database.meteo_dao import MeteoDao
from model.situazione import Situazione


class Model:
    def __init__(self):
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def get_umidita_media(self, mese):
        return MeteoDao.get_umidita_media(mese)

    def get_situazioni_meta_mese(self, mese):
        return MeteoDao.get_situazioni_meta_mese(mese)

    def get_sequenza_ottima(self, mese):
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        self.__ricorsione_sequenza([], 0, self.get_situazioni_meta_mese(mese))
        return self.__sequenza_ottima, self.__costo_ottimo

    def __ricorsione_sequenza(self, parziale: list[Situazione], livello: int, situazioni_mese: list[Situazione]):
        if len(parziale) == 15:
            costo = self.__calcola_costo(parziale)
            if costo < self.__costo_ottimo or self.__costo_ottimo == -1:
                self.__costo_ottimo = costo
                self.__sequenza_ottima = copy.deepcopy(parziale)
        else:
            for i in range(livello * 3, (livello + 1) * 3):
                if self.__is_admissible(parziale, situazioni_mese[i]):
                    parziale.append(situazioni_mese[i])
                    self.__ricorsione_sequenza(parziale, livello + 1, situazioni_mese)
                    parziale.pop()


    def __calcola_costo(self, sequenza: list[Situazione]) -> int:
        """Funzione che calcola il costo di una sequenza di situazioni.
        :param sequenza: la sequenza di situazioni di cui calcolare il costo.
        :return: il costo della sequenza."""
        costo = 0
        # primo giorno
        costo += sequenza[0].umidita
        # secondo giorno
        costo += sequenza[1].umidita
        if sequenza[0].localita != sequenza[1].localita:
            costo += 100
        #altri giorni
        for i in range(2, len(sequenza)):
            sequenza_short = sequenza[i-2:i+1]
            costo += sequenza[i].umidita
            if sequenza_short[2].localita != sequenza_short[1].localita:
                costo += 100
            elif sequenza_short[2].localita != sequenza_short[0].localita:
                costo += 100
        return costo

    def __is_admissible(self, parziale: list[Situazione], situazione: Situazione) -> bool:
        """Funzione che verifica se, data una sequenza parziale, una situazione soddisfa i vincoli
        del problema e puà essere aggiunta.
        :param parziale: la sequenza parziale.
        :param situazione: la situazione di cui verificare l'ammissibilità"""
        #check che nessuna citta sia visitata piu' di 6 volte
        visite = {"Milano": 0, "Genova": 0, "Torino": 0}
        if len(parziale) >= 6:
            for stop in parziale:
                visite[stop.localita] += 1
            visite[situazione.localita] += 1

            # print(list(visite.values())>6)
            # for visita in visite.values():
            #     if visita > 6:
            #         return False
            if any(v > 6 for v in visite.values()):
                return False

        # check che il tecnico non si sposti prima di aver trascorso 3 giorni consecutivi nella stessa
        # citta
        if len(parziale) >= 3:
            last_stop = parziale[-1].localita
            permanenza = 0
            for stop in parziale[-3:]:
                if stop.localita == last_stop:
                    permanenza += 1
            if permanenza < 3 and situazione.localita != last_stop:
                return False
            else:
                return True
        else:
            for stop in parziale:
                if stop.localita != situazione.localita:
                    return False
            return True


if __name__ == "__main__":
    print("CIAO")








