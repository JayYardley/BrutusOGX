import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import time
import json

# REPLACEMENTS - Defines the default Hex code for BrutusOGX to look for by default
REPLACEMENTS = {
    "Auto 720p": {"search": bytes.fromhex('8002E001'), "replace": bytes.fromhex('0005D002')},
    "Window View": {
        "search": [bytes.fromhex('010707'), bytes.fromhex('010808'), bytes.fromhex('010F11')],
        "replace": bytes.fromhex('020A0B')
    }
}

#Set file path to null for initialization
file_path = None

def load_custom_replacements():
    custom_dir = "CustomValues"
    if not os.path.exists(custom_dir):
        os.makedirs(custom_dir)
    for filename in os.listdir(custom_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(custom_dir, filename)
            with open(filepath, 'r') as file:
                custom_data = json.load(file)
                key = custom_data["name"]
                search_bytes = bytes.fromhex(custom_data["search"])
                replace_bytes = bytes.fromhex(custom_data["replace"])
                REPLACEMENTS[key] = {"search": search_bytes, "replace": replace_bytes}
                add_checkbox(key)

def save_custom_replacement(name, search, replace):
    os.makedirs("CustomValues", exist_ok=True)
    data = {"name": name, "search": search, "replace": replace}
    with open(os.path.join("CustomValues", f"{name}.json"), 'w') as file:
        json.dump(data, file)

def check_file():
    global file_path
    if not file_path:
        return messagebox.showwarning("Warning", "Please open a file first.")
    
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        matches = []
        options = {key: {"enabled": var.get(), **value} for key, (var, value) in zip(REPLACEMENTS.keys(), zip(checkbox_vars, REPLACEMENTS.values()))}

        def find_matches(search_value, prefix=b''):
            start = 0
            while (start := file_data.find(prefix + search_value, start)) != -1:
                end = start + len(prefix) + len(search_value)
                matches.append((option, start, end, prefix + search_value))
                start = end
        
        for option, hex_data in options.items():
            if hex_data["enabled"]:
                if option == "Window View":
                    for search_value in hex_data["search"]:
                        find_matches(search_value, REPLACEMENTS["Auto 720p"]["search"])
                else:
                    find_matches(hex_data["search"])

        if matches:
            display_matches(matches)
            save_results(matches)
        else:
            messagebox.showinfo("Info", "No matching hex values were found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_matches(matches):
    matches_window = tk.Toplevel(root)
    matches_window.title("Matched Data")

    frame = ttk.Frame(matches_window)
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    scrollbar = ttk.Scrollbar(frame)
    text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, wrap='word')

    scrollbar.pack(side="right", fill="y")
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_widget.yview)

    checkboxes = []

    for index, (option, start, end, data) in enumerate(matches, start=1):
        match_text = f"{index}. {option}: Offset {start} to {end}, Data: {data.hex().upper()}"

        var = tk.BooleanVar()
        checkbox_frame = ttk.Frame(text_widget)
        ttk.Checkbutton(checkbox_frame, variable=var).pack(side="left")

        text_widget.window_create("end", window=checkbox_frame)
        text_widget.insert("end", match_text + "\n")
        checkboxes.append((var, (option, start, end, data)))

    button_frame = ttk.Frame(matches_window)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Select All", command=lambda: select_all_checkboxes(checkboxes)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Patch", command=lambda: patch_selected(matches, checkboxes)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Brute Mode", command=lambda: generate_brute_mode(matches, checkboxes)).pack(side="left", padx=5)

def save_results(matches):
    try:
        os.makedirs("Results", exist_ok=True)
        filename = f"Results/results-{time.strftime('%Y%m%d-%H%M%S')}.txt"
        with open(filename, "w") as file:
            for option, start, end, data in matches:
                file.write(f"{option}: Offset {start} to {end}, Data: {data.hex().upper()}\n")
        messagebox.showinfo("Success", "Results saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

#Apply single patch
def patch_selected(matches, checkboxes):
    global file_path
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        for var, match in checkboxes:
            if var.get():
                file_data = apply_patch(file_data, match)
        new_file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        if new_file_path:
            with open(new_file_path, 'wb') as file:
                file.write(file_data)
            messagebox.showinfo("Success", "Selected hex replacements completed successfully.")
        else:
            messagebox.showwarning("Warning", "File save was canceled.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def apply_patch(file_data, match):
    option, start, end, search = match

    if option == "Window View":
        replace = REPLACEMENTS["Window View"]["replace"]
        search_len = len(search) - len(REPLACEMENTS["Auto 720p"]["search"])
        file_data = bytearray(file_data)
        file_data[start + len(REPLACEMENTS["Auto 720p"]["search"]):start + len(REPLACEMENTS["Auto 720p"]["search"]) + search_len] = replace
    else:
        replace = REPLACEMENTS[option]["replace"]
        file_data = bytearray(file_data)
        file_data[start:end] = replace

    return bytes(file_data)

#Apply multi-select patch via Brute Mode
def generate_brute_mode(matches, checkboxes):
    try:
        if not os.path.exists("Brute Mode"):
            os.makedirs("Brute Mode")

        for index, (var, match) in enumerate(checkboxes, start=1):
            if var.get():
                file_data = apply_patch(open(file_path, 'rb').read(), match)
                filename = f"Brute Mode/{index}.xbe"
                with open(filename, 'wb') as file:
                    file.write(file_data)

        messagebox.showinfo("Success", "Brute Mode patch outputs generated successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo("Info", "File loaded successfully.")

def add_custom_replacement():
    key = simpledialog.askstring("Input", "Enter a name for the replacement:")
    if key:
        search = simpledialog.askstring("Input", "Enter the hex value to search for (in hex, without spaces):")
        replace = simpledialog.askstring("Input", "Enter the hex value to replace with (in hex, without spaces):")
        if search and replace:
            search_bytes = bytes.fromhex(search)
            replace_bytes = bytes.fromhex(replace)
            REPLACEMENTS[key] = {"search": search_bytes, "replace": replace_bytes}
            add_checkbox(key)
            save_custom_replacement(key, search, replace)

def add_checkbox(key):
    var = tk.BooleanVar()
    checkbox = ttk.Checkbutton(frame, text=key, variable=var)
    checkbox.pack(anchor='w')
    checkbox_vars.append(var)

def select_all_checkboxes(checkboxes):
    for var, _ in checkboxes:
        var.set(True)

root = tk.Tk()
root.title("BrutusOGX 0.2")
##custom icon
##root.wm_iconbitmap(r'C:\Users\username\Desktop\BrutusOGX\image.ico')

style = ttk.Style()
style.theme_use('clam')

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

checkbox_vars = []
for option in REPLACEMENTS.keys():
    add_checkbox(option)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

open_button = ttk.Button(button_frame, text="Open File", command=open_file)
open_button.pack(side="left", padx=5)

check_button = ttk.Button(button_frame, text="Check", command=check_file)
check_button.pack(side="left", padx=5)

custom_button = ttk.Button(button_frame, text="Add Custom Replacement", command=add_custom_replacement)
custom_button.pack(side="left", padx=5)

load_custom_replacements()

root.mainloop()
