import time
import telebot
import json
import random
from telebot import types
from telebot.types import InlineKeyboardButton
from shutil import copy
import token_

expgain = [18, 21]
chance = 75
debug = 0
cooldown = 3600
percent_debuff_per_lvl = 3
exp_buff = 6

# balanced:
# percent_debuff_per_lvl = 4
# exp_buff = 3

chat_link = 'https://t.me/+HhG9tCb5RKk2NTcy'

start_time = time.time()
bot = telebot.TeleBot(token_.token)
bot.set_my_commands([
    telebot.types.BotCommand('fuck', '(в ответ на сообщение) выебать мать'),
    telebot.types.BotCommand('lvl', 'Узнать свой уровень и экспу // (в ответ на сообщение) узнать чужой уровень и шанс успеха'),
    telebot.types.BotCommand('rating', 'Общий рейтинг всех участников'),
    telebot.types.BotCommand('cd', 'Узнать сколько тебе ещё ждать'),
])

def user_add(base, message):
    u_id = str(message.from_user.id)
    try:
        first_name = message.from_user.first_name.encode('utf-8').decode('utf-8')
    except:
        first_name = ''
    try:
        last_name = message.from_user.last_name.encode('utf-8').decode('utf-8')
    except:
        last_name = ''

    nickname = first_name + ' ' + last_name
    if len(nickname) == 1:
        nickname = 'Быдло с кривым ником'

    base[u_id] = {
        'name': nickname,
        'lvl': 1,
        'exp': 0,
        'last_take': time.time() - 86400,
        'last_get': time.time() - 86400,
        'take_count': 0,
        'get_count': 0,
        'fail_count': 0
    }

    return base

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    base = open("Files/data_file.json", encoding='utf8')
    read = json.load(base)
    base.close()
    rating = []
    for i in read:
        rating.append([read[i]['lvl'], read[i]['exp'], read[i]['take_count'], read[i]['get_count'], read[i]['name']])
    if call.data == 'lvl':
        rating_name = 'Топ 10 по уровню:\n(Цифра - уровень)'
        sort_key = 1
        filters = [1, 1, 1]
    elif call.data == 'exp':
        rating_name = 'Топ 10 по количеству опыта:\n(Цифра - кол-во опыта)'
        sort_key = 1
        filters = [0, 1, 1]
    elif call.data == 'take':
        rating_name = 'Топ 10 милфхантеров:\n(Цифра - сколько раз выебал)'
        sort_key = 2
        filters = [0, 0, 1]
    else:
        rating_name = 'Топ 10 слабых на передок мамаш:\n(Цифра - сколько раз выебали его мать)'
        sort_key = 3
        filters = [0, 0, 0]

    rating_str = rating_name + '\n\n'
    rating = sorted(rating, key=lambda sorter: sorter[sort_key])
    rating.reverse()
    count = 0
    for i in rating:
        count += 1
        if count == 11:
            break
        i.pop(filters[0])
        i.pop(filters[1])
        i.pop(filters[2])
        for o in i:
            rating[rating.index(i)][i.index(o)] = str(o)
        rating_str += str(count) + ' - ' + ' - '.join([i[1], i[0]]) + '\n'

    bot.delete_message(*bot.last_message_sent)
    bot.send_message(bot.last_message_sent[0], rating_str, disable_notification=True)

