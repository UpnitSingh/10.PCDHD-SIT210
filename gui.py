import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the SQLite database
db_path = '/home/Upnit/sensor_data/sensordata.db'

# Function to fetch the latest sensor data
def fetch_sensor_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch the most recent DHT22 data
    cursor.execute("SELECT * FROM dht22_data ORDER BY id DESC LIMIT 5")
    dht22_data = cursor.fetchall()

    # Fetch the most recent MQ5 data
    cursor.execute("SELECT * FROM mq5_data ORDER BY id DESC LIMIT 5")
    mq5_data = cursor.fetchall()

    conn.close()
    return dht22_data, mq5_data

# Function to update the GUI with the latest data
def update_data():
    dht22_data, mq5_data = fetch_sensor_data()

    # Update DHT22 data in GUI
    dht22_list.delete(0, tk.END)
    for row in dht22_data:
        dht22_list.insert(tk.END, f"ID: {row[0]} | Temp: {row[1]}\u00B0C | Humidity: {row[2]}%")

    # Update MQ5 data in GUI
    mq5_list.delete(0, tk.END)
    for row in mq5_data:
        mq5_list.insert(tk.END, f"ID: {row[0]} | Gas Level: {row[1]}")

    # Refresh data every 5 seconds
    root.after(5000, update_data)

# Set up the GUI
root = tk.Tk()
root.title("Real-Time Sensor Data")

# Label for DHT22 data
dht22_label = ttk.Label(root, text="DHT22 Data (Temperature & Humidity)")
dht22_label.pack()

# Listbox for DHT22 data
dht22_list = tk.Listbox(root, width=50, height=5)
dht22_list.pack()

# Label for MQ5 data
mq5_label = ttk.Label(root, text="MQ5 Data (Gas Level)")
mq5_label.pack()

# Listbox for MQ5 data
mq5_list = tk.Listbox(root, width=50, height=5)
mq5_list.pack()

# Start updating the data
update_data()

# Run the GUI main loop
root.mainloop()
