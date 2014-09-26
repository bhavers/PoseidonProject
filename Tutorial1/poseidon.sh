#! /bin/sh

# Startup script for PoseidonClient
# Setup instructions
# - Change the path to PoseidonClient.py below
# - Copy file to startup directory: sudo cp poseidon.sh /etc/init.d
# - Change permissions: sudo chmod 755 /etc/init.d/poseidon.sh
# - Test starting script: sudo /etc/init.d/poseidon.sh start
# - Test script running: ps -ef |grep Poseidon     (you should see 2 entries)
# - Test script logging:  tail /home/pi/PoseidonProject/Tutorial1/poseidon.log
# - Test stopping script: sudo /etc/init.d/poseidon.sh stop
# - Test script stopped: ps -ef |grep Poseidon     (entries seen above should be gone)
# - Activate script for boot: sudo update-rc.d poseidon.sh defaults
# - Test reboot: sudo shutdown -r now    (after boot, check with commands above)
# - If you every want to remove autoboot:  sudo update-rc.d -f  poseidon.sh remove 



case "$1" in
  start)
    echo "Starting PoseidonClient"
    # run 
    sleep 10
    cd /home/pi/PoseidonProject/Tutorial1/
    sudo python PoseidonClient.py &
    ;;
  stop)
    echo "Stopping all python processes, including PoseidonClient"
    # Kill process should be made specific for PoseidonClient instance
    killall python
    ;;
  *)
    echo "Usage: /etc/init.d/poseidon {start|stop}"
    exit 1
    ;;
esac
