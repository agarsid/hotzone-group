from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .models import *
import requests, json, math
from datetime import date
import numpy as np
from sklearn.cluster import DBSCAN

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
            #return render(request, 'application/add.html', {'cases': CASES})
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

def get_virus(request):

    #try:
    if(request.user.is_authenticated):

        virus_list = []

        all_virus = Virus.objects.all()

        for each_virus in all_virus:

            virus_list.append(each_virus.virus)
    
        return render(request, 'application/viewdata_prelim.html', {'virus_list': virus_list})
    else:
        return render(request, 'login/login.html')
        
    # except:
    # return render(request, 'login/login.html')

def getall_case(request,virus):

    try:
        if(request.user.is_authenticated):
            print(virus)
            infection = Virus.objects.get(virus=virus)
            ret_data = []

            cases = Case.objects.filter(infection_id=infection.pk)

            for case in cases:

                visited_list = case.visited.all()
                locations = []

                for each_loc in visited_list:

                    each_locs_info = Visit_Info.objects.filter(case_visit=case.pk, location_visit = each_loc.pk)
                    #print('sid',each_locs_info[0])

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
                #print(locations)
                    
                tmp_case_obj = {
                    'case_num': case.case_num,
                    'confirm_date': str(case.confirm_date),
                    'case_class': case.case_class,
                    'name': case.patient.name,
                    'id_num': case.patient.id_num,
                    'birth_date': str(case.patient.birth_date),
                    'virus': case.infection.virus,
                    'locations': locations,
                }
                ret_data.append(tmp_case_obj)
        
            return render(request, 'application/viewdata.html', {'cases': ret_data, 'virus':infection})
        else:
            return render(request, 'login/login.html')
            
    except:
        return render(request, 'login/login.html')

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

def cluster_prelim(request):
    # try:
    #     if(request.user.is_authenticated):

    #         virus = Virus.objects.all()
    #         virus_list = []
    
    #         for each_virus in virus:
    #             virus_list.append(each_virus.virus)

    #         return render(request, 'application/cluster_prelim.html', {'virus': virus_list})
    #     else:
    #         return render(request, 'login/login.html')
            
    # except:
    #     pass
        # return render(request, 'login/login.html')

    try:
        if(request.user.is_authenticated):

            virus_list = []

            all_virus = Virus.objects.all()

            for each_virus in all_virus:

                virus_list.append(each_virus.virus)
        
            return render(request, 'application/cluster_prelim.html', {'virus_list': virus_list})
        else:
            return render(request, 'login/login.html')
    except:
        return render(request, 'login/login.html')

def custom_metric(q, p, space_eps, time_eps):
    dist = 0
    for i in range(2):
        dist += (q[i] - p[i])**2
    spatial_dist = math.sqrt(dist)

    time_dist = math.sqrt((q[2]-p[2])**2)

    if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and p[3] != q[3]:
        return 1
    else:
        return 2

def cluster(vector_4d, distance, time, minimum_cluster, misc_data):

    params = {"space_eps": distance, "time_eps": time}
    db = DBSCAN(eps=1, min_samples=minimum_cluster-1, metric=custom_metric, metric_params=params).fit_predict(vector_4d)

    unique_labels = set(db)
    total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1

    #print("Total clusters:", total_clusters)

    #total_noise = list(db).count(-1)

    #print("Total un-clustered:", total_noise)

    cluster_data = []

    for k in unique_labels:
        if k != -1:

            labels_k = db == k
            cluster_k = vector_4d[labels_k]
            misc = misc_data[labels_k]

            #print("Cluster", k, " size:", len(cluster_k))
            visit_list = []

            for idx, pt in enumerate(cluster_k):
                visit = {
                    'place_name': misc[idx][0],
                    'x_coord': pt[0],
                    'y_coord': pt[1],
                    'visit_date': misc[idx][1],
                    'case_num': int(pt[3])
                }
                visit_list.append(visit)
            
                #print("(x:{}, y:{}, day:{}, caseNo:{}, name:{}, date:{})".format(pt[0], pt[1], pt[2], pt[3], misc[idx][0], misc[idx][1]))

            cluster_data.append(visit_list)

    return cluster_data

def clustering(request):
    try:
        if(request.user.is_authenticated):
            cluster_param = request.GET
    
            virus = cluster_param.get('virus')
            D = int(cluster_param.get('D'))
            T = int(cluster_param.get('T'))
            C = int(cluster_param.get('C'))

            if (not Virus.objects.filter(virus=virus).exists()):
                return JsonResponse({"msg":"error"})
            else:
                infection = Virus.objects.get(virus=virus)
                
            record_list=[]
            misc_list=[]
            cases = Case.objects.filter(infection=infection.pk)
            
            if(len(cases)<1):
                return render(request, 'application/cluster.html', {'clusters': []})

            for each_case in cases:
                visited_list = each_case.visited.all()

                for each_loc in visited_list:
                    each_locs_info = Visit_Info.objects.filter(case_visit=each_case.pk, location_visit = each_loc.pk)

                    for each_loc_info in each_locs_info:

                        if (each_loc_info.date_from == each_loc_info.date_to):
                            origin = date(2020, 1, 1)

                            record = [each_loc.x_coord, each_loc.y_coord, (each_loc_info.date_from - origin).days, each_case.case_num]
                            misc = [each_loc.place_name, str(each_loc_info.date_from)]

                            if record not in record_list:
                                record_list.append(record)
                                misc_list.append(misc)
            print('np', np.array(record_list))
            data = cluster(np.array(record_list), D, T, C, np.array(misc_list))

            # print("Total clusters:", len(data))
            # for idx,obj in enumerate(data):
            #     print("Cluster", idx, " size:", len(obj))
            #     for visit in obj:
            #         print("(x:{}, y:{}, caseNo:{}, name:{}, date:{})".format(visit['x_coord'], visit['y_coord'], visit['case_num'], visit['place_name'], visit['visit_date']))
            #     print()
            # print(data)

            return render(request, 'application/cluster.html', {'clusters': data})
        else:
            return render(request, 'login/login.html')
    except:
        return render(request, 'login/login.html')