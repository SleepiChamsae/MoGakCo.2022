from datetime import datetime, timedelta
import random
import logging

from django import forms
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, ListView

from . import models

# TODO: 기록하기


class waiting(View):
    template_name = 'waiting.html'

    def get(self, request):
        time, buttonVision = self.getNextTime()
        return render(request, self.template_name, {'nextTime': time, 'buttonVision': buttonVision})

    # TODO: 리펙터링?

    @staticmethod
    def getNextTime() -> (datetime, bool):
        # 경고: utc 기준임
        lastTime = models.Time.objects.last()
        try:
            trueTime = lastTime.next_time
            assert trueTime is not None
        except AttributeError:
            trueTime = waiting.getNewTime()

        retVal = False
        logging.getLogger().error(timezone.now() > trueTime + timedelta(hours=1))
        logging.getLogger().error(trueTime)

        if timezone.now() > trueTime + timedelta(hours=1):
            target = models.Ranking.objects.all()
            target.delete()
            trueTime = waiting.getNewTime()
        elif timezone.now() > trueTime:
            retVal = True

        return trueTime, retVal

    # TODO: 에러 기록하기
    # https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
    # datetime.now()를 쓰게 되면 타입에러가 발생한다. 자세한 것은 잘 모르곘다.

    @staticmethod
    def getNewTime() -> datetime:
        nextTime = timezone.now() + waiting.makeRandomTimeDelta() - timedelta(seconds=timezone.now().second)
        models.Time.objects.create(next_time=nextTime)
        return nextTime

    @staticmethod
    def makeRandomTimeDelta() -> timedelta:
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return timedelta(hours=hour, minutes=minute)


class RankingInput(FormView):
    template_name = 'rankingName.html'

    def get(self, request, **kwargs):
        if not isRightTime():
            return render(request, 'waiting.html', {'alert': True})
        name = self.updateRanking(request)
        defualt_data = {'name': name}
        form = NameForm(defualt_data)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def updateRanking(request) -> str:
        client_ip = get_client_ip(request)
        if len(models.Ranking.objects.filter(user_ip=client_ip)) != 0:
            return models.Ranking.objects.get(user_ip=client_ip).user_name
        models.Ranking.objects.create(user_ip=client_ip, user_name=client_ip, time=timezone.now())
        return ''

    def post(self, request, **kwargs):
        if not isRightTime():
            return render(request, '', {'alert': True})
        form = NameForm(request.POST)
        if form.is_valid():
            self.changeName(request, form)
            return HttpResponseRedirect('/RankingList/')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def changeName(request, form):
        new_name = form.cleaned_data['name']
        client_ip = get_client_ip(request)
        target = models.Ranking.objects.filter(user_ip=client_ip).last()
        target.user_name = new_name
        target.save()


class NameForm(forms.Form):
    name = forms.CharField(label="Your name?", max_length=100)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def isRightTime() -> bool:
    tar = models.Time.objects.last().next_time
    return tar + timedelta(hours=1) > timezone.now() > tar


class RankingList(ListView):
    model = models.Ranking

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
