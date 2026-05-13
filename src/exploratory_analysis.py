import pandas as pd

records = pd.read_csv("./datasets/raw/records_raw_messy.csv")
branches = pd.read_csv("./datasets/raw/branches_reference.csv")
categories = pd.read_csv("./datasets/raw/categories_reference.csv")
sources = pd.read_csv("./datasets/raw/sources_reference.csv")

records["record_date"] = pd.to_datetime(records["record_date"], errors="coerce")
records["raw_value"] = pd.to_numeric(records["raw_value"], errors="coerce")
records["normal_sign"] = pd.to_numeric(records["normal_sign"], errors="coerce")
records = records.dropna(subset=["record_date", "raw_value", "normal_sign"])
records["signed_value"] = records["raw_value"] * records["normal_sign"]

records.to_csv("./datasets/processed/cleaned_records.csv", index=False)
branches.to_csv("./datasets/processed/cleaned_branches.csv", index=False)
categories.to_csv("./datasets/processed/cleaned_categories.csv", index=False)
sources.to_csv("./datasets/processed/cleaned_sources.csv", index=False)

print("Cleaned files saved successfully.")
print(categories)