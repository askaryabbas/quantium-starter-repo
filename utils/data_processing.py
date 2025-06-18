import os
import pandas as pd

def load_and_process_data(data_folder="data"):
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    dfs = []

    for file in csv_files:
        file_path = os.path.join(data_folder, file)
        try:
            df = pd.read_csv(file_path)
            if not df.empty and "product" in df.columns:
                dfs.append(df)
        except pd.errors.EmptyDataError:
            print(f"Skipped empty file: {file}")
        except Exception as e:
            print(f"Failed to read {file}: {e}")

    if not dfs:
        raise ValueError("No valid CSV files found in the directory.")

    combined_df = pd.concat(dfs, ignore_index=True)

    # Filter only pink morsel
    pink_df = combined_df[combined_df["product"] == "pink morsel"].copy()

    # Clean price and calculate sales
    pink_df["price"] = pink_df["price"].replace('[\$,]', '', regex=True).astype(float)
    pink_df["sales"] = pink_df["price"] * pink_df["quantity"]

    # Return only required columns
    return pink_df[["sales", "date", "region"]]
