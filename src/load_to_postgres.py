import os
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Use .env.example as guide.")

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Success")
except Exception as e:
    print(f"The specific error is {e}")
    raise

records = pd.read_csv("./datasets/processed/cleaned_records.csv")
branches = pd.read_csv("./datasets/processed/cleaned_branches.csv")
categories = pd.read_csv("./datasets/processed/cleaned_categories.csv")
sources = pd.read_csv("./datasets/processed/cleaned_sources.csv")

branches.to_sql("dim_branches", engine, if_exists="replace", index=False)
categories.to_sql("dim_categories", engine, if_exists="replace", index=False)
sources.to_sql("dim_sources", engine, if_exists="replace", index=False)
records.to_sql("fact_records", engine, if_exists="append", index=False)

print("Database load completed.")
print("Rows inserted into fact_records:", len(records))