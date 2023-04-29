cd "/home/joffin/Downloads/Mark 10 Project"
source ./venv/bin/activate

while ! bluetoothctl info | grep -q  "Connected: yes"; do
  python error_flash.py
done

python rpi_main.py
