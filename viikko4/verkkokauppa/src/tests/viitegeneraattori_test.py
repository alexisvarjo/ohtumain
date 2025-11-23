from viitegeneraattori import Viitegeneraattori


def test_viitegeneraattori_palauttaa_kasvavan_viitteen():
    v = Viitegeneraattori()

    eka = v.uusi()  # pitäisi olla 2
    toka = v.uusi()  # pitäisi olla 3
    kolmas = v.uusi()  # 4

    assert eka == 2
    assert toka == 3
    assert kolmas == 4


def test_viitegeneraattori_sisainen_tila_kasvaa():
    v = Viitegeneraattori()

    v.uusi()
    assert v._seuraava == 2

    v.uusi()
    assert v._seuraava == 3
