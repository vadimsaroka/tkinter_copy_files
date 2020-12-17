import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import subprocess


def copy_from_open_path():
    """Open a folder for copy from"""
    entry1.delete(0, tk.END)
    copy_from_folder = askdirectory(initialdir="/home")
    entry1.insert(index=0, string=copy_from_folder)
    label_msg["text"] = f""


def copy_to_open_path():
    """Open a folder for copy to"""
    entry2.delete(0, tk.END)
    copy_to_folder = askdirectory(initialdir="/home")
    entry2.insert(index=0, string=copy_to_folder)
    label_msg["text"] = f""


def start_copy():
    """Start copying"""
    if not entry1.get():
        label_msg["text"] = f"You must specify 'Copy from' path"
        return

    if not entry2.get():
        label_msg["text"] = f"You must specify 'Copy to' path"
        return

    bash_command = f"rsync -a -v --ignore-existing {entry1.get()} {entry2.get()}"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        label_msg["text"] = f"{error}"
        print(error)

    if not error and du(entry1.get()) == du(entry2.get()):
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        label_msg["text"] = f"Finished"


def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du', '-sh', path]).split()[0].decode('utf-8')


window = tk.Tk()

window.title("Copy Plus")
window.geometry("500x600")
window.minsize(width=380, height=450)

frame = tk.Frame(window, bg="white")
frame.place(relwidth=1, relheight=1)

label1 = tk.Label(frame, text="Copy from: ", bg="white")
label1.place(rely=0.2, relx=0.2, width=80, height=30)

label2 = tk.Label(frame, text="Copy to: ", bg="white")
label2.place(rely=0.32, relx=0.2, width=63, height=30)

label_msg = tk.Label(frame, text="", bg="white", anchor="w")
label_msg.place(relwidth=0.60, relheight=0.1, rely=0.56, relx=0.2)

entry1 = tk.Entry(frame)
entry1.place(rely=0.25, relx=0.2, relwidth=0.39, height=30)

entry2 = tk.Entry(frame)
entry2.place(rely=0.37, relx=0.2, relwidth=0.39, height=30)

button1 = tk.Button(frame, text="Browse", command=copy_from_open_path)
button1.place(rely=0.25, relx=0.6, width=130, height=30)

button2 = tk.Button(frame, text="Browse", command=copy_to_open_path)
button2.place(rely=0.37, relx=0.6, width=130, height=30)

button3 = tk.Button(frame, text="Start", command=start_copy)
button3.place(rely=0.48, relx=0.2, width=130, height=30)

window.mainloop()
