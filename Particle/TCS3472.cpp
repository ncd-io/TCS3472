#include "TCS3472.h"


void TCS3472::init(){
    begin();
    sendCommand(TCS3472_ENABLE_REG, wait_en | TCS3472_ENABLE_RGBC | TCS3472_ENABLE_POWER);
    
    sendCommand(TCS3472_CONTROL_REG, gain);
    sendCommand(TCS3472_TIMING_REG, timing);
    sendCommand(TCS3472_WAIT_REG, wtime);
    
    if(wlong) sendCommand(TCS3472_CONFIG_REG, TCS3472_WLONG);
}

void TCS3472::takeReadings(){
    int data[8];
    readBuffer(TCS3472_COMMAND_REG | TCS3472_DATA_REGISTER_0, data, 8);
    clear = data[0] + (data[1] << 8);
    red = data[2] + (data[3] << 8);
    green = data[4] + (data[5] << 8);
    blue = data[6] + (data[7] << 8);
    toRGB();
}

void TCS3472::toRGB(){
    int high = max(red, max(green, blue));
    float mult = (255 / (float)high);
    rgb = String((int)(red * mult));
    rgb.concat(",");
    rgb.concat((int)(green * mult));
    rgb.concat(",");
    rgb.concat((int)(blue * mult));
}

int TCS3472::readRate(){
    return (int)((256 - timing) * 2.4) + (((256 - wtime) * 2.4) * (wlong ? 12 : 1)) + 7.4;
}

void TCS3472::loop(){
    if(loop_delay == 0){
        loop_delay = readRate();
    }
    int now = millis();
    if(now-last_checked > 1000){
        last_checked = now;
        takeReadings();
    }
}

void TCS3472::sendCommand(int reg, int data){
    writeByte(TCS3472_COMMAND_REG | reg, data);
}

void TCS3472::begin(){
    if(!Wire.isEnabled()) Wire.begin();
}

void TCS3472::writeByte(int reg, int data){
    Wire.beginTransmission(address);
    Wire.write(reg);
    if(data < 256) Wire.write(data);
    Wire.endTransmission();
}

int TCS3472::readByte(int reg){
    writeByte(reg, 256);
    Wire.requestFrom(address, 1);
    return Wire.read();
}

void TCS3472::readBuffer(int reg, int *buff, int len){
    writeByte(reg, 256);
    Wire.requestFrom(address, len);
    for(int i=0;i<len;i++){
        buff[i] = Wire.read();
    }
}
