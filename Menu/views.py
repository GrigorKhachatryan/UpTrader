from django.shortcuts import render
from .models import Menu
from django.db.models import Q

def menu(request):
    # ResultList - вложенные списки формата [title,parent,level]
    ResultList = []
    # Изменение значение default на OR для БД
    Q.default = Q.OR

    # Получаем исходную URL
    url = request.path[1:].split('/')
    # Q() для получения корневых пунктов меню
    ObjectsFilterParams = [Q(parent__iexact='null')]
    # Добавление в ObjectsFilterParams всех parent = url
    for parents in url:
        ObjectsFilterParams.append(Q(parent__iexact=parents))
    # Запрос к БД с использованием Q()
    for p in Menu.objects.filter(*ObjectsFilterParams):
        ResultList.append([p.title, p.parent, p.level])
    # Преобразование ResultList в список объектов формата [{title:'title, children:[{},{}]}]
    ResultJSON = RenderJSON(ResultList)

    return render(request, 'index.html',{'obj': ResultJSON})

# Рекурсивная функция для создания вложенных объектов
def creatdict(i, ResultJSON,PointList):
    for j in PointList:
        if j[1] == i[0]:
            ResultJSON['children'].append({"title": j[0], 'children': []})
            creatdict(j, ResultJSON['children'][0],PointList)

# Функция для создания списка объектов
def RenderJSON(PointList):
    # Создания списка с корневыми пунктами меню
    RootPointList = [i for i in PointList if i[2] == 0]
    # Удаление корневых пунктов из списка пунктов
    PointList = [x for x in PointList if x not in RootPointList]
    # Создание списка объектов
    ResultJSON = [{}] * len(RootPointList)
    # Заполнение списка объектов
    index = 0
    for i in RootPointList:
        ResultJSON[index] = {"title": i[0], 'children': []}
        creatdict(i, ResultJSON[0],PointList)
        index += 1
    return ResultJSON

