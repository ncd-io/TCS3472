// This #include statement was automatically added by the Particle IDE.
#include "TCS3472.h"

TCS3472 sensor;

void setup() {
    sensor.init();
    Particle.variable("Red", sensor.red);
    Particle.variable("Green", sensor.green);
    Particle.variable("Blue", sensor.blue);
    Particle.variable("Clear", sensor.clear);
    Particle.variable("RGB", sensor.rgb);
}

void loop() {
    sensor.loop();
}
