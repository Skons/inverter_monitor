/usr/bin/perl /home/pi/inverter_monitor/inverter.pl /dev/ttyUSB0 > /home/pi/inverter_monitor/logs/current.txt
cat /home/pi/inverter_monitor/logs/current.txt >> /home/pi/inverter_monitor/logs/`date +%Y%m%d`-output.txt
