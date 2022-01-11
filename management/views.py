from django.shortcuts import render
from .models import Projects, Task
from django.db.models import Sum
from .forms import TaskForm, ProjektForm

def podliczenie_czasow(suma_need, projekt_id):

    if suma_need['timeneed__sum'] != None:

        suma_done_min = Task.objects.filter(projekt_id=projekt_id).exclude(status=2).aggregate(Sum('timedone'))
        # suma_done_done = Task.objects.filter(projekt_id=projekt_id, status=2).aggregate(Sum('timedone'))

        if suma_done_min["timedone__sum"] == None:
            suma_done_min["timedone__sum"] = 0

        suma_done = round(float((suma_done_min["timedone__sum"] / 60)), 2)
        suma_czas_do_skonczenia = round((suma_need["timeneed__sum"] - suma_done_min["timedone__sum"]) / 60, 2)
        info_o_zadaniach = ""

        zadania_for_needtime = Task.objects.filter(status__lt=2, projekt_id=projekt_id)
        suma_needtime = 0
        for zadanie in zadania_for_needtime:
            if zadanie.timedone >= zadanie.timeneed:
                continue
            else:
                suma_needtime += (zadanie.timeneed - zadanie.timedone)

        suma_czas_do_skonczenia = round((suma_needtime / 60),2)
    else:
        suma_czas_do_skonczenia = 0
        suma_done = 0
        info_o_zadaniach = "DODAJ ZADANIE"

    return suma_done, suma_czas_do_skonczenia, info_o_zadaniach
def check_waga(projekt_id, weight, level):

    if weight == ['Minor']:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2, weight=0)
        waga = "Minor"
    elif weight == ['Major']:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2, weight=1)
        waga = "Major"
    elif weight == ['Critical']:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2, weight=2)
        waga = "Critical"
    elif weight == ['Minor', 'Major']:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2, weight__lt=2)
        waga = "Minor, Major"
    elif weight == ['Minor', 'Critical']:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2)
        zadania = zadania.exclude(weight=1)
        waga = "Minor, Critical"
    elif weight == ['Major', 'Critical']:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2, weight__gt=0)
        waga = "Major, Critical"

    else:
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2)
        waga = "Wszystkie"

    if level == ['Easy']:
        zadania = zadania.filter(level=0)
        poziom = "Easy"
    elif level == ['Medium']:
        zadania = zadania.filter(level=1)
        poziom = "Medium"
    elif level == ['Hard']:
        zadania = zadania.filter(level=2)
        poziom = "Hard"
    elif level == ['Easy', 'Medium']:
        zadania = zadania.filter(level__lt=2)
        poziom = "Easy, Medium"
    elif level == ['Easy', 'Hard']:
        zadania = zadania.exclude(level=1)
        poziom = "Easy, Hard"
    elif level == ['Medium', 'Hard']:
        zadania = zadania.filter(level__gt=0)
        poziom = "Medium, Hard"

    else:
        poziom = "Wszystkie"

    return zadania, waga, poziom
def start(request):

    projects = Projects.objects.all()

    return render(request, "main_management.html", {"projects": projects})
def zadania(request, projekt_id: int):

    poziom = "Wszystkie"
    waga = "Wszystkie"
    projekt = Projects.objects.filter(id=projekt_id)
    name_of_projekt = projekt[0].project

    zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2)
    lista = [zadania, waga, poziom]
    # ----------------- filtrów zadania względem wagi ----------------
    # weight_list = ['minor', 'major', 'critical']
    if request.method == 'POST':
        weight = request.POST.getlist('weight')
        level = request.POST.getlist('level')
        lista = (check_waga(projekt_id, weight, level))

    suma_need = zadania.aggregate(Sum('timeneed'))
    czasy = podliczenie_czasow(suma_need, projekt_id)

    contex = {"zadania": lista[0], "nr_projektu": projekt_id, "side": "show",
              "time_need": czasy[1], "time_done": czasy[0], "is_task": czasy[2],
              "nazwa_projektu": name_of_projekt, "waga": lista[1], "poziom": lista[2]}

    return render(request, "zadania.html", contex)

def add_task(request, projekt_id:int):


    form = TaskForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.projekt_id = projekt_id
        obj.save()
        poziom = "Wszystkie"
        waga = "Wszystkie"
        projekt = Projects.objects.filter(id=projekt_id)
        name_of_projekt = projekt[0].project
        zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2)
        suma_need = zadania.aggregate(Sum('timeneed'))
        czasy = podliczenie_czasow(suma_need, projekt_id)

        contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "show",
                  "time_need": czasy[1], "time_done": czasy[0], "is_task": czasy[2],
                  "nazwa_projektu": name_of_projekt, "waga": "wszystkie", "poziom": "wszystkie"}
        return render(request, "zadania.html", contex)

    return render(request, 'add_task.html', {'form': form,
                                                  'numer_projektu':  projekt_id,
                                                  'side': 'add'})
