import tkinter as tk
import Recognize
import FaceTrain

def open_train(name, number):
    FaceTrain.main(name, number)

def open_recognize(name, number):
    Recognize.main(name, number)

def validate_input():
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        train_btn.config(state="normal")
        recognize_btn.config(state="normal")

def submit_input_train():
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        open_train(name, number)

def submit_input_recognize():
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        open_recognize(name, number)

root = tk.Tk()
root.geometry("450x150+100+100")
root.title("Autolock")

# Name input field
name_label = tk.Label(root, text="Insert User Name(Only Alphabet):")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)
name_entry.focus()
name_entry.bind("<Return>", lambda event: validate_input())

# Number input field
number_label = tk.Label(root, text="Insert User Id(Non-Duplicate number):")
number_label.grid(row=1, column=0)
number_entry = tk.Entry(root)
number_entry.grid(row=1, column=1)
number_entry.bind("<Return>", lambda event: validate_input())

# Train button
train_btn = tk.Button(root, text="Train", state="disabled", command=submit_input_train)
train_btn.grid(row=2, column=0, columnspan=2)

# Recognize button
recognize_btn = tk.Button(root, text="Recognize", state="disabled", command=submit_input_recognize)
recognize_btn.grid(row=2, column=1, columnspan=2)

root.mainloop()
