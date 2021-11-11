from django.contrib.auth import forms
import datetime
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm  
from .forms import CustomUserform
from .forms import patientform, appointmentform,appointmentforms
from .models import Appointment, Doctor, Patient
import pandas as pd 
import os
import csv
from hospital_management_system.settings import BASE_DIR
# Create your views here.

def home(request):
    return render(request,'index.html')


def signupuser(request):
    if request.method == 'POST':
        form=CustomUserform(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse("Register user successfull")
    form=CustomUserform  
    return render(request,'register.html',{'form':form})



def loginuser(request):
    if request.method=="POST":
        name=request.POST['name']
        pd=request.POST['password']
        user=authenticate(username=name,password=pd)
        if user:
            login(request,user)
            print("user login =====", user.usertype, type(user.usertype))
            if user.usertype==1:
                return redirect('doctorprofile')
            elif user.usertype==2:
                return redirect('patientprofile')

            else:
                
                return HttpResponse("admin profile")  
            
        else:
            return HttpResponse("invalid password or username")    
    return render(request,'login.html')





def logoutuser(request):
    logout(request)
    return redirect("home")



def patientprofile(request):
    obj=Patient.objects.filter(user=request.user)
    if obj:
        return redirect('appoitnment')  
    if request.method=="POST":      
        gd=request.POST['gender']
        mb=request.POST['mobile']
        age=request.POST['age']
        ad=request.POST['address'] 
       
        obj=Patient.objects.create(
            user=request.user,
            name=request.user,
            gender=gd,
            mobile=mb,
            age=age,
            address=ad
            )
        # obj.save()
        return redirect('appoitnment')
            
        # return HttpResponse("form not valid")

    return render(request,'pst.html')





def appointment(request):
    if request.method=='POST':
        dep=request.POST['dep']
        dat=request.POST['date']
        time=request.POST['time'] 
        
        
        if time<"10:00" or time>"21:00":
            return HttpResponse("<h1> this is not a appointment time <br> appointment time 10am to 9pm only</h1>") 
        #print("====time===",time)
        data=Appointment.objects.filter(dep=dep, date=dat,time=time).first()
        if data:
            return HttpResponse("this slot time allready book <br>please change the time")
            # check appointment full or not
        #data=Appointment.objects.filter(dep=dep, date=datetime.date.today())   
        data=Appointment.objects.filter(dep=dep, date=dat) 
        l=[] 
        for i in data:
            l.append(i.patientname)
        if len(l)>=10:
            return HttpResponse("this date slot allready Book please change date")


        Appointment.objects.create(patientname=request.user,
        dep=dep,
        date=dat,
        time=time)
        #### show doctor
        doct=Doctor.objects.filter(specielist=dep).first()
        data={
            "deparment":dep,
            "date":dat,
            "time":time,
            "doctor":doct.name,
            "name":request.user,
        }

        #print("=========",data)
        
        return render(request, 'appointment_detail.html',data) 
    user=request.user
    data=Appointment.objects.filter(patientname=user)
    return render(request,'apt.html',{'data':data})




def download(request,id):
    data=Appointment.objects.get(id=id)
    
   # print("datasupport",data.__dict__)
    dict_data={
        'id':[data.id],
        'name':[data.patientname],
        'dep':[data.dep],
        'prescription':[data.prescription],
        'date':[data.date],
        'time':[data.time],
    }
    #print("data",dict_data)
       
    dataframe=pd.DataFrame(dict_data)
    # print(dataframe)
               # save file by default
    file_name=request.user
    id=str(id)
    # dataframe.to_csv(f'{file_name}{id}.csv')
    path = str(BASE_DIR) + '/hospital/static/csv'
    print(path,'=-----------------------------------')
    dataframe.to_csv(os.path.join(path,f'{file_name}{id}.csv'))
    # dataframe.to_csv(f'/home/saddam/Desktop/hms/hospital_management_system/hospital/static/csv/{file_name}{id}.csv')
    
    # filename=str(BASE_DIR) + f'/hospital/static/csv/{file_name}{id}.csv'
    # print(filename,"==-- --==")
    # openfile=pd.read_csv(filename) 
    # #print(openfile)
    # print(openfile['id'][0],openfile['name'][0],openfile['dep'][0],openfile['date'][0])
    # return HttpResponse('data downloaded')
    
        ##download file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={file_name}{id}.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'dep', 'prescription','date','time'])
    writer.writerow([data.id,data.patientname,data.dep,data.prescription,data.date,data.time])
    return response
  




def doctorprofile(request):
    obj=Doctor.objects.filter(user=request.user)
    if obj:
        return redirect('patientappointmentdetail')   
    if request.method=='POST':
        dep=request.POST['dep']
        mob=request.POST['mobile']
            
        obj=Doctor.objects.create(
            user=request.user,
            name=request.user,
            mobile=mob,
            specielist=dep
            )
        return redirect('patientappointmentdetail')     
    return render(request,'doc.html')







def patientappointmentdetail(request):
    obj=Doctor.objects.get(user=request.user)
    dep=obj.specielist
    #print(dep,'==============d============d============')
    #print(datetime.date.today(), "date============")
    type=request.GET.get('type')
    pr=Appointment.objects.filter()
    #print(type,"=====")
    if type=='upcomming':                        #tommorrow date
        data=Appointment.objects.filter(dep=dep, date__gt=datetime.date.today())
        return render(request, 'allapt.html',{'data':data}) 
    elif type==None or type=='today':               #today date
        data=Appointment.objects.filter(dep=dep, date=datetime.date.today())
        return render(request, 'allapt.html',{'data':data}) 
    elif type=='expire':                                       #yesterday date
        data=Appointment.objects.filter(dep=dep, date__lt=datetime.date.today())
        return render(request, 'allapt.html',{'data':data}) 
    else:           #all appointment
        data=Appointment.objects.filter(dep=dep)
        return render(request, 'allapt.html',{'data':data}) 

 


def v(request,id):
    data=Appointment.objects.get(id=id)
    if data.prescription != None:
        return HttpResponse("this appointment already checked")
    if request.method=='POST':
        form=appointmentforms(request.POST,instance=data)
        form.save()
        data=Appointment.objects.get(id=id)
        return render(request,'ppd.html',{'data':data})
    
    data=appointmentforms(instance=data)
    return render(request,'v.html',{'data':data})   




def updatedata(request,id):
    data=Appointment.objects.get(id=id)
    
    if request.method=='POST':
        form=appointmentforms(request.POST,instance=data)
        form.save()
        return HttpResponse("data updated")
    
    data=appointmentforms(instance=data)
    return render(request,'v.html',{'data':data})   





def delete_appointment(request,id):
    try:
        data=Appointment.objects.get(id=id)
        data.delete()
        return HttpResponse('data deleted')
    except data.DoesNotExist:
        return HttpResponse("data DoesNotExist:")   




def checkp(request,id):
    data=Appointment.objects.get(id=id)
    return render(request,'check.html',{'data':data})


def tedb(request):
    data=Appointment.objects.all()
    d={}
    for data in data:
        dict_data={
        'id':[data.id],
        'name':[data.patientname],
        'dep':[data.dep],
        'prescription':[data.prescription],
        'date':[data.date],
        'time':[data.time],}
    return HttpResponse('data in dict')