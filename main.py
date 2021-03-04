import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import random

# bot token
TOKEN = "641260a0ec621dfff90ba8322fd778dbf2f3594d2ebe75037675d5e21272290f76086b6c6c8f4aa8a7d97"

# connection to VK
vk = vk_api.VkApi(token=TOKEN)
vk_session = vk.get_api()
longpoll = VkLongPoll(vk)


# get name meaning
def req(name):
    # format name
    name.lower()

    # request to website
    request = f"https://kakzovut.ru/names/{name}.html"

    # get request
    response = requests.get(request)

    # check response status
    if response.status_code // 100 != 2:
        return False

    # decoding result of query(html)
    html = response.content.decode('utf-8')

    # start parsing
    result = ''

    # max pages count
    count = 5

    # iteration in html
    for line in html.split('\n'):

        # check only <p> tags
        if line[:3] == "<p>" and count:
            count -= 1
            write = True

            # iteration in <p> tag
            for i in line[3:-3]:
                # write only content(not '<tag>')
                if i == '<':
                    write = False
                elif i == '>':
                    write = True
                elif write:
                    result += i

    return result


# get user name ( not used)
def get_user_name(user_id):
    user_get = vk_session.users.get(user_ids=(user_id))
    user_get = user_get[0]
    first_name = user_get['first_name']
    last_name = user_get['last_name']

    return first_name, last_name


# send to chat
def send_message(chat_id, text):
    # generate random id
    random_id = random.randint(0, 1000000)

    # send message
    vk.method('messages.send', {'chat_id': chat_id, 'message': text, 'random_id': random_id})


# event loop
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:
                # message from user
                msg = event.text

                # chat id
                chat_id = event.chat_id
                user_id = event.user_id
                user_name = get_user_name(user_id)

                # bot response
                if req(msg):
                    send_message(chat_id, req(msg))

if __name__ == '__main__':
    main()
