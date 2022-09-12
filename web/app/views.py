from django.http import HttpResponseForbidden, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.models import Staff, Machine, Process, MoldData
# Create your views here.
import traceback
import json
from app.tool import convert_datetime_timezone

def ridrectHome(request):
    return HttpResponseRedirect('/doWork')

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
            for staff in staffs:
                unm = len(MoldData.objects.filter(staff=staff).exclude(status=1))
                staff.unm = unm
            return render(request, 'allWork.html', {
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

            if work.times:
                times = work.times
                times = sorted(times.items())
            else:
                times = {}
            work.times = times
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

@csrf_exempt
def stop(request, id):
    if request.method == 'POST':
        try:
            m = MoldData.objects.get(id=id)
            m.status = -1
            stop_time = getCurrentTime()

            times = m.times
            if not times:
                i = 0
            else:
                i = len(times)
            if not times:
                times = {}
            times[str(i)] = {}
            times[str(i)]['stop_time'] = stop_time
            m.times = times
            m.save()
            return JsonResponse({
                'code': 1,
                'msg': '已暫停'
            })
        except:
            traceback.print_exc()
            return JsonResponse({
                'code': 0,
                'msg': '暫停失敗'
            })
    return HttpResponseForbidden()

@csrf_exempt
def con(request, id):
    if request.method == 'POST':
        try:
            m = MoldData.objects.get(id=id)
            m.status = 0
            continue_time = getCurrentTime()

            times = m.times
            print(times)
            i = len(times) - 1
            times[str(i)]['continue_time'] = continue_time
            m.times = times
            m.save()
            return JsonResponse({
                'code': 1,
                'msg': '已繼續'
            })
        except:
            traceback.print_exc()
            return JsonResponse({
                'code': 0,
                'msg': '繼續失敗'
            })
    return HttpResponseForbidden()

@csrf_exempt
def deleteWork(request):
    id = request.POST.get('id', '')
    try:
        s = MoldData.objects.get(id=id)
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

def hello(request):
    from app.test import haha
    haha()

