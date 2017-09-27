#include "Particle.h"

//Command register
#define TCS3472_COMMAND_REG 0x80

//Enable register
#define TCS3472_ENABLE_REG 0x00

#define TCS3472_ENABLE_INT 0xA0
#define TCS3472_ENABLE_WAIT 0x08
#define TCS3472_ENABLE_RGBC 0x02
#define TCS3472_ENABLE_POWER 0x01


//Integration timing register, integration time works in 2.4ms increments STARTING at 0xF6, i.e. writing a  will set the integration time to 24ms
#define TCS3472_TIMING_REG 0x01

//Wait time register, also works in 2.4ms increments exactly as above, unless the WLONG flag is set, in which case the time is 12x longer
#define TCS3472_WAIT_REG 0x03


//Configuration register, only used for the WLONG flag
#define TCS3472_CONFIG_REG 0x0D
#define TCS3472_WLONG 0x02


//Control register, used for setting gain
#define TCS3472_CONTROL_REG 0x0F

#define TCS3472_AGAIN_1 0x00
#define TCS3472_AGAIN_4 0x01
#define TCS3472_AGAIN_16 0x02
#define TCS3472_AGAIN_60 0x03


//Status register
#define TCS3472_STATUS_REG 0x13

//integration cycles have completed
#define TCS3472_AVALID 0x01


#define TCS3472_DATA_REGISTER_0 0x14


class TCS3472{
public:
    void init();
    void loop();
    void takeReadings();
    void toRGB();
    
    int address = 0x29;
    
    int loop_delay = 0;
    
    int wait_en = TCS3472_ENABLE_WAIT;
    bool wlong = false;
    
    int wtime = 0x00;
    int timing = 0x00;
    
    int gain = TCS3472_AGAIN_1;
    
    int red;
    int green;
    int blue;
    int clear;
    
    String rgb;
private:
    int last_checked;
    
    void sendCommand(int reg, int data);
    
    void begin();
    int readRate();
    void writeByte(int reg, int data);
    void readBuffer(int reg, int *data, int length);
    int readByte(int reg);
};
