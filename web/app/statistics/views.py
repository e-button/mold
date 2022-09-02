import traceback

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
from app.models import Statistics
import secrets
import os
from app.statistics.func import main, make_excel
import shutil
import threading

def statistics(request):
    ss = Statistics.objects.all().order_by('-id')

    if request.method == 'GET':
        return render(request, 'statistics.html', {
            'nav': 3,
            'ss': ss
        })

    return HttpResponseForbidden()

def statistic(request, id):
    try:
        s = Statistics.objects.get(id=id)
        return render(request, 'statistic.html', {
            'nav': 3,
            's': s
        })
    except:
        pass

@csrf_exempt
def generate(request):
    token = secrets.token_hex(16)
    try:
        s = Statistics.objects.create(
            path=token
        )
        s.save()
        if not os.path.isdir(f'statistics_files/{token}/'):
            print(os.getcwd())
            os.mkdir(f'statistics_files/{token}/')

        make_excel(token)

        main(token)

        # main(token, 1)
        # main(token, 2)

        #
        # t1 = threading.Thread(target=main, args=(token, 1, ))
        # t2 = threading.Thread(target=main, args=(token, 2,))
        # t2.start()
        # t1.start()
        # t2.join()
        # t1.join()

        return JsonResponse({
            'code': 1,
            'msg': '生成成功'
        })
    except:
        traceback.print_exc()
        return JsonResponse({
            'code': 0,
            'msg': '生成失敗'
        })

def file_view(request):
    id = request.GET.get('id', '')
    type = request.GET.get('type', '')
    order = request.GET.get('order', '')
    try:
        s = Statistics.objects.get(id=id)
        token = s.path
        if type == 'image':
            with open(os.getcwd()+f'/statistics_files/{token}/{order}.png', "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        elif type == 'excel':
            f = open(os.getcwd()+f'/statistics_files/{token}/mold_analysis.xlsx', "rb")
            return FileResponse(f)
    except:
        traceback.print_exc()
        return HttpResponse('File Not Found')

@csrf_exempt
def delete(request):
    id = request.POST.get('id', '')
    try:
        s = Statistics.objects.get(id=id)

        token = s.path
        token_path = f'statistics_files/{token}/'

        shutil.rmtree(token_path)

        s.delete()
        return JsonResponse({
            'code': 1,
            'msg': '刪除成功'
        })
    except:
        return JsonResponse({
            'code': 0,
            'msg': '刪除失敗'
        })