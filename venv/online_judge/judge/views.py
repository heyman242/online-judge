from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Questions, Submission
from .forms import SubmissionForm
import subprocess
from django.http import JsonResponse


def questions(request):
    myquestions = Questions.objects.all()
    context = {
        'myquestions': myquestions,
    }
    return render(request, 'all_questions.html', context)


def details(request, id,):
    myquestion = get_object_or_404(Questions, id=id)
    #question = get_object_or_404(Questions, pk=question_id)
    submission = Submission(problem=myquestion)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = SubmissionForm(instance=submission)
    context = {
        'myquestions': myquestion,
        'form': form,
    }
    return render(request, 'details.html', context)


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

# def submit_code(request, question_id, problem_id):
#     question = get_object_or_404(Questions, pk=question_id)
#     submission = Submission(problem=question)
#
#     if request.method == 'POST':
#         form = SubmissionForm(request.POST, instance=submission)
#         if form.is_valid():
#             submission = form.save(commit=False)
#             submission.save()
#             return redirect('submission_detail', pk=submission.pk)
#     else:
#         form = SubmissionForm(instance=submission)
#
#     url = reverse('judge:submit_code', kwargs={'id': question_id, 'problem_id': problem_id})
#     return render(request, 'details.html', {'form': form, 'question': question, 'url': url})
