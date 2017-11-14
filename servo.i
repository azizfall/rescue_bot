%module servo
%{
extern int fd;
extern void set_pwm(int fd,float duty_cycle,char lower_byte_addr,char higher_byte_addr);
extern void reset(int fd);
extern void exit_servo();
extern void move_servo(float duty_cycle);
extern void init_servo();

%}
extern int fd;
extern void set_pwm(int fd,float duty_cycle,char lower_byte_addr,char higher_byte_addr);
extern void reset(int fd);
extern void exit_servo();
extern void move_servo(float duty_cycle);
extern void init_servo();

