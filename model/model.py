import copy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self._costo_minimo = -1
        self._sequenza_ottima = []

    def calcola_umidita_media(self, mese):
        return MeteoDao.get_umidita_media_mese(mese)

    def calcola_sequenza(self, mese):
        self._costo_minimo = -1
        self._sequenza_ottima = []
        situazioni_meta_mese = MeteoDao.get_situazione_meta_mese(mese)
        self._ricorsione([], situazioni_meta_mese)
        return self._sequenza_ottima, self._costo_minimo

    def _ricorsione(self, parziale, situazioni):
        #caso terminale:
        if len(parziale) == 15:
            print(parziale)
            costo = self._calcola_costo(parziale)
            if (self._costo_minimo == -1) or (costo < self._costo_minimo):
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
        else:
            day = len(parziale)+1
            for situazione in situazioni[(day-1)*3:day*3]:
                #if situazione.data.day == day:
                if self._vincoli_soddisfatti(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, situazioni)
                    parziale.pop()

    def _vincoli_soddisfatti(self, parziale, situazione) -> bool:
        #Vincolo 1) check che non sono stato gia 6 giorni nella citta
        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter += 1
        if counter >= 6:
            return False

        # Vincolo 2) check che  il tecnicno si fermi almeno tre giorni consecutivi
        # se la sequenza ha 1 o due elementi, posso solo rimettere il primo
        if len(parziale) <= 2 and len(parziale) > 0:
            if situazione.localita != parziale[0].localita:
                return False
        # se la mia parziale ha almeno 3 elementi, devo controllare gli ultimi 3
        # e vedere se il tecnico si è fermato almeno tre giorni di fila nello stesso posto
        elif len(parziale) > 2:
            sequenza_finale = parziale[-3:] # <- ultimi 3 giorni in parziale
            prima_fermata = sequenza_finale[0].localita # < primo di questi ultimi tre giorni
            counter = 0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter += 1
            if (counter < 3) and situazione.localita != sequenza_finale[-1].localita:
                return False
        # Ho soddisfatto tutti i vincoli
        return True

    def _calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            # 1) costo dell'umidita
            costo += parziale[i].umidita
            if i == 2: #primi due giorni
                if (parziale[i].localita != parziale[0].localita):
                    costo += 100
            elif i > 2: # altri giorni
                ultime_fermate = parziale[i-2:i+1]
                if (ultime_fermate[2].localita != ultime_fermate[0].localita
                        or ultime_fermate[2].localita != ultime_fermate[1].localita):
                    costo += 100
        return costo