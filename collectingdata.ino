#include <DHT.h>
#include <FreeRTOS.h>
#include <task.h>

// Pin configurations
#define DHTPIN 2        // DHT22 sensor connected to pin 2
#define DHTTYPE DHT22   // Define DHT sensor type
DHT dht(DHTPIN, DHTTYPE);

#define MQ5PIN A0       // MQ5 sensor connected to analog pin A0
#define BUZZER_PIN 3    // Buzzer connected to digital pin 3

// Thresholds for the sensors
const float TEMP_THRESHOLD = 50.0;     // Temperature threshold in °C
const int MQ5_THRESHOLD = 500;         // MQ5 gas sensor threshold (adjustable)

// Task handles
TaskHandle_t TaskDHTHandle;
TaskHandle_t TaskMQ5Handle;
TaskHandle_t TaskAlarmHandle;

// DHT22 Sensor reading task
void readDHTSensor(void *pvParameters) {
  while (true) {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
    } else {
      // Send data in the required format
      Serial.print("DHT:");
      Serial.print(temperature, 1);  // 1 decimal place
      Serial.print(",");
      Serial.println(humidity, 1);   // 1 decimal place
    }

    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}

// MQ5 Sensor reading task
void readMQ5Sensor(void *pvParameters) {
  while (true) {
    int mq5Value = analogRead(MQ5PIN);

    // Send data in the required format
    Serial.print("MQ5:");
    Serial.println(mq5Value);

    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}

// Alarm task to trigger buzzer if thresholds are crossed
void alarmIfCritical(void *pvParameters) {
  while (true) {
    float temperature = dht.readTemperature();
    int mq5Value = analogRead(MQ5PIN);

    if (temperature > TEMP_THRESHOLD || mq5Value > MQ5_THRESHOLD) {
      Serial.println("ALERT! Critical condition detected. Triggering alarm!");
      digitalWrite(BUZZER_PIN, HIGH);  // Turn on buzzer
    } else {
      digitalWrite(BUZZER_PIN, LOW);   // Turn off buzzer if no critical condition
    }

    vTaskDelay(500 / portTICK_PERIOD_MS);  // Check more frequently for critical conditions
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Initialize buzzer pin as output
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);  // Ensure the buzzer is off initially

  // Create FreeRTOS tasks
  xTaskCreate(readDHTSensor, "Read DHT Sensor", 1024, NULL, 1, &TaskDHTHandle);
  xTaskCreate(readMQ5Sensor, "Read MQ5 Sensor", 1024, NULL, 1, &TaskMQ5Handle);
  xTaskCreate(alarmIfCritical, "Alarm if Critical", 1024, NULL, 2, &TaskAlarmHandle);  // Higher priority for alarm

  // Start the RTOS scheduler
  vTaskStartScheduler();
}

void loop() {
  // Empty because FreeRTOS is handling tasks
}
