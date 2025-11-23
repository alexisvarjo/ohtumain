import pytest

from kirjanpito import Kirjanpito
from tuote import Tuote
from varasto import Varasto


@pytest.fixture
def kirjanpito():
    return Kirjanpito()


@pytest.fixture
def varasto(kirjanpito):
    # injektoidaan uusi kirjanpito,
    # jotta testit eivät sotke globaalia olioita
    return Varasto(kirjanpito)


def test_hae_tuote_loytyy(varasto):
    tuote = varasto.hae_tuote(1)
    assert isinstance(tuote, Tuote)
    assert tuote.id == 1


def test_hae_tuote_ei_loydy(varasto):
    tuote = varasto.hae_tuote(999)
    assert tuote is None


def test_saldo_palauttaa_oikean_saldon(varasto):
    tuote = varasto.hae_tuote(1)
    assert varasto.saldo(tuote.id) == 100


def test_ota_varastosta_vahentaa_saldoa(varasto, kirjanpito):
    tuote = varasto.hae_tuote(1)
    ennen = varasto.saldo(1)

    varasto.ota_varastosta(tuote)

    assert varasto.saldo(1) == ennen - 1
    assert len(kirjanpito.tapahtumat) == 1
    assert "otettiin varastosta" in kirjanpito.tapahtumat[0]


def test_palauta_varastoon_kasvattaa_saldoa(varasto, kirjanpito):
    tuote = varasto.hae_tuote(2)
    ennen = varasto.saldo(2)

    varasto.palauta_varastoon(tuote)

    assert varasto.saldo(2) == ennen + 1
    assert len(kirjanpito.tapahtumat) == 1
    assert "palautettiin varastoon" in kirjanpito.tapahtumat[0]


def test_varasto_sisaltaa_oikeat_tuotteet_alustuksen_jalkeen(varasto):
    # tarkistetaan että alustus loi vähintään nämä tuotteet
    ids = {t.id for t in varasto._saldot.keys()}
    assert {1, 2, 3, 4, 5}.issubset(ids)
