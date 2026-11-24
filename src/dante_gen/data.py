"""Load the raw Dante texts and build one clean corpus table."""

import logging
import re
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

COLUMNS = ["work", "form", "poem_type", "section", "unit", "verse_number", "text"]
ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(roman: str) -> int:
    """Convert a Roman numeral to an integer"""

    total = 0
    for i, letter in enumerate(roman):
        value = ROMAN_VALUES[letter]
        if i + 1 < len(roman) and value < ROMAN_VALUES[roman[i + 1]]:
            total -= value
        else:
            total += value
    return total


def clean_text(text: str) -> str:
    """Remove markup and normalise punctuation in a verse or paragraph."""
    text = text.replace("}}", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[[IVXLC]+\]\s*", "", text)
    text = text.replace("’", "'")
    text = text.replace("«", '"').replace("»", '"')
    return text.strip()


def load_commedia(path: Path) -> pd.DataFrame:
    """Divina Commedia: poem_type is the cantica, section the canto, unit the tercet."""
    df = pd.read_parquet(path)
    df = df.rename(
        columns={"volume": "poem_type", "canto": "section", "tercet": "unit"}
    )
    df["section"] = df["section"].str.removeprefix("Canto ").map(roman_to_int)
    df["work"] = "divina_commedia"
    df["form"] = "verse"
    return df[COLUMNS]


def load_vita_nuova_poetry(path: Path) -> pd.DataFrame:
    """Vita Nuova poems: section is the chapter, unit the poem within the chapter."""
    df = pd.read_csv(path)
    df = df.rename(
        columns={"chapter_number": "section", "poem_index_in_chapter": "unit"}
    )
    df["work"] = "vita_nuova"
    df["form"] = "verse"
    return df[COLUMNS]


def load_vita_nuova_prose(path: Path) -> pd.DataFrame:
    """Vita Nuova prose: section is the chapter, unit the paragraph; no verse number."""
    df = pd.read_csv(path)
    df = df.rename(columns={"chapter_number": "section", "paragraph_index": "unit"})
    df["work"] = "vita_nuova"
    df["form"] = "prose"
    df["poem_type"] = "prose"
    df["verse_number"] = pd.NA
    return df[COLUMNS]


def build_corpus(raw_dir: Path) -> pd.DataFrame:
    """Combine the three raw files into one clean table with the COLUMNS schema."""
    corpus = pd.concat(
        [
            load_commedia(raw_dir / "divina_commedia.parquet"),
            load_vita_nuova_poetry(raw_dir / "vita_nuova_poetry.csv"),
            load_vita_nuova_prose(raw_dir / "vita_nuova_prose.csv"),
        ],
        ignore_index=True,
    )
    corpus["verse_number"] = corpus["verse_number"].astype("Int64")
    corpus["text"] = corpus["text"].map(clean_text)
    logger.info("Built corpus with %d rows", len(corpus))
    return corpus
