from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question,Choice
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


# def index(request):
#     latest_question_list = Question.objects.filter(
#         pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
#     #template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     #return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)

class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question does not exist')
#     question = get_object_or_404(Question, pk=question_id)
#     #return HttpResponse("You're looking at question %s." % question_id)
#     context = {
#         'question': question,
#     }
#     return render(request,'polls/detail.html',context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    return render(request, 'polls/results.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
    print(question.choice_set.get(pk=1).votes)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))