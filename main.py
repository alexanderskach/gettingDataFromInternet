
import json
import requests
from pprint import pprint
import vk_api

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.
# github username
username = "alexanderskach"

url_repos = f"https://api.github.com/users/{username}/repos"
repos_usr_data = requests.get(url_repos).json()

git_repo = open('repo.json', 'w+')

for repo in repos_usr_data:
    pprint(repo['html_url'])

git_repo.write(json.dumps(repos_usr_data))

git_repo.close()



#  Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте
# (https://vk.com/dev/first_guide). Сделайте запрос, чтобы получить список
# всех сообществ на которые вы подписаны.


vk_session = vk_api.VkApi('+792696-----', '$$$$')
vk_session.auth()

vk = vk_session.get_api()

out_str = ''
grp = open('group.txt', 'w')

grps = vk.groups.get(user_id=vk_session.auth())['items']
for group in grps:
    print(group)
    # out_str.join(vk.groups.getById(group_id=group))
    out_str = str(vk.groups.getById(group_id=group))
    grp.write(out_str)

grp.close()




# friends = vk.friends.get(user_id=vk_session.auth())['items']
# for friend in friends:
#     print(friend)
#     print(vk.users.get(user_id=friend))
