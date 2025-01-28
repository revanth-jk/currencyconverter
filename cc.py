import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Function to fetch the exchange rate
def fetch_exchange_rate():
    global rates
    url = "https://api.exchangerate-api.com/v4/latest/USD"  # Example API
    try:
        response = requests.get(url)
        response.raise_for_status()
        rates = response.json()["rates"]
    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch exchange rates: {e}")
        rates = {}

# Function to perform the conversion
def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        if from_currency == to_currency:
            converted_amount = amount
        else:
            converted_amount = (amount / rates[from_currency]) * rates[to_currency]

        result_var.set(f"{converted_amount:.2f} {to_currency}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
    except KeyError:
        messagebox.showerror("Error", "Exchange rates not available. Please refresh.")

# Function to refresh rates
def refresh_rates():
    fetch_exchange_rate()
    messagebox.showinfo("Info", "Exchange rates updated successfully.")

# GUI setup
app = tk.Tk()
app.title("Currency Converter")
app.geometry("400x300")
app.resizable(False, False)

# Variables
from_currency_var = tk.StringVar(value="USD")
to_currency_var = tk.StringVar(value="INR")
amount_var = tk.StringVar()
result_var = tk.StringVar()

# Fetch rates initially
fetch_exchange_rate()

# GUI Widgets
title_label = tk.Label(app, text="Currency Converter", font=("Arial", 16))
title_label.pack(pady=10)

frame = tk.Frame(app)
frame.pack(pady=10)

amount_label = tk.Label(frame, text="Amount:")
amount_label.grid(row=0, column=0, padx=5, pady=5)

amount_entry = ttk.Entry(frame, textvariable=amount_var)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

from_currency_label = tk.Label(frame, text="From Currency:")
from_currency_label.grid(row=1, column=0, padx=5, pady=5)

from_currency_menu = ttk.Combobox(frame, textvariable=from_currency_var, values=list(rates.keys()), state="readonly")
from_currency_menu.grid(row=1, column=1, padx=5, pady=5)

to_currency_label = tk.Label(frame, text="To Currency:")
to_currency_label.grid(row=2, column=0, padx=5, pady=5)

to_currency_menu = ttk.Combobox(frame, textvariable=to_currency_var, values=list(rates.keys()), state="readonly")
to_currency_menu.grid(row=2, column=1, padx=5, pady=5)

convert_button = ttk.Button(app, text="Convert", command=convert_currency)
convert_button.pack(pady=10)

result_label = tk.Label(app, textvariable=result_var, font=("Arial", 14), fg="blue")
result_label.pack(pady=10)

refresh_button = ttk.Button(app, text="Refresh Rates", command=refresh_rates)
refresh_button.pack(pady=5)

# Run the app
app.mainloop()
