import tkinter as tk

from methods import get_message_history


def main(peer, window, api_key, name, surname, group):
    children = tk.Toplevel(window)
    children.title("Настройки")
    children.resizable(width=False, height=False)
    children.minsize(width=800, height=600)
    children.configure(bg="#B0C4DE")
    diff = 0
    messages_db = get_message_history.get_story(api_key, peer)
    for i in messages_db['response']['items']:
        lbl = tk.Label(
            children,
            text=name + ' ' + surname + f' [{group}]: ' + i['text']
        )
        lbl.place(x=25, y=520 - diff)
        diff += 30
    lbl = tk.Entry(
        children,
        width=75)
    lbl.place(x=25, y=550)

    btn = tk.Button(
        children,
        text='Отправить'
    )
    btn.place(x=720, y=553)
