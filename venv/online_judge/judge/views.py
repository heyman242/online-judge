from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Questions, CodeSnippet
from django.http import JsonResponse
from .forms import CodeSnippetForm


def questions(request):
    myquestions = Questions.objects.all()
    context = {
        'myquestions': myquestions,
    }
    return render(request, 'all_questions.html', context)


def details(request, id, ):
    myquestion = get_object_or_404(Questions, id=id)
    context = {
        'myquestions': myquestion,
    }
    return render(request, 'details.html', context)


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())


def create_code_snippet(request, id):
    question = Questions.objects.get(id=id)
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            code_snippet = form.save(commit=False)
            code_snippet.question = question
            code_snippet.save()
            return redirect('code_snippet_list')
    else:
        form = CodeSnippetForm()
    return render(request, 'create_code_snippet.html', {'form': form, 'question': question})
