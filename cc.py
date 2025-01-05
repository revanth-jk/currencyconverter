import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x600")
        self.root.config(bg="#121212")  # Dark mode background

        # API Configuration
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"
        self.primary_color = "#1F6FEB"
        self.secondary_color = "#212121"
        self.text_color = "#E0E0E0"
        self.font_family = "Roboto"
        self.font_size = 14

        # Configure modern fonts
        self.heading_font = Font(family=self.font_family, size=20, weight="bold")
        self.text_font = Font(family=self.font_family, size=self.font_size)
        self.result_font = Font(family=self.font_family, size=16, slant="italic")

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, text="Currency Converter",
            font=self.heading_font, bg="#121212", fg=self.primary_color
        )
        title_label.pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#121212")
        input_frame.pack(pady=20)

        # Amount Input
        tk.Label(input_frame, text="Enter Amount:", font=self.text_font, bg="#121212", fg=self.text_color).grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(input_frame, font=self.text_font, width=20, bd=0, relief="flat", bg=self.secondary_color, fg=self.text_color, insertbackground=self.text_color)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)
        self.amount_entry.insert(0, "Enter amount")
        self.amount_entry.bind("<FocusIn>", lambda event: self.amount_entry.delete(0, tk.END))

        # From Currency
        tk.Label(input_frame, text="From Currency:", font=self.text_font, bg="#121212", fg=self.text_color).grid(row=1, column=0, padx=10, pady=10)
        self.from_currency_combobox = ttk.Combobox(input_frame, font=self.text_font, width=18, state="readonly")
        self.from_currency_combobox.grid(row=1, column=1, pady=10)

        # To Currency
        tk.Label(input_frame, text="To Currency:", font=self.text_font, bg="#121212", fg=self.text_color).grid(row=2, column=0, padx=10, pady=10)
        self.to_currency_combobox = ttk.Combobox(input_frame, font=self.text_font, width=18, state="readonly")
        self.to_currency_combobox.grid(row=2, column=1, pady=10)

        # Convert Button
        convert_button = tk.Button(
            self.root, text="Convert", command=self.convert_currency,
            font=self.text_font, bg=self.primary_color, fg="white",
            relief="flat", overrelief="solid", bd=0, highlightthickness=0
        )
        convert_button.pack(pady=20, ipadx=20, ipady=10)

        # Result Display
        self.result_label = tk.Label(self.root, text="", font=self.result_font, bg="#121212", fg=self.primary_color)
        self.result_label.pack(pady=10)

        # Real-Time Rate
        self.usd_inr_label = tk.Label(self.root, text="Fetching USD to INR rate...", font=self.text_font, bg="#121212", fg=self.text_color)
        self.usd_inr_label.pack(pady=5)

        # Footer
        footer_label = tk.Label(self.root, text="Designed by Punithan", font=("Roboto", 10), bg="#121212", fg="#757575")
        footer_label.pack(side="bottom", pady=20)

        # Load Data
        self.load_currencies()
        self.fetch_usd_to_inr_rate()

    def load_currencies(self):
        try:
            response = requests.get(self.api_url + "USD")
            data = response.json()
            currencies = list(data["rates"].keys())

            # Populate comboboxes
            self.from_currency_combobox["values"] = currencies
            self.to_currency_combobox["values"] = currencies
            self.from_currency_combobox.set("USD")
            self.to_currency_combobox.set("INR")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load currencies: {e}")

    def fetch_usd_to_inr_rate(self):
        try:
            response = requests.get(self.api_url + "USD")
            data = response.json()
            usd_to_inr = data["rates"]["INR"]
            self.usd_inr_label.config(text=f"1 USD = {usd_to_inr:.2f} INR")
            self.root.after(60000, self.fetch_usd_to_inr_rate)  # Refresh every 60 seconds
        except Exception as e:
            self.usd_inr_label.config(text="Error fetching USD to INR rate.")

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_combobox.get()
            to_currency = self.to_currency_combobox.get()

            response = requests.get(self.api_url + from_currency)
            data = response.json()
            rates = data["rates"]

            if to_currency in rates:
                converted_amount = amount * rates[to_currency]
                self.result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            else:
                self.result_label.config(text="Invalid target currency.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
