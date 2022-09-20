# https://www.youtube.com/watch?v=7LU1npoPmcg&ab_channel=VeryAcademy
import asyncio
import time

from sklearn.datasets import fetch_california_housing

# await func() - просто ждёт , когда эта функиця закончится и вернёт результат. Это как синхронная функция

async def fetch_data():
    print('fetch start')
    await asyncio.sleep(4)
    return {'data':100}

async def countdown():
    print('countdown start')
    for i in reversed(range(10)):
        print(i)
        await asyncio.sleep(2)

async def main():
    
    fetch = asyncio.create_task(fetch_data())
    count = asyncio.create_task(countdown())

    fetch_data_resp = await fetch
    print(fetch_data_resp)
    await count

# asyncio.run(main())    




# async def get_pokemon(session, url):
#     async with session.get(url) as res:
#         pokemon = await res.json()
#         return pokemon['name']
# async def search(request):

#     start_time = time.time()
#     pokemon_data = []
#     actions = []

#     async with aiohttp.ClientSession() as session:
#         for num in range(1,101):
#             url = f'https://pokeapi.co/api/v2/pokemon/{num}/'
#             # https://ru.stackoverflow.com/questions/902586/asyncio-%D0%9E%D1%82%D0%BB%D0%B8%D1%87%D0%B8%D0%B5-tasks-%D0%BE%D1%82-future
#             actions.append(asyncio.ensure_future(get_pokemon(session, url)))
            
#         pokemon_res = await asyncio.gather(*actions)
#         for data in pokemon_res:
#             pokemon_data.append(data)

#     count = len(pokemon_data)
#     total_time = time.time() - start_time
#     return render(request, 'scrap/search.html', {'data':pokemon_data, 'count':count, 'time': total_time})

#     # async with aiohttp.ClientSession() as session:
#     #     async with session.get() as res: # https://catfact.ninja/fact
#     #         data = await res.json()
#     #         print(data)
#     # return render(request, 'scrap/search.html', {'data':data})



