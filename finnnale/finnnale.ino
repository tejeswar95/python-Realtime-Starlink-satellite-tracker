#include <Wire.h>
#include <MPU6050_tockn.h>
#include <Servo.h>

// Define the pins for servo motors
#define HORIZONTAL_SERVO_PIN 6
#define VERTICAL_SERVO_PIN 9

// Create servo objects
Servo horizontalServo;
Servo verticalServo;

// Create an instance of the MPU6050 class
MPU6050 mpu6050(Wire);

// Target orientation (x=0, y=0, z=0)
const float targetX = 0.0;
const float targetY = 0.0;
const float targetZ = 0.0;

// Tolerance range within which the orientation is considered aligned
const float tolerance = 0.05;

// Function to set servo angles
void setServoAngle(Servo &servo, int angle) {
  // Ensure the angle is within bounds (0 to 180 degrees)
  angle = constrain(angle, 0, 180);
  servo.write(angle);
}

void setup() {
  // Start the serial communication
  Serial.begin(9600);

  // Initialize MPU6050
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);

  Serial.println("MPU6050 initialized successfully!");

  // Attach servos to pins
  horizontalServo.attach(HORIZONTAL_SERVO_PIN);
  verticalServo.attach(VERTICAL_SERVO_PIN);
}

void loop() {
  // Update MPU6050 values
  mpu6050.update();

  // Read accelerometer values
  float accelX = mpu6050.getAccX();
  float accelY = mpu6050.getAccY();
  float accelZ = mpu6050.getAccZ();

  // Print out the accelerometer values
  Serial.print("X = ");
  Serial.print(accelX);
  Serial.print(" Y = ");
  Serial.print(accelY);
  Serial.print(" Z = ");
  Serial.println(accelZ);
 
  // Check if the current orientation is within the tolerance range of the target
  if (abs(accelX - targetX) > tolerance || abs(accelY - targetY) > tolerance || abs(accelZ - targetZ) > tolerance) {
    // Calculate servo angles to reduce the difference
    int horizontalAngle = map(accelX * 100, -200, 200, 0, 180);
    int verticalAngle = map(accelY * 100, -200, 200, 0, 180);

    // Set servo angles
    setServoAngle(horizontalServo, horizontalAngle);
    setServoAngle(verticalServo, verticalAngle);
  } else {
    // If within tolerance, hold position (optional, can be adjusted)
    setServoAngle(horizontalServo,90); // Neutral position, adjust as needed
    setServoAngle(verticalServo, 90);   // Neutral position, adjust as needed
  }

  // Add a small delay to avoid excessive servo movement
  delay(100);
}