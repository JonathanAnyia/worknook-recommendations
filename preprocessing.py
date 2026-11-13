import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(filepath):
    df = pd.read_csv(filepath)  # Load dataset
    df.dropna(inplace=True)  # Remove missing values
    return df

def split_data(df):
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    return train, test

if __name__ == "__main__":
    data = load_data("data/dataset.csv")
    train, test = split_data(data)
    print(train.head())