from django.shortcuts import render
import json
from control.models import Student, Region, District
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.forms import model_to_dict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def manage(function):
    def user_data(request:HttpRequest, *args, **kwargs):

        data = json.loads(request.body)
        student, student_created = Student.objects.get_or_create(telegram_id=data["telegram_id"])
        student.platform = 'telegram'
        student.certificate_id = f"{student.id}"
        
        student.save()
        
        sdata = model_to_dict(student, ['fio', 'phone', 'region', 'district', 'birthday', 'tgender', 'company', 'activity', 'job'])
        vlist = []

        regions = Region.objects.filter(available=True)
        response_data = {
            "student": model_to_dict(student), 
            "regions": list(map(lambda region: model_to_dict(region), regions))
        }
        if student.region:
            response_data["student"]["region"] = model_to_dict(student.region)
        if student.district:
            response_data["student"]["district"] = model_to_dict(student.district)
            
        try: 
            if data['field'] == "region_id":
                districts = District.objects.filter(available=True, region_id=data["value"])
                response_data["districts"] = list(map(lambda district: model_to_dict(district), districts))
        except: 
            pass

        if student.region: 
            districts = District.objects.filter(available=True, region_id=student.region.id)
            response_data["districts"] = list(map(lambda district: model_to_dict(district), districts))
        

        for key, value in sdata.items():
            vlist.append(value)
        if None not in vlist:
            response_data["status"] = "end"
        else:
            response_data["status"] = "start"

        student.save()
        return function(request, data, response_data, *args, **kwargs)

    return user_data



@csrf_exempt
@manage
def user(request:HttpRequest, data, response_data):
    response_data["code"] = 200
    return JsonResponse(json.dumps(response_data), safe=False)
    
    

@csrf_exempt
@manage
def answer(request:HttpRequest, data, response_data):
    student, student_created = Student.objects.get_or_create(telegram_id=data["telegram_id"])

    if data["field"] == "phone":
        try:
            ystudent = Student.objects.filter(phone=data["value"])[0]
            if ystudent.telegram_id is None or ystudent.telegram_id == '':
                ystudent.telegram_id = data["telegram_id"]
                ystudent.save()
                student.delete()
                student = ystudent

        except:pass


    setattr(student, data["field"], data["value"])
    
    sdata = model_to_dict(student, ['fio', 'phone', 'region', 'district', 'birthday', 'tgender', 'company', 'activity', 'job'])
    vlist = []

    for key, value in sdata.items():
        vlist.append(value)
        
    if None not in vlist:
        response_data["status"] = "end"
        student.status = "Сўровнома тўлдирилди"
    else:
        response_data["status"] = "start"
        student.status = "Рўйхатдан ўтмоқда"


    response_data["student"] = model_to_dict(student)
    if student.region:
        response_data["student"]["region"] = model_to_dict(student.region)
    if student.district:
        response_data["student"]["district"] = model_to_dict(student.district)

    student.save()

    return JsonResponse(json.dumps(response_data), safe=False)


@csrf_exempt
@manage
def sertificate(request:HttpRequest, data, response_data):
    if response_data["student"]["certificate_id"]:
        file_location = f'media/sertificate/{response_data["student"]["certificate_id"]}.pdf'
        response_data["file_path"] = file_location

    else:
        response_data["file_path"] = None

    return JsonResponse(json.dumps(response_data), safe=False)
