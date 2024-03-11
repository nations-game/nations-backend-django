import os, time

while True:
    os.system("python manage.py run_tick")
    print("ticked")
    time.sleep(10)