def fuck(message):
    read = json.load(open('Files/data_file.json', 'r', encoding='utf8'))
    user_id = str(message.from_user.id)
    try:
        reply_id = str(message.reply_to_message.from_user.id)
    except:
        bot.reply_to(message, 'Перешли сообщение того чью мать хочешь выебать')

        return

    if user_id == reply_id:
        bot.send_animation(message.chat.id, open('Files/realshit.gif', 'rb'), reply_to_message_id=message.id)

        return
    elif message.reply_to_message.from_user.username == 'DickDestroyerBot':
        bot.reply_to(message, 'У меня нет матери')

        return
    else:
        pass


    try:
        attack = read[user_id]
    except:
        read = user_add(read, message)
        attack = read[user_id]

    try:
        defence = read[reply_id]
    except:
        read = user_add(read, message.reply_to_message)
        defence = read[reply_id]

    if debug == 1:
        pass
    else:
        last_take = attack['last_take']
        time_diff = time.time() - last_take
        if time_diff < cooldown:
            time_diff = cooldown - time_diff
            if time_diff > 60:
                time_diff = str(int(time_diff // 60)) + ' мин.'
            else:
                time_diff = str(int(time_diff)) + ' сек.'
            bot.reply_to(message, 'Не переоценивай себя. Ещё чуть больше {}'.format(time_diff))

            return

        last_get = defence['last_get']
        time_diff = time.time() - last_get
        if time_diff < 120:
            time_diff = 120 - time_diff
            if time_diff > 60:
                time_diff = str(int(time_diff // 60)) + ' мин.'
            else:
                time_diff = str(int(time_diff)) + ' сек.'
            bot.reply_to(message, 'Дай мамаше отдохнуть. Ещё чуть больше {}'.format(time_diff))

            return

    if random.randint(1, 100) < 2:
        bot.reply_to(message, 'О нет! Его мать оказалась трапом и сама тебя выебала. Ну ничего, подлечишь очелло и снова в бой!')
        attack['last_take'] = time.time()
        copy('Files/data_file.json', 'Files/data_file_copy.json')
        json.dump(read, open('Files/data_file.json', 'w', encoding='utf8'), ensure_ascii=False)

        return

    # chance count
    lvl_dif = attack['lvl'] - defence['lvl']
    bonus_chance = lvl_dif * percent_debuff_per_lvl
    if bonus_chance > 100 - chance - 5:
        bonus_chance = 100 - chance - 5
    elif bonus_chance < 0 - (chance - 5):
        bonus_chance = 0 - (chance - 5)
    bonus_chance += attack['fail_count'] * 5

    if random.randint(1, 100) < chance + bonus_chance:
        # success
        lvl_difference = attack['lvl'] - defence['lvl']
        if lvl_difference < 0:
            exp_gain = random.randint(expgain[0], expgain[1]) + lvl_difference * -1 * exp_buff
        else:
            lvl_difference = lvl_difference * 3
            if lvl_difference > 17:
                lvl_difference = 17
            exp_gain = random.randint(expgain[0], expgain[1]) - lvl_difference

        attack['last_take'] = time.time()
        defence['last_get'] = time.time()
        attack['take_count'] += 1
        defence['get_count'] += 1
        attack['exp'] += exp_gain
        attack['fail_count'] = 0
        bot.reply_to(message, 'Ты успешно выебал мать {}\n+{} опыта\nLVL {} - {}/{} XP'.format('[' + defence['name'] + '](tg://user?id=' + reply_id + ')', exp_gain, attack['lvl'], attack['exp'], 150 * int(attack['lvl'])), parse_mode='Markdown')
        bot.send_animation(message.chat.id, open('Files/success.gif', 'rb'))
        if attack['exp'] >= 150 * int(attack['lvl']):
            attack['lvl'] = attack['exp'] // 150 + 1
            bot.reply_to(message, 'Ты достиг уровня {}! \nСледующий уровень {}/{} XP'.format(attack['lvl'], attack['exp'], 150 * int(attack['lvl'])))
    else:
        # fail
        lvl_dif = defence['lvl'] - attack['lvl']
        if lvl_dif < 0:
            exp_gain = random.randint(5, 8) + random.randint(1, 3) * lvl_dif * -1
        else:
            lvl_dif = lvl_dif * 3
            if lvl_dif > 17:
                lvl_dif = 17
            exp_gain = random.randint(expgain[0] - 5, expgain[1] - 5) - lvl_dif

        attack['last_take'] = time.time()
        attack['fail_count'] += 1
        defence['exp'] += exp_gain
        bot.reply_to(message, 'Тебе не удалось выебать мамашу {}. Теперь он получил {} опыта'.format('[' + defence['name'] + '](tg://user?id=' + reply_id + ')', exp_gain), parse_mode='Markdown')
        bot.send_animation(message.chat.id, open('Files/fail.gif', 'rb'))
        if defence['exp'] >= 150 * int(defence['lvl']):
            defence['lvl'] = defence['exp'] // 150 + 1
            bot.send_message(message.chat.id, '{} ты достиг уровня {}! \nСледующий уровень {}/{} XP'.format(defence['name'] + '](tg://user?id=' + reply_id + ')', defence['lvl'], defence['exp'], 150 * int(defence['lvl'])), parse_mode='Markdown')

    read[user_id] = attack
    read[reply_id] = defence
    copy('Files/data_file.json', 'Files/data_file_copy.json')
    json.dump(read, open('Files/data_file.json', 'w', encoding='utf8'), ensure_ascii=False)

def lvl(message):
    read = json.load(open('Files/data_file.json', 'r', encoding='utf8'))
    if message.reply_to_message is None:
        user_id = str(message.from_user.id)
        try:
            attack = read[user_id]
        except:
            read = user_add(read, message)
            attack = read[user_id]
        bot.reply_to(message, 'LVL {} - {}/{} XP'.format(attack['lvl'], attack['exp'], 150 * int(attack['lvl'])))
    else:
        reply_id = str(message.reply_to_message.from_user.id)
        try:
            defence = read[reply_id]
        except:
            read = user_add(read, message.reply_to_message)
            defence = read[reply_id]
        lvl_dif = defence['lvl'] - read[reply_id]['lvl']
        bonus_chance = lvl_dif * 6
        if bonus_chance > 100 - chance - 5:
            bonus_chance = 100 - chance - 5
        elif bonus_chance < 0 - (chance - 5):
            bonus_chance = 0 - (chance - 5)
        success_change = chance + bonus_chance
        bot.reply_to(message, 'Его уровень:\nLVL {} - {}/{} XP\nТвой шанс - {}%'.format(defence['lvl'], defence['exp'], 150 * int(defence['lvl']), success_change))

def rating(message):
    inline = types.InlineKeyboardMarkup()
    lvl = InlineKeyboardButton('По уровню', callback_data='lvl')
    exp = InlineKeyboardButton('По опыту', callback_data='exp')
    take = InlineKeyboardButton('Рейтинг милфхантеров', callback_data='take')
    get = InlineKeyboardButton('Рейтинг слабых на передок', callback_data='get')
    inline.row_width = 2
    inline.add(lvl, exp, get, take)
    msg = bot.reply_to(message, 'Выбери сортировку', reply_markup=inline)
    bot.last_message_sent = msg.chat.id, msg.message_id

def cd(message):
    user_id = str(message.from_user.id)
    read = json.load(open('Files/data_file.json', 'r', encoding='utf8'))
    try:
        last_take = read[user_id]['last_take']
        time_diff = time.time() - last_take
        if time_diff < cooldown:
            time_diff = cooldown - time_diff
            if time_diff > 60:
                time_diff = str(int(time_diff // 60)) + ' мин.'
                bot.reply_to(message, 'Ещё чуть больше {}'.format(time_diff))
            else:
                time_diff = str(int(time_diff)) + ' сек.'
                bot.reply_to(message, 'Ещё {}'.format(time_diff))
        else:
            bot.reply_to(message, 'Уже можно!')
    except:
        bot.reply_to(message, 'Ты не в игре, выеби чью нибудь мать что бы вступить в наш клуб')


mapp = {'/fuck@DickDestroyerBot': fuck, '/lvl@DickDestroyerBot': lvl, '/rating@DickDestroyerBot': rating, '/cd@DickDestroyerBot': cd}

time.sleep(1)
print('started')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    text = message.text
    if text in mapp:
        if message.chat != -1001458417910:
            bot.send_message(message.chat.id, 'Бот написан эксклюзивно для [Белой Комнаты]({})'.format(chat_link), parse_mode='Markdown')
        else:
            mapp[text](message)


bot.polling(none_stop=True, interval=0)
