from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from nhp_app.models import *
# from ..models.master_models import designation_Master

USER_LOGIN_MAP = {
    'delhi' : 'nhp-delhi',
    'shimla' : 'nhp-shimla',
    'super_admin' : 'admin',
}

def user_login(request):
    if request.method == 'GET':
        print('>>>>>>>>>>> ',request.user)
        if request.user:
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            else:
                states = state_master.objects.all()
                return render(request,'authentication/login.html', {'states':states})
        states = state_master.objects.all()
        return render(request,'authentication/login.html', {'states':states})

    # if request.method == 'POST':
    #     username = request.POST['emailaddress']
    #     password = request.POST['password']
    #     state = request.POST['nhp-state']

    #     userFK = authenticate(username=username, password=password)
    #     if userFK is not None:
    #         if(userFK.is_superuser):
    #             if(state == 'admin'):
    #                 login(request, userFK)
    #                 return redirect('admin_dashboard')
    #             else:
    #                 messages.success(request,'Invalid credentials')
    #                 return redirect('user_login')
    #         else:
    #             user_prof = user_profile.objects.get(user=userFK)
    #             if user_prof.state.name == state:
    #                 login(request, userFK)
    #                 return redirect('admin_dashboard')
    #             else:
    #                 messages.success(request,'Invalid credentials')
    #                 return redirect('user_login')
    #     else:
    #         messages.success(request,'Invalid credentials')
    #         return redirect('user_login')
    if request.method == 'POST':
        username = request.POST['emailaddress']
        password = request.POST['password']

        userFK = authenticate(username=username, password=password)
        if userFK is not None:
            if(userFK.is_superuser):
                login(request, userFK)
                return redirect('admin_dashboard')
            else:
                messages.success(request,'Invalid credentials')
                return redirect('user_login')
        else:
            messages.success(request,'Invalid credentials')
            return redirect('user_login')



@login_required(login_url='/')
def update_site_detail(request, uuid):
    if request.method == 'GET':
        siteObj = site.objects.get(uuid=uuid)
        projects = project_master.objects.all()
        return render(request,'admin/bin_serv/edit_detail.html', {'siteObj':siteObj,'projects':projects})
    if request.method == 'POST':
        dev_name = request.POST.get('dev_name',' ')
        dev_loc = request.POST.get('dev_loc',' ')
        dev_lat = request.POST.get('dev_lat',' ')
        dev_lon = request.POST.get('dev_lon',' ')
        tpro_prfx = request.POST.get('tpro_prfx',' ')
        tpro_file = request.POST.get('tpro_file',' ')
        dev_proj = request.POST.get('dev_proj',' ')
        pos1 = request.POST.get('pos1',' ')
        pos2 = request.POST.get('pos2',' ')
        pos3 = request.POST.get('pos3',' ')
        pos4 = request.POST.get('pos4',' ')
        pos5 = request.POST.get('pos5',' ')
        pos6 = request.POST.get('pos6',' ')
        pos7 = request.POST.get('pos7',' ')
        pos8 = request.POST.get('pos8',' ')
        pos9 = request.POST.get('pos9',' ')
        pos10 = request.POST.get('pos10',' ')

        try:
            siteObj = site.objects.get(uuid=uuid)
            deviceCong = {
                            "device" : siteObj.prefix.lower(),
                            "location" : dev_loc,
                            "sensor_position" : {
                                "0" : "timestamp",
                                "1" : "count",
                                "2" : pos1,
                                "3" : pos2,
                                "4" : pos3,
                                "5" : pos4,
                                "6" : pos5,
                                "7" : pos6,
                                "8" : pos7,
                                "9" : pos8,
                                "10" : pos9,
                                "11" : pos10,
                            }
                        }
            paramList = []
            if pos1:
                paramList.append(pos1)
            if pos2:
                paramList.append(pos2)
            if pos3:
                paramList.append(pos3)
            if pos4:
                paramList.append(pos4)
            if pos5:
                paramList.append(pos5)
            if pos6:
                paramList.append(pos6)
            if pos7:
                paramList.append(pos7)
            if pos8:
                paramList.append(pos8)
            if pos9:
                paramList.append(pos9)
            if pos10:
                paramList.append(pos10)

            siteList = siteObj.total_params
            for i in paramList:
                siteList.append(i)
            siteList = list(set(siteList))
            siteObj.name = dev_name
            siteObj.tpro_file_name = tpro_file
            if dev_proj:
                projectObj = project_master.objects.get(uuid=dev_proj)
                siteObj.project = projectObj

            siteObj.total_params = siteList
            siteObj.device_location = dev_loc
            siteObj.tpro_prefix = tpro_prfx
            siteObj.site_lattitude = dev_lat
            siteObj.sit_longitude = dev_lon
            siteObj.device_config = deviceCong
            siteObj.save()
            return JsonResponse({'response':'Site updated successfully.'})

        except Exception as err:
            print(f'Error occured due to : {err}')
            return JsonResponse({'response':str(err)})


@login_required(login_url='/')
def site_data(request, uuid):
    if request.method == 'GET':
        siteObj = site.objects.get(uuid=uuid)
        return render(request,'admin/bin_serv/site_data.html', {'siteObj':siteObj})


@login_required(login_url='/')
def user_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('user_login')




@login_required(login_url='/')
def admin_dashboard(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            sites = site.objects.all()
            return render(request,'admin/dashboard.html', {'sites':sites})
        else:
            # return redirect('admin_dashboard')
            return render(request,'authentication/login.html')