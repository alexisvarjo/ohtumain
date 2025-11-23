import unittest
from unittest.mock import ANY, Mock

from kauppa import Kauppa
from tuote import Tuote
from varasto import Varasto
from viitegeneraattori import Viitegeneraattori


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()

        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        # Oletusarvo: varastossa on tuotetta
        def saldo(tuote_id):
            # Testit voivat ylikirjoittaa side_effectin, mutta tämä toimii defaultina
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 5
            if tuote_id == 3:
                return 0
            return 0

        def hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            if tuote_id == 3:
                return Tuote(3, "olut", 7)
            return None

        self.varasto_mock.saldo.side_effect = saldo
        self.varasto_mock.hae_tuote.side_effect = hae_tuote

        self.kauppa = Kauppa(
            self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_yksi_tuote_ostos_kutsuu_pankkia_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_kaksi_eri_tuotetta_ostos_kutsuu_pankkia_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # hinta 5
        self.kauppa.lisaa_koriin(2)  # hinta 3
        self.kauppa.tilimaksu("matti", "99999")

        self.pankki_mock.tilisiirto.assert_called_with(
            "matti", 42, "99999", "33333-44455", 5 + 3
        )

    def test_kaksi_samaa_tuotetta_ostos_kutsuu_pankkia_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("liisa", "11111")

        self.pankki_mock.tilisiirto.assert_called_with(
            "liisa", 42, "11111", "33333-44455", 5 + 5
        )

    def test_yksi_tuote_saatavilla_ja_yksi_loppu_ostos_kutsuu_pankkia_oikeilla_parametreilla(
        self,
    ):
        # tuote 1 on varastossa: saldo=10
        # tuote 3 on loppu: saldo=0
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # lisätään
        self.kauppa.lisaa_koriin(3)  # ei lisätä
        self.kauppa.tilimaksu("sami", "22222")

        self.pankki_mock.tilisiirto.assert_called_with(
            "sami",
            42,
            "22222",
            "33333-44455",
            5,  # vain tuote 1
        )

    def test_aloita_asiointi_nollaa_ostoskorin(self):
        # Ensimmäinen asiointi
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # 5e

        # Toinen asiointi – pitää nollata ostoskori
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # 3e

        self.kauppa.tilimaksu("anne", "00000")

        # Tarkistetaan että hinta on vain 3, ei 8
        self.pankki_mock.tilisiirto.assert_called_with(
            "anne", 42, "00000", "33333-44455", 3
        )

    def test_uusi_viitenumero_joka_maksulle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("eka", "11111")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("toka", "22222")

        # kaksi maksua → kaksi viitteen hakua
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_poista_korista_kutsuu_varastoa_ja_vahentaa_summaa(self):
        # Tämä testi nostaa kattavuuden lähelle 100 %
        # koska poista_korista-metodi ei aiemmin tullut testatuksi

        self.kauppa.aloita_asiointi()

        # varastossa tuote 1 on 10 kpl
        self.kauppa.lisaa_koriin(1)  # +5
        self.kauppa.lisaa_koriin(2)  # +3

        # poistetaan tuote 1
        self.kauppa.poista_korista(1)

        self.kauppa.tilimaksu("teppo", "33333")

        # jäljellä vain tuote 2 → summa = 3
        self.pankki_mock.tilisiirto.assert_called_with(
            "teppo", 42, "33333", "33333-44455", 3
        )

        # Varmistetaan että varasto kutsuttiin palauttamaan tuote 1
        tuote_1 = self.varasto_mock.hae_tuote(1)
        self.varasto_mock.palauta_varastoon.assert_called_with(tuote_1)

    if __name__ == "__main__":
        unittest.main()
