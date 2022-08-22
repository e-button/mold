from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.models import Staff, Machine, Process, MoldData
# Create your views here.
import traceback
import json
from app.tool import convert_datetime_timezone
def getCurrentTime():
    import time
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t
def doWork_view(request):
    if request.method == 'GET':
        staffs = Staff.objects.all()
        machines = Machine.objects.all()
        processes = Process.objects.all()
        return render(request, 'doWork.html', {
            'staffs': staffs,
            'machines': machines,
            'processes': processes,
            'nav': 1
        })
    return HttpResponseForbidden()

def allWorks_view(request):
        if request.method == 'GET':
            staffs = Staff.objects.all()
            return render(request, 'myWork.html', {
                'staffs': staffs,
                'nav': 2
            })
        return HttpResponseForbidden()

@csrf_exempt
def staff_view(request, id):
    if request.method == 'GET':
        try:
            return render(request, 'staff.html')
        except:
            traceback.print_exc()
            return HttpResponseForbidden()
    elif request.method == 'POST':
        try:
            staff = Staff.objects.get(id=id)
            works = MoldData.objects.filter(staff=staff).order_by('-start_time')

            res = {
                'code': 1,
                'msg': '查詢成功',
                'works': []
            }
            for work in works:
                data_dict = {}
                data_dict['id'] = work.id
                data_dict['start_time'] = convert_datetime_timezone(str(work.start_time).split('.')[0].split('+')[0], 'UTC', 'Asia/Taipei').replace(' ', '<br>')
                try:
                    data_dict['end_time'] = convert_datetime_timezone(str(work.end_time).split('.')[0].split('+')[0], 'UTC', 'Asia/Taipei').replace(' ', '<br>')
                except:
                    data_dict['end_time'] = 'None'
                data_dict['status'] = work.status
                data_dict['staff_name'] = work.staff.name
                data_dict['machine_no'] = work.machine.no
                data_dict['process_type'] = work.process.type
                data_dict['mod_no'] = work.mod_no
                data_dict['status'] = work.status

                res['works'].append(data_dict)
            res = json.dumps(res)
            return HttpResponse(res, content_type="application/json")
        except:
            traceback.print_exc()
            return JsonResponse({
                'code': 0,
                'msg': '查詢失敗'
            })
    return HttpResponseForbidden()

@csrf_exempt
def singleWork_view(request, id):
    if request.method == 'GET':
        try:
            work = MoldData.objects.get(id=id)
            return render(request, 'sigleWork.html', {
                'work': work
            })
        except:
            traceback.print_exc()
            return HttpResponseForbidden()
    return HttpResponseForbidden()

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        try:
            staff_id = request.POST.get('staff_id', '')
            machine_id = request.POST.get('machine_id', '')
            process_id = request.POST.get('process_id', '')
            mod_no = request.POST.get('mod_no', '')

            staff = Staff.objects.get(id=staff_id)
            machine = Machine.objects.get(id=machine_id)
            process = Process.objects.get(id=process_id)

            m = MoldData(
                # start_time=getCurrentTime(),
                staff=staff,
                machine=machine,
                process=process,
                mod_no=mod_no
            )
            m.save()
            return JsonResponse({
                'code': 1,
                'msg': '報工成功'
            })
        except:
            traceback.print_exc()
            return JsonResponse({
                'code': 0,
                'msg': '報工失敗'
            })
    return HttpResponseForbidden()

@csrf_exempt
def finish(request, id):
    if request.method == 'POST':
        try:
            m = MoldData.objects.get(id=id)
            m.status = 1
            m.end_time = getCurrentTime()
            m.save()
            return JsonResponse({
                'code': 1,
                'msg': '完工成功'
            })
        except:
            traceback.print_exc()
            return JsonResponse({
                'code': 0,
                'msg': '完工失敗'
            })
    return HttpResponseForbidden()


def hello(request):
    from app.test import haha
    haha()

