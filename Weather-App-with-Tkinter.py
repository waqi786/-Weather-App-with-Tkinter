import tkinter as tk
from tkinter import messagebox
import requests
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Weather App')

        self.create_widgets()

    def create_widgets(self):

        self.city_label = tk.Label(self.root, text='Enter city:')
        self.city_label.pack(pady=10)
        self.city_entry = tk.Entry(self.root, width=30)
        self.city_entry.pack()

        self.submit_btn = tk.Button(self.root, text='Get Weather', command=self.fetch_weather)
        self.submit_btn.pack(pady=10)

        self.weather_frame = tk.LabelFrame(self.root, text='Weather Information', padx=20, pady=20)
        self.weather_frame.pack(padx=10, pady=10)

        self.temp_label = tk.Label(self.weather_frame, text='')
        self.temp_label.pack()

        self.desc_label = tk.Label(self.weather_frame, text='')
        self.desc_label.pack()

    def fetch_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning('Warning', 'Please enter a city name.')
            return

        thread = threading.Thread(target=self.get_weather, args=(city,))
        thread.start()

    def get_weather(self, city):
        api_key = 'your_api_key_here'  # Replace with your actual API key
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        try:
            response = requests.get(api_url)
            data = response.json()

            if response.status_code == 200:

                self.root.after(0, self.update_gui, data)
            else:
                messagebox.showerror('Error', f'Error fetching data. Status code: {response.status_code}')
        except Exception as e:
            messagebox.showerror('Error', f'Error occurred: {str(e)}')

    def update_gui(self, data):
        city_name = data['name']
        temperature = data['main']['temp']
        description = data['weather'][0]['description']

        self.temp_label.config(text=f'Temperature in {city_name}: {temperature} °C')
        self.desc_label.config(text=f'Description: {description}')

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
