from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from .FileParser import FileParser
from .forms import UploadFileForm
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import pandas
import os


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        try:
            fileExtension = request.FILES.get('file').name.split('.')[1]
            if fileExtension == 'xlsx':
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    vv = pandas.read_excel(form['file'].data)
                    fp = FileParser(vv)
                    return JsonResponse(fp.getResult())
            else:
                raise NotImplementedError()
        except NotImplementedError:
            return HttpResponse(status=452, reason=f"Expected .xlsx file but got .{fileExtension}")
        except KeyError:
            return HttpResponse(status=453, reason=f"The uploaded file doesn't contain the right fields!")
        except ZeroDivisionError:
            return HttpResponse(status=454, reason=f"Division by zero!")

