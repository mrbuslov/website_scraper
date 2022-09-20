present_dict = {
    "names": [
        "Дніпро,Дніпропетровська область Остафія Дашковича вулиця,Черкаси,Черкаська область",
        "Відродження вулиця,Овруцький район,Житомирська область Торгова площа,Білоцерківський район,Київська область",
        "Відродження вулиця,Овруцький район,Житомирська область Хрещатик вулиця,Київ,Київ",
    ],
    "addrs": [
        "Рената Кондратенкова Заявник",
        "Ірина Заявник",
        "Ірина Заявник",
    ],
    'text':'text',
}
new_dict = {
    "names": [
        "Дніпро,Дніпропетровська область Остафія Дашковича вулиця,Черкаси,Черкаська область",
        "Відродження вулиця,Овруцький район,Житомирська область Торгова площа,Білоцерківський район,Київська область",
        "Відродження вулиця,Овруцький район,Житомирська область Хрещатик вулиця,Київ,Київ",
    ],
    "addrs2": [
        "Рената Кондратенкова Заявник",
        "Ірина Заявник",
        "Ірина Заявник",
    ],
    'text1':'text',
    'text':'text',
}


for key in new_dict:
    if key in present_dict:
        if isinstance(present_dict[key], list): # если в этом словаре значение - СПИСОК
            if isinstance(new_dict[key], list): # то мы добавим к нему список
                present_dict[key] = present_dict[key] + new_dict[key]
            elif isinstance(new_dict[key], str): # или добавим строку
                present_dict[key].append(new_dict[key])
        elif  isinstance(present_dict[key], str): # если в этом словаре значение - СТРОКА
            if isinstance(new_dict[key], str): # то мы добавим к ней строку, образуя список
                present_dict[key] = [present_dict[key], new_dict[key]]
            elif isinstance(new_dict[key], list): # или добавим список
                present_dict[key] = new_dict[key].insert(0, present_dict[key]) # на первую позицию

    else:
        present_dict[key] = new_dict[key]


data = [
    [1,2,3],
    [2,3,4],
    [5,6,7],
]


list_one = ('Joe', 'Mark', 'Jane')
list_two = ( 100, 34, 87, 23, 65 )

arr = [list_one, list_two]

import itertools

res = list(itertools.zip_longest(*arr, fillvalue=''))





d = [
    {
        "йцу": [
            "/html/body/div[3]/div/div/div/p",
            "/html/body/div[3]/div/div/div/p[2]"
        ]
    },
    {
        "фыв": "/html/body/div[3]/div/div[2]/div/p/span"
    }
]


