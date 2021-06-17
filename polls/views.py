from django.shortcuts import render, redirect

from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.


def show_index(request):
    return render(request, 'index.html')


def show_q3_region(request):
    return render(request, 'q3/region.html')


def show_q3_school(request):
    return render(request, 'q3/school.html')


@xframe_options_exempt
def show_q3_total(request):
    return render(request, 'q3/total.html')


def show_q1_q2_grade_count(request):
    return render(request, 'q1_q2/grade_count.html')


def show_q1_q2_grid(request):
    return render(request, 'q1_q2/grid.html')


def show_q1_q2_school_count(request):
    return render(request, 'q1_q2/school_count.html')


def show_q4_q9_q10_q11(request):
    return render(request, 'q4_q9_q10_q11/q4_q9_q10_q11.html')


def show_q5(request):
    return render(request, 'q5/course_time.html')


def show_q6_q7_grade(request):
    return render(request, 'q6_q7/grade_study_state.html')


def show_q6_q7_region(request):
    return render(request, 'q6_q7/region_study_state.html')


def show_q6_q7_school(request):
    return render(request, 'q6_q7/school_study_state.html')


def show_q8_grade(request):
    return render(request, 'q8/grade_rely.html')


def show_q8_region(request):
    return render(request, 'q8/region_rely.html')


def show_q8_school(request):
    return render(request, 'q8/school_rely.html')


def show_q12_region(request):
    return render(request, 'q12/region.html')


def show_q12_school(request):
    return render(request, 'q12/school.html')


def show_q12_total(request):
    return render(request, 'q12/total.html')


def show_q13(request):
    return render(request, 'q13/problem_count.html')


def show_q14_region(request):
    return render(request, 'q14/region.html')


def show_q14_school(request):
    return render(request, 'q14/school.html')


def show_q14_total(request):
    return render(request, 'q14/total.html')


def show_q15_region(request):
    return render(request, 'q15/region.html')


def show_q15_school(request):
    return render(request, 'q15/school.html')


def show_q15_total(request):
    return render(request, 'q15/total.html')


def show_q16_grade(request):
    return render(request, 'q16/grade.html')


def show_q16_region(request):
    return render(request, 'q16/region.html')


def show_q16_school(request):
    return render(request, 'q16/school.html')


def show_q17_region(request):
    return render(request, 'q17/region.html')


def show_q17_school(request):
    return render(request, 'q17/school.html')


def show_q17_total(request):
    return render(request, 'q17/total.html')


def show_q18_region(request):
    return render(request, 'q18/region.html')


def show_q18_school(request):
    return render(request, 'q18/school.html')


def show_q18_total(request):
    return render(request, 'q18/total.html')


def show_q19_region(request):
    return render(request, 'q19/region.html')


def show_q19_school(request):
    return render(request, 'q19/school.html')


def show_q19_total(request):
    return render(request, 'q19/total.html')


def show_q20_region(request):
    return render(request, 'q20/region.html')


def show_q20_school(request):
    return render(request, 'q20/school.html')


def show_q20_total(request):
    return render(request, 'q20/total.html')


def show_squirrel(request):
    return render(request, '../static/images/squirrel.png')