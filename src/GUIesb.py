import html
from tkinter import *
from tkinter import filedialog as fd

import requests

MSK_URL = 'http://10.28.43.16:26011/logmonitor/LogSearcher?dName=esb_rtkdev3&sName=osb_server1&sText='

root = Tk()

e = Entry(width=20)  # текстовое поле
msk_button = Button(text="MSKDEV3")  # кнопка
b2 = Button(text="Сохранить")
log_file_label = Label(bg='white', fg='black')  # метка


def search_file_log_msk(event):
    log_file_label['text'] = ' '
    s = requests.get(MSK_URL + e.get())
    global result
    result = re.findall(r'(?=<b>(osb_server1.log\d*))', html.unescape(s.text))
    for file_element in result:
        log_file_label['text'] += file_element + '\n'


def extract_text(event):
    file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"), ("All files", "*.*")))
    f = open(file_name, 'w')
    for element in result:
        f.write(element + '\n'*5)
        page = requests.get(
            'http://10.28.43.16:26011/logmonitor/LogViewer?type=raw&dName=esb_rtkdev3&sName=osb_server1&lName=' +
            element, stream=True)
        page = str(page.content.decode('utf-8'))
        page = re.split(r'(?=####)', page)
        for elem_page in page:
            if str(e.get()) in elem_page:
                f.write(elem_page + '\n\n\n')
    f.close()


def init_gui():
    msk_button.bind('<Button-1>', search_file_log_msk)
    # функции, которые вызываются при наступлении события. <Button-1> - щелчок левой кнопкой мыши
    b2.bind('<Button-1>', extract_text)
    e.pack()  # расположим элементы друг за другом с помощью наиболее простого менеджера геометрии tkinter
    msk_button.pack()
    log_file_label.pack()
    b2.pack()
    root.mainloop()  # приводит к отображению главного окна со всеми его причиндалами на экране


if __name__ == '__main__':
    init_gui()
