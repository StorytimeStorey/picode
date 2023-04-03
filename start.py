import subprocess



#This will run all the scripts that we need to run at the same time
#The bot, the data collector, eventually the alerts checker and maybe the processes for running the relays
subprocess.Popen(['python', 'data/start_data.py'])
subprocess.Popen(['python', 'bot/Bonnibel.py'])
subprocess.Popen(['python', 'bot_2/McJohnson.py'])