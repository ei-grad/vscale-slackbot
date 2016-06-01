Бот для Slack для vscale.io
===========================

Бот позволяет:

- создавать/запускать/останавливать сервера
- сообщает о заканчивающихся средствах на счете

Установка
---------

```bash
pip install git+https://github.com/ei-grad/vscale-slackbot.git
```

Настройка
---------

В файл `slackbot_settings.py` (в директории откуда будем запускать бота) добавляем строчки:

```python
API_TOKEN = "<your-slack-api-token>"
VSCALE_TOKEN = "<your-vscale-token>"
```

Запуск
------

```bash
vscale-slackbot
```
