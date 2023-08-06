#! /bin/sh
sudo cat <<EOF >/etc/init.d/piforgeStart
#! /bin/sh
#/etc/init.d/piforgeStart
### BEGIN INIT INFO
# Provides: piforgeStart
# Required-Start: \$remote_fs \$syslog
# Required-Stop: \$remote_fs \$syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: start a program from boot
# Description: A simple script  which will start a program from boot and stop upon shut-down
### END INIT INFO
 
# Put any commands you always want to run here.
sudo piforge
EOF
sudo chmod +x /etc/init.d/piforgeStart
sudo update-rc.d piforgeStart defaults
