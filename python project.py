import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
def get_exchange_rate(currency):
    try:
        url = f"https://www.x-rates.com/calculator/?from={currency}&to=INR&amount=1"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rate = soup.find("span", class_="ccOutputTrail").previous_sibling
        return rate
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")
        return None
    except AttributeError:
        messagebox.showerror("Error", "Could not retrieve exchange rate.")
        return None
def update_rate():
    selected_currency = currency_var.get()
    if selected_currency:
        exchange_rate = get_exchange_rate(selected_currency)
        if exchange_rate:
            rate_label.config(text=f"{selected_currency} to INR: {exchange_rate}")
        else:
            rate_label.config(text="Error retrieving rate")
    else:
        rate_label.config(text="Please select a currency")
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    date_time_label.config(text="Last Updated: " + date_time)
def on_currency_change(*args):
    update_rate()
window = Tk()
window.title("Currency Exchange Rate to INR")
window.geometry("400x300")
window.configure(bg="light grey")
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="light grey")
style.configure("TButton", font=("Arial", 10), background="light blue")
currency_var = StringVar()
currency_var.set("USD")  # Default currency
currency_var.trace_add('write', on_currency_change)
currency_options = ["USD", "THB", "EUR", "GBP", "RUB", "CAD", "RSD", "JPY", "AUD", "CNY", "SGD", "CHF", "SEK", "NOK", "BRL", "KRW"]
currency_dropdown = ttk.Combobox(window, textvariable=currency_var, values=currency_options, state="readonly", font=("Arial", 14))
currency_dropdown.pack(pady=15)
rate_label = ttk.Label(window, text="", font=("Arial", 18))
rate_label.pack(pady=20)
date_time_label = ttk.Label(window, text="", font=("Arial", 10))
date_time_label.pack()
refresh_button = ttk.Button(window, text="Refresh", command=update_rate)
refresh_button.pack(pady=10)
update_rate()
window.mainloop()
