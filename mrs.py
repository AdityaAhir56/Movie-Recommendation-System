import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import ast

# Load and preprocess data
credits_df = pd.read_csv(r"C:\Users\adity\Projects\Movie recommendation system\data\credits.csv")
movies_df = pd.read_csv(r"C:\Users\adity\Projects\Movie recommendation system\data\movies.csv")

movies_df = movies_df.merge(credits_df, on="title")
movies_df = movies_df[["movie_id", "title", "cast", "crew", "tagline", "genres", "keywords", "spoken_languages", "overview"]]
movies_df.dropna(inplace=True)

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)
movies_df['spoken_languages'] = movies_df['spoken_languages'].apply(convert)

def convert_cast(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

movies_df['cast'] = movies_df['cast'].apply(convert_cast)

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies_df['crew'] = movies_df['crew'].apply(fetch_director)

movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
movies_df['tagline'] = movies_df['tagline'].apply(lambda x: x.split())
movies_df['genres'] = movies_df['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df['keywords'] = movies_df['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df['cast'] = movies_df['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df['crew'] = movies_df['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies_df['tags'] = movies_df['cast'] + movies_df['crew'] + movies_df['tagline'] + movies_df['genres'] + movies_df['keywords'] + movies_df['spoken_languages'] + movies_df['overview']

new_df = movies_df[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: ' '.join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(new_df.iloc[i[0]].title)
    return recommended_movies