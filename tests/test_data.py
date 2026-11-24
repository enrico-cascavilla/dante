from pathlib import Path

import pytest

from dante_gen.data import COLUMNS, build_corpus, clean_text, roman_to_int

RAW_DIR = Path(__file__).parents[1] / "data" / "raw"


@pytest.fixture(scope="session")
def corpus():
    return build_corpus(RAW_DIR)


@pytest.mark.parametrize(
    "roman, expected", [("I", 1), ("IV", 4), ("IX", 9), ("XIV", 14), ("XXXIV", 34)]
)
def test_roman_to_int(roman, expected):
    assert roman_to_int(roman) == expected


def test_clean_text_removes_markup_and_normalise():
    assert clean_text(" l’amor}} </span>") == "l'amor"
    assert clean_text("[II] Poi che") == "Poi che"


def test_corpus_schema(corpus):
    assert list(corpus.columns) == COLUMNS


def test_commedia_is_complete(corpus):
    commedia = corpus[corpus["work"] == "divina_commedia"]
    assert len(commedia) == 14233
    assert commedia.groupby("poem_type")["section"].nunique().to_dict() == {
        "Inferno": 34,
        "Purgatorio": 33,
        "Paradiso": 33,
    }


def test_no_markup_left(corpus):
    assert not corpus["text"].str.contains(r"[{}<>’«»]").any()


def test_verse_number_missing_only_in_prose(corpus):
    missing = corpus["verse_number"].isna()
    assert (missing == (corpus["form"] == "prose")).all()
