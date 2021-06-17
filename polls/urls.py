from django.urls import path
from polls import views

app_name = 'polls'

urlpatterns = [
    path('', views.show_index, name='index'),

    path('q1_q2/grade_count', views.show_q1_q2_grade_count, name='show_q1_q2_grade_count'),
    path('q1_q2/grid', views.show_q1_q2_grid, name='show_q1_q2_grid'),
    path('q1_q2/school_count', views.show_q1_q2_school_count, name='show_q1_q2_school_count'),

    path('q3/region', views.show_q3_region, name='show_q3_region'),
    path('q3/school', views.show_q3_school, name='show_q3_school'),
    path('q3/total', views.show_q3_total, name='show_q3_total'),

    path('q4_q9_q10_q11/', views.show_q4_q9_q10_q11, name='show_q4_q9_q10_q11'),

    path('q5/', views.show_q5, name='show_q5'),

    path('q6_q7/grade', views.show_q6_q7_grade, name='show_q6_q7_grade'),
    path('q6_q7/region', views.show_q6_q7_region, name='show_q6_q7_region'),
    path('q6_q7/school', views.show_q6_q7_school, name='show_q6_q7_school'),

    path('q8/grade', views.show_q8_grade, name='show_q8_grade'),
    path('q8/region', views.show_q8_region, name='show_q8_region'),
    path('q8/school', views.show_q8_school, name='show_q8_school'),

    path('q12/region', views.show_q12_region, name='show_q12_region'),
    path('q12/school', views.show_q12_school, name='show_q12_school'),
    path('q12/total', views.show_q12_total, name='show_q12_total'),

    path('q13/', views.show_q13, name='show_q13'),

    path('q14/region', views.show_q14_region, name='show_q14_region'),
    path('q14/school', views.show_q14_school, name='show_q14_school'),
    path('q14/total', views.show_q14_total, name='show_q14_total'),

    path('q15/region', views.show_q15_region, name='show_q15_region'),
    path('q15/school', views.show_q15_school, name='show_q15_school'),
    path('q15/total', views.show_q15_total, name='show_q15_total'),

    path('q16/grade', views.show_q16_grade, name='show_q16_grade'),
    path('q16/region', views.show_q16_region, name='show_q16_region'),
    path('q16/school', views.show_q16_school, name='show_q16_school'),

    path('q17/region', views.show_q17_region, name='show_q17_region'),
    path('q17/school', views.show_q17_school, name='show_q17_school'),
    path('q17/total', views.show_q17_total, name='show_q17_total'),

    path('q18/region', views.show_q18_region, name='show_q18_region'),
    path('q18/school', views.show_q18_school, name='show_q18_school'),
    path('q18/total', views.show_q18_total, name='show_q18_total'),

    path('q19/region', views.show_q19_region, name='show_q19_region'),
    path('q19/school', views.show_q19_school, name='show_q19_school'),
    path('q19/total', views.show_q19_total, name='show_q19_total'),

    path('q20/region', views.show_q20_region, name='show_q20_region'),
    path('q20/school', views.show_q20_school, name='show_q20_school'),
    path('q20/total', views.show_q20_total, name='show_q20_total'),

    path('squirrel', views.show_squirrel, name='show_squirrel'),
]