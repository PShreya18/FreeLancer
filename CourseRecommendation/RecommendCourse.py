# Load EDA Pkgs
import pandas as pd
import csv
import neattext.functions as nfx
# Load ML/Rc Pkgs
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from django.templatetags.static import static

# Load our dataset
df = pd.read_csv(("CourseRecommendation/static/udemy_courses.csv"))
# Clean Text:stopwords,special charac
df['clean_course_title'] = df['course_title'].apply(nfx.remove_stopwords)
# Clean Text:stopwords,special charac
df['clean_course_title'] = df['clean_course_title'].apply(nfx.remove_special_characters)

# Vectorize our Text
count_vect = CountVectorizer()
cv_mat = count_vect.fit_transform(df['clean_course_title'])

df_cv_words = pd.DataFrame(cv_mat.todense(), columns=count_vect.get_feature_names_out())

# Cosine Similarity Matrix
cosine_sim_mat = cosine_similarity(cv_mat)

# Get Course ID/Index
course_indices = pd.Series(df.index, index=df['course_title']).drop_duplicates()
idx = course_indices['How To Maximize Your Profits Trading Options']

scores = list(enumerate(cosine_sim_mat[idx]))
# Sort our scores per cosine score
sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
# Omit the First Value/itself
sorted_scores[1:]
# Selected Courses Indices
selected_course_indices = [i[0] for i in sorted_scores[1:]]
# Selected Courses Scores
selected_course_scores = [i[1] for i in sorted_scores[1:]]
recommended_result = df['course_title'].iloc[selected_course_indices]
rec_df = pd.DataFrame(recommended_result)
rec_df['similarity_scores'] = selected_course_scores


