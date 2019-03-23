from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Employee, Availability, Dayschedule
from django.template import loader
import calendar, datetime

def index(request):
    current_user=Employee.objects.get(user=request.user)
    template = loader.get_template('shiftmaestro/index.html')
    thenow = datetime.datetime.now()
    month = thenow.month
    year = thenow.year
    context = {'user': current_user, 'month': month, 'year':year}
    return HttpResponse(template.render(context, request))
    
def availability(request):
    current_user=Employee.objects.get(user=request.user)
    template = loader.get_template('shiftmaestro/availability.html')
    thenow = datetime.datetime.now()
    month = thenow.month
    year = thenow.year
    #CREATING LIST OF DAYS
    if thenow.month==12:
        nextmonth = 1
        nextmonthyear = (thenow.year)+1
    else:
        nextmonth = (thenow.month)+1
        nextmonthyear = thenow.year
    num_days = calendar.monthrange(nextmonthyear, nextmonth)[1]
    days = [datetime.date(nextmonthyear, nextmonth, day) for day in range(1, num_days+1)]
    
    context = {'user': current_user, 'days': days, 'month': month, 'year':year}
    return HttpResponse(template.render(context, request))

def availabilitysaved(request):
    template = loader.get_template('shiftmaestro/availabilitysaved.html')
    current_user=Employee.objects.get(user=request.user)

    #CREATING LIST OF DAYS
    thenow = datetime.datetime.now()
    month = thenow.month
    year = thenow.year
    if thenow.month==12:
        nextmonth = 1
        nextmonthyear = (thenow.year)+1
    else:
        nextmonth = (thenow.month)+1
        nextmonthyear = thenow.year
    num_days = calendar.monthrange(nextmonthyear, nextmonth)[1]
    days = [datetime.date(nextmonthyear, nextmonth, day) for day in range(1, num_days+1)]
    #SAVING AVAILABILITY DATA FROM FORM to DATABASE
    for q in days:
        shifts=[False, False, False]
        for i in range (3):

            if request.POST.get('formsh' + str(i+1) + str(q.day)):
                shifts[i] = True
        obj, created = Availability.objects.update_or_create(employee=current_user , day=q, defaults = {'shift1' : shifts[0], 'shift2' : shifts[1], 'shift3' : shifts[2],},)
    context = {'user':current_user, 'month': month, 'year':year}
    return HttpResponse(template.render(context, request))

def schedule(request, year, month):
    current_user=Employee.objects.get(user=request.user)

    #CREATING LIST OF DAYS
    thenow = datetime.datetime.now()
    curmonth = thenow.month
    curyear = thenow.year

    if thenow.month==12:
        nextmonth = 1
        nextmonthyear = (thenow.year)+1
    else:
        nextmonth = (thenow.month)+1
        nextmonthyear = thenow.year
    num_daysthismonth = calendar.monthrange(year, month)[1]
    daysthismonth = [datetime.date(year, month, day) for day in range(1,num_daysthismonth+1)]

    #GETTING DATA ABOUT SCHEDULE FROM DATABASE
    monthsched = {d:{1:[],2:[],3:[]} for d in daysthismonth} 
    for i in daysthismonth:
        for e in Dayschedule.objects.filter(shift=1, day = i).values_list('employee', flat=True):
            monthsched[i][1].append(Employee.objects.get(user=e))
        for e in Dayschedule.objects.filter(shift=2, day = i).values_list('employee', flat=True):
            monthsched[i][2].append(Employee.objects.get(user=e))
        for e in Dayschedule.objects.filter(shift=3, day = i).values_list('employee', flat=True):
            monthsched[i][3].append(Employee.objects.get(user=e))

    template = loader.get_template('shiftmaestro/schedule.html')
    context = {'user': current_user, 'daysthismonth': daysthismonth, 'monthsched': monthsched, 'daysthismonth':daysthismonth, 'curmonth': curmonth, 'curyear':curyear, 'month':month, 'year':year, 'nextmonth':nextmonth, 'nextmonthyear':nextmonthyear}
    return HttpResponse(template.render(context, request))


def schedulemaker(request, forday):
    current_user=Employee.objects.get(user=request.user)
    day_editing = 0
    shiftdict={1:[],2:[],3:[]}
    shifts = [1,2,3]
    thenow = datetime.datetime.now()
    month = thenow.month
    year = thenow.year
    if thenow.month==12:
        nextmonth = 1
        nextmonthyear = (thenow.year)+1
    else:
        nextmonth = (thenow.month)+1
        nextmonthyear = thenow.year
    fdoor = calendar.monthrange(nextmonthyear, nextmonth)[1] + 1 #first day out of range
    days_list = range(1,fdoor)    
    #creating list of available employees for each day and each shift
    if (forday > 0):
        day_editing = datetime.date(nextmonthyear, nextmonth, forday)
        if (Availability.objects.filter(day=day_editing.strftime('%Y-%m-%d'), shift1=True).count() > 0):
            for i in Availability.objects.filter(day=day_editing, shift1=True):
                shiftdict[1].append(i.employee.name)
        if (Availability.objects.filter(day=day_editing.strftime('%Y-%m-%d'), shift2=True).count() > 0):
            for i in Availability.objects.filter(day=day_editing, shift2=True):
                shiftdict[2].append(i.employee.name)
        if (Availability.objects.filter(day=day_editing.strftime('%Y-%m-%d'), shift3=True).count() > 0):
            for i in Availability.objects.filter(day=day_editing, shift3=True):
                shiftdict[3].append(i.employee.name)
        
    template = loader.get_template('shiftmaestro/schedulemaker.html')
    context = {'user': current_user, 'day_editing': day_editing, 'shifts': shifts, 'shiftdict': shiftdict, 'fdoor': fdoor, 'days_list': days_list, 'forday': forday, 'month': month, 'year':year}
    return render(request, 'shiftmaestro/schedulemaker.html', context)

def schedulesaved(request, forday):
    current_user = Employee.objects.get(user=request.user)
    nextday = forday+1
    employees_list = Employee.objects.all()
    thenow = datetime.datetime.now()
    month = thenow.month
    year = thenow.year
    if thenow.month==12:
        nextmonth = 1
        nextmonthyear = (thenow.year)+1
    else:
        nextmonth = (thenow.month)+1
        nextmonthyear = thenow.year
    day_saved = datetime.date(nextmonthyear, nextmonth, forday)
    fdoor = calendar.monthrange(nextmonthyear, nextmonth)[1] + 1 #first day out of range
    #saving schedule data to database
    for shift in range(1,4):
        scheduleday = []
        for emp in employees_list:
            if request.POST.get('formsh' + str(shift) + emp.name):
                Dayschedule.objects.update_or_create(day=day_saved, employee = emp.id, defaults = {'shift' : shift,}) 

    template = loader.get_template('shiftmaestro/schedulesaved.html')
    context = {'user': current_user, 'fdoor':fdoor,'forday':forday , 'nextday':nextday, 'scheduleday':scheduleday, 'month': month, 'year':year}
    return HttpResponse(template.render(context, request))
