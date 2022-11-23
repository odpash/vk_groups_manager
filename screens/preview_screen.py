import json
import tkinter as tk
from datetime import datetime

import requests
from PIL import Image, ImageTk

from methods import get_dialogs, get_group_names
from screens import chat_screen
from utils import fonts

api_entry = None


def open_settings():
    global api_entry
    children = tk.Toplevel(W)
    children.title("Настройки")
    children.resizable(width=False, height=False)
    children.minsize(width=600, height=400)
    children.configure(bg="#B0C4DE")
    lbl = tk.Label(
        children,
        text="Настройки",
        font=fonts.BOLD, bg="#F0FFF0")
    lbl.place(x=260, y=25)

    lbl = tk.Label(
        children,
        text="Для добавления нового сообщества введите API ключ",
        font=fonts.BOLD, bg="#F0FFF0")
    lbl.place(x=80, y=60)

    api_entry = tk.Entry(children, width=46, borderwidth=1)
    api_entry.place(x=82, y=90)

    api_add_button = tk.Button(children, text="Добавить")
    api_add_button.config(command=add_new)
    api_add_button.place(x=270, y=125)

    lbl = tk.Label(
        children,
        text="Подключенные сообщества",
        font=fonts.BOLD, bg="#F0FFF0")
    lbl.place(x=180, y=170)
    diff = 0
    for api_key in json.loads(open('api_keys.json', 'r').read()):
        group = get_group_names.get_group_info(api_key)[0]
        img_data = requests.get(group['photo_50']).content
        with open(f'{group["id"]}.jpg', 'wb') as handler:
            handler.write(img_data)
        image = Image.open(f"{group['id']}.jpg")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(children, image=photo)
        label.image = photo
        label.place(x=200, y=200 + diff)

        lbl = tk.Label(
            children,
            text="Название: " + group['name'],
            font=fonts.BOLD, bg="#F0FFF0")
        lbl.place(x=260, y=200 + diff)

        lbl = tk.Button(
            children,
            text=group['online'])
        lbl.place(x=260, y=230 + diff)
        lbl_del = tk.Button(
            children,
            text="Удалить")

        lbl_del.config(command=lambda: delete(api_key))
        lbl_del.place(x=325, y=230 + diff)
        diff += 70


def add_new():
    e = api_entry.get()
    data = json.loads(open('api_keys.json', 'r').read())
    data.append(e)
    with open('api_keys.json', 'w') as f:
        f.write(json.dumps(data))


def delete(api_key):
    data = json.loads(open('api_keys.json', 'r').read())
    data.remove(api_key)
    with open('api_keys.json', 'w') as f:
        f.write(json.dumps(data))


def header(window):
    header_search = tk.Entry(window, width=71, borderwidth=1)
    header_settings_button = tk.Button(text="Настройки")
    header_settings_button.config(command=open_settings)
    header_search.place(x=25, y=5)
    header_settings_button.place(x=700, y=8)


def load_photo(window, m, y_diff):
    img_data = requests.get(m.photo_link).content
    with open(f'{m.peer}.jpg', 'wb') as handler:
        handler.write(img_data)
    image = Image.open(f"{m.peer}.jpg")
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=photo)
    label.image = photo
    label.place(x=33, y=41 + y_diff)
    return label


def load_name(m, y_diff):
    lbl = tk.Label(
        text=f'{m.first_name} {m.last_name} ({m.group_name}) [{datetime.utcfromtimestamp(m.last_message_date).strftime("%H:%M:%S %d-%m-%Y")}]',
        font=fonts.BOLD, bg="#F0FFF0")
    lbl.place(x=90, y=41 + y_diff)
    return lbl


def load_message(window, m, y_diff):
    bg = "#87CEEB" if m.is_unread else "#C0C0C0"
    lbl = tk.Label(window, text="  " + m.last_message_text, width=60, bg=bg, anchor="w")
    lbl.place(x=90, y=70 + y_diff)
    return lbl


def load_button(window, m, y_diff):
    btn = tk.Button(window, height=4, width=71)
    btn.config(command=lambda: chat_screen.main(m.peer, window, m.api_key, m.first_name, m.last_name, m.group_name))
    btn.place(x=28, y=34 + y_diff)
    return btn


update_cycle = []
W = None


def update():
    global update_cycle
    for i in update_cycle:
        i.destroy()
    update_cycle = []
    chats(W)


def chats(window):
    global update_cycle
    y_diff = 0
    delay = 2000
    for m in get_dialogs.run():
        button = load_button(window, m, y_diff)
        photo = load_photo(window, m, y_diff)
        name = load_name(m, y_diff)
        message = load_message(window, m, y_diff)
        update_cycle.append(button)
        update_cycle.append(photo)
        update_cycle.append(name)
        update_cycle.append(message)
        y_diff += 70
    window.after(delay, update)


def start(window):
    global W
    W = window
    header(window)
    chats(window)
