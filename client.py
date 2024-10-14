# client.py
import tkinter as tk
from tkinter import messagebox, ttk

import requests

API_URL = "http://127.0.0.1:5000/api/equipment"

class InventoryApp:
    def __init__(self, master):
        self.master = master
        master.title("Inventory Management")
        master.geometry("600x400")

        # Estilo para el árbol (Treeview)
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Frame para el formulario
        self.form_frame = tk.Frame(master, padx=10, pady=10)
        self.form_frame.pack(pady=10)

        self.label = tk.Label(self.form_frame, text="Add New Equipment", font=("Arial", 16))
        self.label.grid(row=0, columnspan=2)

        self.name_label = tk.Label(self.form_frame, text="Name:")
        self.name_label.grid(row=1, column=0, sticky=tk.E)
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.grid(row=1, column=1)

        self.model_label = tk.Label(self.form_frame, text="Model:")
        self.model_label.grid(row=2, column=0, sticky=tk.E)
        self.model_entry = tk.Entry(self.form_frame)
        self.model_entry.grid(row=2, column=1)

        self.quantity_label = tk.Label(self.form_frame, text="Quantity:")
        self.quantity_label.grid(row=3, column=0, sticky=tk.E)
        self.quantity_entry = tk.Entry(self.form_frame)
        self.quantity_entry.grid(row=3, column=1)

        self.location_label = tk.Label(self.form_frame, text="Location:")
        self.location_label.grid(row=4, column=0, sticky=tk.E)
        self.location_entry = tk.Entry(self.form_frame)
        self.location_entry.grid(row=4, column=1)

        self.add_button = tk.Button(self.form_frame, text="Add Equipment", command=self.add_equipment, bg="green", fg="white")
        self.add_button.grid(row=5, columnspan=2, pady=10)

        # Frame para la lista de equipos
        self.list_frame = tk.Frame(master)
        self.list_frame.pack(pady=10)

        self.fetch_button = tk.Button(self.list_frame, text="Fetch Equipment", command=self.fetch_equipment, bg="blue", fg="white")
        self.fetch_button.pack(pady=5)

        self.equipment_list = ttk.Treeview(self.list_frame, columns=("Name", "Model", "Quantity", "Location"), show='headings', height=10)
        self.equipment_list.heading("Name", text="Name")
        self.equipment_list.heading("Model", text="Model")
        self.equipment_list.heading("Quantity", text="Quantity")
        self.equipment_list.heading("Location", text="Location")

        self.equipment_list.column("Name", width=150)
        self.equipment_list.column("Model", width=100)
        self.equipment_list.column("Quantity", width=100)
        self.equipment_list.column("Location", width=150)

        self.equipment_list.pack()

    def add_equipment(self):
        name = self.name_entry.get()
        model = self.model_entry.get()
        quantity = self.quantity_entry.get()
        location = self.location_entry.get()

        if name and model and quantity.isdigit() and location:
            response = requests.post(API_URL, json={
                'name': name,
                'model': model,
                'quantity': int(quantity),
                'location': location
            })
            if response.status_code == 201:
                messagebox.showinfo("Success", "Equipment added successfully")
                self.fetch_equipment()
                self.clear_entries()
            else:
                messagebox.showerror("Error", "Failed to add equipment")
        else:
            messagebox.showwarning("Input Error", "All fields are required and quantity must be a number")

    def fetch_equipment(self):
        for item in self.equipment_list.get_children():
            self.equipment_list.delete(item)
        response = requests.get(API_URL)
        if response.status_code == 200:
            for eq in response.json():
                self.equipment_list.insert('', tk.END, values=(eq['name'], eq['model'], eq['quantity'], eq['location']))
        else:
            messagebox.showerror("Error", "Failed to fetch equipment")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
