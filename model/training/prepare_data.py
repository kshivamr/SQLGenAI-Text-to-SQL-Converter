import pandas as pd
import json
from sklearn.model_selection import train_test_split

input_file = "../../data/raw/spider/spider_text_sql.csv"

train_file = "../../data/processed/train.json"
validation_file = "../../data/processed/validation.json"

df = pd.read_csv(input_file)

train_df, validation_df = train_test_split(
    df,
    test_size=0.1,
    random_state=42
)

def convert_to_messages(dataframe):
    data = []

    for _, row in dataframe.iterrows():
        data.append({
            "messages": [
                {
                    "role": "user",
                    "content": f"Convert the following question into SQL:\n\n{row['text_query']}"
                },
                {
                    "role": "assistant",
                    "content": row["sql_command"]
                }
            ]
        })

    return data

train_data = convert_to_messages(train_df)
validation_data = convert_to_messages(validation_df)

with open(train_file, "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2, ensure_ascii=False)

with open(validation_file, "w", encoding="utf-8") as f:
    json.dump(validation_data, f, indent=2, ensure_ascii=False)

print(f"Training examples: {len(train_data)}")
print(f"Validation examples: {len(validation_data)}")