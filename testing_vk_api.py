import datetime

import requests
import vk_api
import wikipedia
import wikipediaapi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

from data import LOGIN, PASSWORD, GROUP_TOKEN, GROUP_ID, ALBUM_ID
from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/vk_stat/<int:group_id>')
def index(group_id):
    vk_session = vk_api.VkApi(LOGIN, PASSWORD,
                              token=GROUP_TOKEN)
    vk_session.auth()
    vk = vk_session.get_api()
    response = vk.stats.get(group_id=group_id, intervals_count=10, access_key=GROUP_TOKEN)
    data = {}
    data['message'] = "access denied!"
    if response:
        data['message'] = 'success'
        data['likes'] = 0
        data['comments'] = 0
        data['subscribed'] = 0
        data['12-18'] = 0
        data['18-21'] = 0
        data['21-24'] = 0
        data['24-27'] = 0
        data['27-30'] = 0
        data['30-35'] = 0
        data['35-45'] = 0
        data['45-100'] = 0
        data['cities'] = set()

        for item in response:
            try:
                data['likes'] += item['activity']['likes']
                data['comments'] += item['activity']['comments']
                data['subscribed'] += item['activity']['subscribed']
                for age in item['reach']['age']:
                    data[age['value']] += age['count']
                for city in item['reach']['cities']:
                    data['cities'].add(city['name'])
            except Exception:
                pass
        data['cities'] = list(data['cities'])
    return render_template('stats.html', data=data)


if __name__ == '__main__':
    app.run()
