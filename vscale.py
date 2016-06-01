#!/usr/bin/env python
# encoding: utf-8

import requests

from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

from slackbot_settings import VSCALE_TOKEN


def get_images():
    return {
        i['id'].split('_')[0]: i
        for i in requests.get('https://api.vscale.io/v1/images').json()
    }


def get_rplans():
    return {
        i['id']: i
        for i in requests.get('https://api.vscale.io/v1/rplans').json()
    }


@respond_to(u'планы')
def rplans(message):
    message.reply(u'Доступные размеры машин:\n{}'.format('\n'.join(
        '- {id} ({cpus}xCPU, {memory}Mb RAM, )'.format(**i)
        for i in requests.get('https://api.vscale.io/v1/rplans').json()
    )))


@respond_to(u'создай ([^ ]+)( [^ ]+)', re.IGNORECASE)
def create(message, image, rplan):

    images = get_images()
    if image not in images:
        message.reply(u'На vscale.io нет такой операционной системы :-(')
        return

    resp = requests.post(
        'https://api.vscale.io/v1/scalets',
        params={
            'make_from': images[image]['id'],
            'rplan': rplan,
        },
        headers={'X-Token': VSCALE_TOKEN},
    ).json()

    info = requests.get(
        'https://api.vscale.io/v1/scalets/{ctid}'.format(resp['ctid']),
        headers={'X-Token': VSCALE_TOKEN},
    ),
    message.reply((u'Машина {name} (#{ctid}) создана, адрес: '
                   u'{public_address.address}').format(**info))


@respond_to(u'запусти ([^ ]+)', re.IGNORECASE)
def run(message, name):

    scalets = requests.get(
        'https://api.vscale.io/v1/scalets',
        headers={'X-Token': VSCALE_TOKEN},
    )

    info = None
    for i in scalets:
        if i['name'] == name:
            info = i
    if info is None:
        message.reply(u"Не знаю такой машины :-(")
        return

    resp = requests.post(
        'https://api.vscale.io/v1/scalets/{ctid}/run'.format(**info),
        headers={'X-Token': VSCALE_TOKEN},
    ).json()
    message.reply(u'Машина #{ctid} запущена'.format(**resp))


@listen_to(u'останови ([^ ]+)', re.IGNORECASE)
def stop(message, name):

    scalets = requests.get(
        'https://api.vscale.io/v1/scalets',
        headers={'X-Token': VSCALE_TOKEN},
    )

    info = None
    for i in scalets:
        if i['name'] == name:
            info = i
    if info is None:
        message.reply(u"Не знаю такой машины :-(")
        return

    resp = requests.post(
        'https://api.vscale.io/v1/scalets/{ctid}/stop'.format(**info),
        headers={'X-Token': VSCALE_TOKEN},
    ).json()
    message.reply(u'Машина #{ctid} остановлена'.format(**resp))


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
