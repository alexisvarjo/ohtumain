class Sovelluslogiikka:
    def __init__(self):
        self._arvo = 0
        self._edellinen_arvo = 0

    def arvo(self):
        return self._arvo

    def _talleta_edellinen(self):
        self._edellinen_arvo = self._arvo

    def plus(self, arvo):
        self._talleta_edellinen()
        self._arvo = self._arvo + arvo

    def miinus(self, arvo):
        self._talleta_edellinen()
        self._arvo = self._arvo - arvo

    def nollaa(self):
        self._talleta_edellinen()
        self._arvo = 0

    def kumoa(self):
        self._arvo, self._edellinen_arvo = self._edellinen_arvo, self._arvo
