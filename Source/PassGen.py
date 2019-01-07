import secrets as s
from tkinter import *
from tkinter import Tk, Frame, Entry, messagebox, ttk
import json


def gui_main():

    main_window = Tk()
    main_window.title('PassGen')

    # output file
    path = "data\PassKeep.json"

    # some globals
    load_values = []

    # get the passwords from file
    with open(path) as jsonSets:
        data = json.load(jsonSets)

        for k, v in data.get("Passwords").items():
            load_values.append(v.get('website'))

    # tab creation
    tabs ={}

    notebook = ttk.Notebook(main_window)
    notebook.grid()

    tabs["save_tab"] = ttk.Frame(notebook)
    tabs["load_tab"] = ttk.Frame(notebook)

    notebook.add(tabs["save_tab"], text="Save")
    notebook.add(tabs["load_tab"], text="Load")

    # create the frames inside of the save tab
    frames = {}

    frames["main_frame"] = LabelFrame(tabs["save_tab"], text="Generate", labelanchor=NW, padx=5, pady=5)
    frames["main_frame"].grid(row=1, column=0)

    frames["options_frame"] = LabelFrame(tabs["save_tab"], text="Options", labelanchor=NW, padx=5, pady=5)
    frames["options_frame"].grid(row=0, column=0, sticky=W)

    # create the checkbuttons in the options frame
    has_special_chars = IntVar(value=1)
    has_numbers_checkbutton = Checkbutton(frames["options_frame"], text="Special characters",
                                          variable=has_special_chars)
    has_numbers_checkbutton.grid(row=0, column=0, sticky=W)

    has_numbers = IntVar(value=1)
    has_numbers_checkbutton = Checkbutton(frames["options_frame"], text="Numbers", variable=has_numbers)
    has_numbers_checkbutton.grid(row=1, column=0, sticky=W)

    has_lowercase = IntVar(value=1)
    has_lowercase_checkbutton = Checkbutton(frames["options_frame"], text="Lowercase characters",
                                            variable=has_lowercase)
    has_lowercase_checkbutton.grid(row=2, column=0, sticky=W)

    has_uppercase = IntVar(value=1)
    has_uppercase_checkbutton = Checkbutton(frames["options_frame"], text="Uppercase characters",
                                            variable=has_uppercase)
    has_uppercase_checkbutton.grid(row=3, column=0, sticky=W)

    # get the length of the password
    length_label = ttk.Label(frames["main_frame"], text="Enter password length:")
    length_label.grid(row=0, column=0, sticky=W)

    length_entry = ttk.Entry(frames["main_frame"])
    length_entry.insert(0, '10')
    length_entry.grid(row=0, column=1, sticky=W)

    # get the name of the website
    website_label = ttk.Label(frames["main_frame"], text="Enter name of the website:")
    website_label.grid(row=1, column=0, sticky=W)

    website_entry = ttk.Entry(frames["main_frame"])
    website_entry.insert(0, 'Website')
    website_entry.grid(row=1, column=1, sticky=W)

    # generate the password
    generate_button = ttk.Button(frames["main_frame"], text="Generate Password", command=lambda: generate_password())
    generate_button.grid(row=2, column=0, sticky=W)

    pass_entry = ttk.Entry(frames["main_frame"])
    pass_entry.grid(row=2, column=1)
    pass_entry.insert(0, 'Password')

    # save the password
    save_button = ttk.Button(frames["main_frame"], text="save", command=lambda: save_password())
    save_button.grid(row=3, column=1, sticky=E)

    # create frames in the Load tab
    frames["load_frame"] = LabelFrame(tabs["load_tab"], text="Load Password", labelanchor=NW)
    frames["load_frame"].grid(row=0, column=0)

    # create options in the load password frame
    load_label = ttk.Label(frames["load_frame"], text="Choose password:")
    load_label.grid(row=0, column=0)

    # combobox for loading passwords from file
    load_combobox = ttk.Combobox(frames["load_frame"])
    load_combobox.set("None")
    load_combobox.grid(row=0, column=1)
    load_combobox.config(values = load_values)

    #load password button
    load_password_button = ttk.Button(frames["load_frame"], text="Load", command=lambda: load_password())
    load_password_button.grid(row=0, column=2)

    load_password_label = ttk.Label(frames["load_frame"], text="Password is:")
    load_password_label.grid(row=1, column=0, sticky=W)

    load_password_entry = ttk.Entry(frames["load_frame"], text="Password")
    load_password_entry.grid(row=1, column=1, sticky=W+E+N+S)

    def generate_password():
        chosen_options = 25
        if(has_special_chars.get() == 1):
            if(has_numbers.get() == 1):
                chosen_options=45
            else:
                chosen_options=35
        incomplete_pass = ""
        chars = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                 's', 't', 'u', 'v', 'x', 'y', 'z', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        specials = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')')
        nums = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        if (has_special_chars.get() == 1) & (has_numbers.get() == 1):
            choices = chars + specials + nums
            incomplete_pass = s.choice(choices)
        elif (has_special_chars.get() == 1) & (has_numbers.get() == 0):
            choices = chars + specials
        elif (has_special_chars.get() == 0) & (has_numbers.get() == 1):
            choices = chars + nums

        try:
            for i in range(0, int((length_entry.get()))):
                incomplete_pass += s.choice(choices)
                pass_entry.delete(0, len(pass_entry.get()))
                pass_entry.insert(0, incomplete_pass)
        except ValueError:
            messagebox.showerror(title="Error", message="Invalid input")
#       try:
#           for i in range(0, int((length_entry.get()))):
#               incomplete_pass += chars[s.randbelow(chosen_options)]
#            pass_entry.delete(0, len(pass_entry.get()))
#            pass_entry.insert(0, incomplete_pass)


    def save_password():
        """
        saves the passwords to a dictionary stored in a json file
        """
        website_name = website_entry.get()
        pass_name = pass_entry.get()
        data["Passwords"][website_name] = {
            "website": website_name,
            "password": pass_name
        }
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def load_password():
        settings_name = load_combobox.get()
        settings_string = data['Passwords'][settings_name].get('password')
        load_password_entry.delete(0, len(load_password_entry.get()))
        load_password_entry.insert(0, settings_string)

    main_window.mainloop()


if __name__ == '__main__':
    gui_main()
