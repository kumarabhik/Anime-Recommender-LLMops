# src/dataloader.py
import pandas as pd
from typing import Set

class AnimeDataLoader:
    def __init__(self, original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self) -> str:
        """
        Reads the original CSV, validates required columns, builds a combined text column,
        and writes a 1-column CSV to processed_csv. Returns processed_csv path.
        """
        # Use on_bad_lines="skip" (error_bad_lines is removed in recent pandas)
        df = pd.read_csv(self.original_csv, encoding="utf-8", on_bad_lines="skip")
        df = df.dropna()

        # Be careful with spelling; your code had `sypnopsis`.
        # Adjust this set to match the ACTUAL CSV headers exactly.
        # If your file really has 'sypnopsis', add it to the fallbacks below.
        required: Set[str] = {"Name", "Genres", "synopsis"}

        # If the file actually uses a misspelled column, try to remap it
        if "synopsis" not in df.columns and "sypnopsis" in df.columns:
            df = df.rename(columns={"sypnopsis": "synopsis"})

        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}. "
                             f"Found: {list(df.columns)}")

        df["combined_info"] = (
            "Title: " + df["Name"] + ".. Overview: " + df["synopsis"] + ".. Genres: " + df["Genres"]
        )

        # No leading space in the column name; fix encoding typo
        df[["combined_info"]].to_csv(self.processed_csv, index=False, encoding="utf-8")
        return self.processed_csv
