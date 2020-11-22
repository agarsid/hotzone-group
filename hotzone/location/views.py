from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .models import *
import requests
import json
    

def begin(request):
    return render(request, 'application/begin.html')

def log(request):
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return begin(request)

def authenticate_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return render(request, "login/landingpage.html")
        else:
            return render(request, "login/login.html", {"isError": True})
    except:
        return render(request, 'login/login.html')

def add(request):
    try:
        if(request.user.is_authenticated):
            ret_data = []


            cases = Case.objects.all()
            CASES=[]
            for case in cases:
                temp = {}
                temp['case'] = case.case_num
                temp['virus'] = case.infection.virus
                print(temp)
                CASES.append(temp)

            return render(request, 'application/add.html', {'cases': CASES})
        else:
            return render(request, 'login/login.html')
            
    except:
        return render(request, 'login/login.html')

def get_locs(request):
    name = request.GET.get('loc')
    results = Locations.objects.filter(place_name__icontains = name)
    res = []
    for result in results:
        temp = {'nameEN': result.place_name, 'addressEN': result.address, 'x': result.x_coord, 'y': result.y_coord}
        res.append(temp)
    return JsonResponse(res, safe=False)

def getall_case(request):

    # try:
        if(request.user.is_authenticated):

            ret_data = []

            cases = Case.objects.all()

            for case in cases:

                visited_list = case.visited.all()
                locations = []

                for each_loc in visited_list:

                    each_locs_info = Visit_Info.objects.filter(case_visit=case.pk, location_visit = each_loc.pk)
                    print('sid',each_locs_info[0])

                    for each_loc_info in each_locs_info:
                        loc = {
                            'place_name': each_loc.place_name,
                            'address': each_loc.address,
                            'x_coord': each_loc.x_coord,
                            'y_coord': each_loc.y_coord,
                            'date_from': str(each_loc_info.date_from),
                            'date_to': str(each_loc_info.date_to),
                            'category': each_loc_info.category,
                        }
                        if loc not in locations:
                            locations.append(loc)

                print("locations for",case)
                print(locations)
                    
                tmp_case_obj = {
                    'case_num': case.case_num,
                    'confirm_date': str(case.confirm_date),
                    'case_class': case.case_class,
                    'name': case.patient.name,
                    'birth_date': str(case.patient.birth_date),
                    'virus': case.infection.virus,
                    'locations': locations,
                }
                ret_data.append(tmp_case_obj)
        
            return render(request, 'application/viewdata.html', {'cases': ret_data})
        else:
            return render(request, 'login/login.html')
            
    # except:
    #     return render(request, 'login/login.html')

def addToDb(request):
    try:
        if(request.user.is_authenticated):
            if 'csrfmiddlewaretoken' in request.POST:

                form = request.POST

                data= json.loads(form['formDat'])
                case_info = data['case'].replace("'",'"')
                
                case_info = json.loads(case_info)
                
            
                if (not Virus.objects.filter(virus=case_info['virus']).exists()):
                    return JsonResponse({"msg":"error"})
                else:
                    infection = Virus.objects.get(virus=case_info['virus'])
                
                if (not Case.objects.filter(infection_id=infection.pk, case_num=case_info['case']).exists()):
                    return JsonResponse({"msg":"error"})
                else:
                    case = Case.objects.get(infection_id=infection.pk, case_num=case_info['case'])

                place_name = data['name']
                address = data['address']
                x_coord = data['x']
                y_coord = data['y']
                date_from = data['visited_from']
                date_to = data['visited_to']
                category = data['case_class']
                

                if (not Locations.objects.filter(place_name=place_name).exists()):
                    location = Locations.objects.create(place_name=place_name, address=address, x_coord=x_coord, y_coord=y_coord)
                else:
                    location = Locations.objects.get(place_name=place_name)

                Visit_Info.objects.create(case_visit_id=case.pk, location_visit_id=location.pk, date_from=date_from, date_to=date_to, category=category)            
                return HttpResponse(200)
        else:
            return render(request, 'login/login.html')
            
    except:
        return render(request, 'login/login.html')
                