import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('/home/Upnit/sensor_data/sensordata.db')
cursor = conn.cursor()

# Fetch the most recent DHT22 data
cursor.execute("SELECT * FROM dht22_data ORDER BY id DESC LIMIT 5")
dht22_data = cursor.fetchall()

# Fetch the most recent MQ5 data
cursor.execute("SELECT * FROM mq5_data ORDER BY id DESC LIMIT 5")
mq5_data = cursor.fetchall()

# Display the fetched data
print("Latest DHT22 Data (Temp, Humidity):")
for row in dht22_data:
    print(row)

print("\nLatest MQ5 Data (Gas Level):")
for row in mq5_data:
    print(row)

# Close the database connection
conn.close()
