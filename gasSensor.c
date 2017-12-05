//sensors

#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define GAS_SENSOR_ADDRESS 0x48

int main()
{
	//while(1) {
		//printf("****Gas Sensor Testing****\n");
		int fd, i;
		char *fileName = "/dev/i2c-1";
		int address = GAS_SENSOR_ADDRESS;
		unsigned char buf[10];

		if ((fd = open(fileName, O_RDWR)) < 0) {
			printf("Failed to open i2c port\n");
			exit(1);
		}

		if(ioctl(fd, I2C_SLAVE, address) < 0) {
			printf("Unable to get bus access to talk to slave\n");
			exit(1);
		}

		usleep(900000);

		buf[0] = 0;

		if((write(fd, buf, 1)) != 1) {
			printf("Error writing to i2c slave\n");
			exit(1);
		}

		if((read(fd, buf, 2)) != 2) {
			printf("Error reading from i2c slave\n");
			exit(1);
		}

		else {
			unsigned char highByte = buf[0];
			unsigned char lowByte = buf[1];
			//unsigned char lowerByte = buf[2];
			//unsigned int gasLevel = (highByte<<16) + (lowByte<<8) + lowerByte;
			unsigned int gasLevel = (highByte<<8) + lowByte;

			printf("%u", gasLevel);
		}


	//}//while
	return 0;

}//main
