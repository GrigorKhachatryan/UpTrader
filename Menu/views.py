from django.shortcuts import render
from .models import Menu
from django.db.models import Q
import json

def menu(request):
    ResultObject = []
    # Изменение значение default на OR для БД
    Q.default = Q.OR

    # Получаем исходную URL
    url = request.path[1:].split('/')

    ObjectsFilterParams = [Q(parent__iexact='null')]

    for parents in url:
        ObjectsFilterParams.append(Q(parent__iexact=parents))

    for p in Menu.objects.filter(*ObjectsFilterParams):
        ResultObject.append([p.title, p.parent, p.depth])


    my_list = ResultObject
    null_list = []

    for i in my_list:
        if i[2] == 0:
            null_list.append(i)
    my_list = [x for x in my_list if x not in null_list]
    data = [{}] * len(null_list)

    def creatdict(i, data):
        for j in my_list:
            if j[1] == i[0]:
                data['children'].append({"title": j[0], 'children': []})

                creatdict(j, data['children'][0])

    index = 0
    for i in null_list:
        data[index] = {"title": i[0], 'children': []}
        creatdict(i, data[0])
        index += 1
    print(data)
    return render(request, 'index.html',{'obj': data})

# Create your views here.
