/usr/bin/perl /home/pi/inverter_monitor/inverter.pl /dev/ttyUSB0 > /home/pi/inverter_monitor/logs/current.txt
cat /home/pi/inverter_monitor/logs/current.txt >> /home/pi/inverter_monitor/logs/`date +%d%m%Y`-output.txt
