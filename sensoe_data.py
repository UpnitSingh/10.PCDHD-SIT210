import sqlite3
import serial
import time

# Connect to SQLite database
conn = sqlite3.connect('/home/Upnit/sensor_data/sensordata.db')  # Ensure the correct path to your database
cursor = conn.cursor()

# Set up serial connection (adjust port and baud rate as needed)
ser = serial.Serial('/dev/ttyACM0', 115200)  # Use the correct port /dev/ttyACM0

# Function to insert DHT22 data (temperature, humidity)
def insert_dht22_data(temperature, humidity):
    try:
        cursor.execute("INSERT INTO dht22_data (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
        conn.commit()
        print(f"Inserted DHT22 data - Temp: {temperature}, Humidity: {humidity}")
    except Exception as e:
        print(f"Error inserting DHT22 data: {e}")

# Function to insert MQ5 data (gas level)
def insert_mq5_data(gas_level):
    try:
        cursor.execute("INSERT INTO mq5_data (gas_level) VALUES (?)", (gas_level,))
        conn.commit()
        print(f"Inserted MQ5 data - Gas Level: {gas_level}")
    except Exception as e:
        print(f"Error inserting MQ5 data: {e}")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Raw Data: {line}")  # Print the raw serial data

            # Check if the line is in the expected format "DHT:temp,hum" or "MQ5:level"
            if line.startswith("DHT:"):
                try:
                    _, data = line.split(":")
                    temp, hum = map(float, data.split(","))
                    insert_dht22_data(temp, hum)
                except ValueError:
                    print("Malformed DHT data, skipping line")
                    continue  # Skip malformed data

            elif line.startswith("MQ5:"):
                try:
                    _, gas_level = line.split(":")
                    insert_mq5_data(int(gas_level))
                except ValueError:
                    print("Malformed MQ5 data, skipping line")
                    continue  # Skip malformed data

        time.sleep(1)

except KeyboardInterrupt:
    print("Terminated by user")

finally:
    ser.close()
    conn.close()
