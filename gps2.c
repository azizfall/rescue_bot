//sensors

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <termios.h>
#include <errno.h>

void readBytes(int descriptor, int count);
unsigned char serialBuffer[1];
int i,j;


//output is
//GPGGA: GPS fix data
//GPGSA: GPS DOP and active satallites
//GPRMC: Recommended minimum specification GPS
//GPVTG: Track made good and ground speed

//GPS has no connection if light next to GPS is blinking once a second
//GPS has connection if light next to GPS is blinking once every ten seconds

int main() {
	int fd;
	char position[60];
	bool isType = 0;
	char *portName = "/dev/ttyS0";
	struct termios options;
	unsigned char gpsDataType[6] = {'G','P','G','G','A','\0'};

	fd = open(portName, O_RDWR | O_NOCTTY | O_SYNC);
	if (fd == -1)
	{
		perror("openPort: Unable to open port ");
	}
	tcgetattr(fd, &options);
	cfsetispeed(&options, B9600);
	cfsetospeed(&options, B9600);

	cfmakeraw(&options);

	tcflush(fd, TCIFLUSH);
	tcsetattr(fd, TCSANOW, &options);
		
//	while(1) {
	
	read(fd, serialBuffer, 1);
	if (serialBuffer[0] == '$') //new data category
	{	
		isType = true;
		for(i = 0; i < 5; i++) { //check if type is GPGGA
			read(fd, serialBuffer, 1);
			//printf("gpsData: %c\n", serialBuffer[0]); //check the input data
			//printf("gpsDataType: %s\n", gpsDataType); //check default string

			if (serialBuffer[0] != gpsDataType[i])
			{
				isType = false;
				break;
			}
		}
		
		if(isType) {
			//printf("***** Location *****\n");
			//printf("Time: ");
			read(fd, serialBuffer, 1);
			//printf("test data: %c\n", serialBuffer[0]); //ignored data
			read(fd, serialBuffer, 1);
			while(serialBuffer[0] != ',') {
				//printf("%c",serialBuffer[0]);
				read(fd, serialBuffer, 1);
			}
			//printf("\n");

			//printf("Latitude: ");
			read(fd, serialBuffer, 1);
			while(serialBuffer[0] != ',') {
				printf("%c",serialBuffer[0]);
				read(fd, serialBuffer, 1);
			}
			read(fd, serialBuffer, 1); //read N or S
			//printf(" degrees %c\n",serialBuffer[0]); //print N or S

			printf(" ");

			//printf("Longitude: ");
			read(fd,serialBuffer, 1);
			//printf("test data2: %c\n", serialBuffer[0]); //ignored data
			read(fd, serialBuffer, 1);
			while(serialBuffer[0] != ',') {
				printf("%c",serialBuffer[0]);
				read(fd, serialBuffer, 1);
			}
			read(fd, serialBuffer, 1); //read E or W
			//printf(" degrees %c\n\n",serialBuffer[0]); //print E or W
		}//if isType GPGGA --> look at data
		
	}//if looking for next data category

	

	usleep(10000);

//	}//while1

 	//fclose(f);
	fflush(stdout);
	close(fd);
	return 0;

	
}//main

void writeBytes(int descriptor, int count) {
	tcsendbreak(descriptor, 1);
	if ((write(descriptor, serialBuffer, count)) == -1) {
		perror("Error writing");
		close(descriptor);
		exit(1);
	}
}//writeBytes

void readBytes(int descriptor, int count) {
	tcflush(descriptor, TCIFLUSH);
	if(read(descriptor, serialBuffer, count) == -1) {
		perror("Error reading ");
		close(descriptor);
		exit(1);
	}

}//readBytes
	

