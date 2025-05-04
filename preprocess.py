# preprocess.py

import pandas as pd
import re
import string

def load_data(path='UpdatedResumeDataSet.csv'):
    df = pd.read_csv(path)
    return df

def clean_text(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower().strip()

def preprocess_resumes(df):
    df['cleaned'] = df['Resume'].apply(clean_text)
    return df
