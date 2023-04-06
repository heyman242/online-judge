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
    return HttpResponse(template.render(request=request))


def create_code_snippet(request, id):
    question = Questions.objects.get(id=id)
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            print("1")
            code_snippet = form.save(commit=False)
            code_snippet.question = question
            code_snippet.save()
            print("3")
            return HttpResponse("create_code_snippet_success")
    else:
        form = CodeSnippetForm()
    return render(request, 'create_code_snippet.html', {'form': form, 'question': question})



