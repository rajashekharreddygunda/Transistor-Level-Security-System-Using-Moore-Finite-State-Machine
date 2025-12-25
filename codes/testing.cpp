/*
  Measure Period and Pulse Width using ADC
  Works for analog signals
*/

const int analogPin = A0;
const int threshold = 512; // ~2.5V (for 5V ADC)

unsigned long tRise = 0;
unsigned long tFall = 0;
unsigned long tPrevRise = 0;

unsigned long period_us = 0;
unsigned long high_us = 0;
bool lastAbove = false;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  int adc = analogRead(analogPin);
  unsigned long now = micros();
  bool above = adc > threshold;

  // Rising threshold crossing
  if (above && !lastAbove) {
    tPrevRise = tRise;
    tRise = now;
    if (tPrevRise != 0)
      period_us = tRise - tPrevRise;
  }

  // Falling threshold crossing
  if (!above && lastAbove) {
    tFall = now;
    high_us = tFall - tRise;

    if (period_us > 0) {
      float freq = 1000000.0 / period_us;
      float duty = (high_us * 100.0) / period_us;

      Serial.print("Period: ");
      Serial.print(period_us);
      Serial.print(" us | Frequency: ");
      Serial.print(freq, 2);
      Serial.print(" Hz | High Time: ");
      Serial.print(high_us);
      Serial.print(" us | Duty: ");
      Serial.print(duty, 2);
      Serial.println(" %");
    }
  }

  lastAbove = above;
}
