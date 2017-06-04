from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from ask.models import *
import numpy as np


def pagination(request, data, count, page):
  paginator = Paginator(data, count)
  get = request.GET.get('page')
  if get:
    page = int(get)
  try: 
    paginator_datas_list = paginator.page(int(page))
  except PageNotAnInteger: 
    data_list = paginator.page(1)
  except EmptyPage:
    paginator_datas_list = paginator.page(paginator.num_pages)
  return paginator_datas_list


def randomTags(Tag):
	tags = []
	for i in range(Tag.objects.count()):
		tags.append(str(Tag.objects.get_queryset()[i]))
	np.random.shuffle(tags)
	return tags[:3]


class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(
                content = json.dumps(kwargs),
                content_type = 'application/json',
                )


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
                status = 'error', code = code, message = message
                )


def login_required_ajax(func):
    def check(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        return helpers.HttpResponseAjaxError(
                code = "no_auth",
                message = 'login required',
                )
    return check