def check_task(request, zadanie_id: int, nr_projektu: int):

    task = Task.objects.get(id=zadanie_id)

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.projekt_id = nr_projektu
        obj.timedone = obj.timedone + obj.timeusing
        obj.timeusing = 0
        obj.save()

        poziom = "Wszystkie"
        waga = "Wszystkie"
        projekt = Projects.objects.filter(id=nr_projektu)
        name_of_projekt = projekt[0].project

        zadania = Task.objects.all().filter(projekt=nr_projektu, status__lt=2)
        lista = [zadania, waga, poziom]
        suma_need = zadania.aggregate(Sum('timeneed'))
        czasy = podliczenie_czasow(suma_need,nr_projektu)

        contex = {"zadania": lista[0], "nr_projektu": nr_projektu, "side": "show",
                  "time_need": czasy[1], "time_done": czasy[0], "is_task": czasy[2],
                  "nazwa_projektu": name_of_projekt, "waga": lista[1], "poziom": lista[2]}

        return render(request, "zadania.html", contex)

    return render(request, 'add_task.html', {'form': form, 'numer_projektu':  nr_projektu})
def add_projekt(request):

    form = ProjektForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        projects = Projects.objects.all()
        return render(request, "main_management.html", {'projects': projects})
    return render(request, 'add_projekt.html', {'form': form})
def done_task(request, projekt_id: int):

    zadania = Task.objects.all().filter(projekt=projekt_id, status=2)

    suma_need_done = Task.objects.filter(projekt_id=projekt_id, status=2).aggregate(Sum('timeneed'))
    if suma_need_done['timeneed__sum'] != None:

        suma_timeneed_done = round(suma_need_done["timeneed__sum"] / 60, 2)
        suma_done_done = Task.objects.filter(projekt_id=projekt_id, status=2).aggregate(Sum('timedone'))
        suma_done_done = round(suma_done_done["timedone__sum"] / 60, 2)
    else:
        suma_timeneed_done = 0
        suma_done_done = 0

    projekt = Projects.objects.filter(id=projekt_id)
    name_of_projekt = projekt[0].project
    poziom = "Wszystkie"
    waga = "Wszystkie"
    # contex = {"zadania": lista[0], "nr_projektu": projekt_id, "side": "show",
    #           "time_need": czasy[1], "time_done": czasy[0], "is_task": czasy[2],
    #           "nazwa_projektu": name_of_projekt, "waga": lista[1], "poziom": lista[2]}


    contex = {"waga": waga, "poziom": poziom,"zadania": zadania, "nr_projektu": projekt_id, "side": "done", "nazwa_projektu": name_of_projekt, "suma_timeneed_done": suma_timeneed_done,
              "suma_done_done": suma_done_done}

    return render(request, "zadania.html", contex)
def delete_task(request, projekt_id: int):

    zadania = Task.objects.all().filter(projekt=projekt_id)
    contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "delete"}

    return render(request, "zadania.html", contex)
def remove_task(request, zadanie_id: int, nr_projektu:int):

    projects = Projects.objects.all()


    zadania = Task.objects.all().filter(projekt=nr_projektu, status__lt=2)
    projekt = Projects.objects.filter(id=nr_projektu)
    name_of_projekt = projekt[0].project
    suma_need = Task.objects.filter(projekt_id=nr_projektu).exclude(status=2).aggregate(Sum('timeneed'))

    if suma_need['timeneed__sum'] != None:

        suma_done_min = Task.objects.filter(projekt_id=nr_projektu).exclude(status=2).aggregate(Sum('timedone'))
        suma_done_done = Task.objects.filter(projekt_id=nr_projektu, status=2).aggregate(Sum('timedone'))

        if suma_done_done["timedone__sum"] == None:
            suma_done_done["timedone__sum"] = 0

        suma_done = round(float((suma_done_min["timedone__sum"]/60)) + float((suma_done_done["timedone__sum"] / 60)), 2)
        suma_czas_do_skonczenia = round((suma_need["timeneed__sum"] - suma_done_min["timedone__sum"])/60, 2)
        info_o_zadaniach = ""
    else:
        suma_czas_do_skonczenia = 0
        suma_done = 0
        info_o_zadaniach = "DODAJ ZADANIE"


    task_to_delete = Task.objects.filter(id=zadanie_id)
    task_to_delete.delete()

    contex = {"zadania": zadania, "nr_projektu": nr_projektu, "side": "show",
              "nazwa_projektu": name_of_projekt,
              "time_need": suma_czas_do_skonczenia, "time_done": suma_done, "is_task": info_o_zadaniach}



    return render(request, "zadania.html", contex)






