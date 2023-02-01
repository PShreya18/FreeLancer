from django.http import HttpResponse
from django.shortcuts import render
from IPython.display import  HTML
from CourseRecommendation.RecommendCourse import course_indices,cosine_sim_mat,df,pd


def course(request):
    return render(request, 'courses.html')


def recommend_course(request):
    title = request.POST['course']
    num_of_rec = int(request.POST['rec_no'])
    print(title,num_of_rec)
    # ID for title
    idx = course_indices[str(title)]
    # Course Indice
    # Search inside cosine_sim_mat
    scores = list(enumerate(cosine_sim_mat[idx]))
    # Scores
    # Sort Scores
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # Recommend
    selected_course_indices = [i[0] for i in sorted_scores[1:]]
    selected_course_scores = [i[1] for i in sorted_scores[1:]]
    result = df['course_title'].iloc[selected_course_indices]
    rec_df = pd.DataFrame(result)
    rec_df['similarity_scores'] = selected_course_scores
    df_new = df[df.course_title.isin(rec_df.head(num_of_rec)['course_title'])]
    df_new=df_new[['course_id', 'course_title', 'url', 'price', 'num_subscribers', 'level']]
    #HTML(df_new.to_html(classes='table table-striped'))
    return HttpResponse((df_new.to_html(classes="table table-striped table-hover")))
