# picode


Here we will set out implentation plans and major updates.
If there are any major changes, please put explanations and date/time here


## Known errors:

- Last data taken at 9.0. <- should say 0009 (12:09 am). reads as 0009 in the text file, so its an error in the comprehension
- Graphs x axis isn't showing proper times
    - Intended to show in 30 minute increments + last time taken. 
    - Current rendition somehow offsets time with the graph weirdly
    - Current rendition doesn't show the proper times.
    
## Fixed Errors
- ~data in graph will not reset between calls from the bot~ 4/4/23 Had to do plt.close(). Was actually kind of a big memory leak.
- ~Currently stuck in test mode~ fixed 4/3 @ 10am.
- ~slash command for graph not working, regular command is working~
- ~csv randomly got deleted? Can't figure out why. 3/30 @ 11pm~ I think we were both interacting at the same time and didn't notice
- ~@tree isn't working currently~~
- ~directory won't be accessed sometimes~ This is an issue with permissions. Currently fixed by with using sudo python3 start.py

## Most Important:
- We should focus on the following in this order:
    - Control
    - Relays
        - Safety Measures
    - Alerts (will work with function to control relay on/off states)
        - Alerts CSV
        - bot tasks.loop
    - Testing
    - Graphing

## Control:
- Read from Raw
- Check values against chosen lows and high
- control relay signals
- Pass to Alerts
    - To be passed: temp, low, relay_status


## Alerts:
- will read from raw
    - temp, hum, relay_status
    - will be in charge of handling relay_status timekeeping
    - if an element is on too long, send alarm
    - might be good at have emergency on/off operable from bot
- will work as part of main control script (imported)
- alerts will save to csv
- bot will tasks.loop: check the csv for updates
- bot will be able to access alert history csv
- triggered alert will create graph of temp/hum of the day
    - graph to show temp, hum, and on/off states of systems for that day


## Bot:
- get tasks.loop to work for alerts
- clean up names and function names
- remove Bonnibel and standardize Johnson conventions
- **CREATE DOCUMENTATION FOR INTENTS AND PROCESS TO CREATE BOT NECESSARY TO WORK WITH THIS PROGRAM**
- implement graph responses, allowing for more time options on request. 
    - may tie into advanced alerts requests
- have status update with last line of dot.csv

### Graph:
- Show time in X axis in 30-min intervals, including last time
- Request "graph" for most current day
- request "graph X"    
    - X days, weeks, months, years desired               
- temp/hum
- fix x axis issues
- fix weird graph scaling problem from latest x axis fuckery


## Saved Data
- Data saves to an external folder on the pi. This folder needs to be created if running for the first time.
- current save convention is dd/mm/yy_dot.csv. dot stands for "data over time." This convention is under construction.
- Raw data, which is replaced every 5 minutes, is saved to data/csv inside the picode directory. 
    - Any test data is also saved here, when running off-pi.


## data_rec_final:
- ~~Each CSV should eventually be seperated by days and saved with a naming convention easy to find.~~ finished 3/30, each daily csv named DD_MM_YY_dot.csv
- ~~Need to reset the data list after each run. ~~  finished 3/30, line 35 in data_rec_final.py. 
- Sometimes return weird times, remove instances of XXX9 and XXX4 from timestamp

# TO BE CONSIDERED:
- code for tiggering camera
   - have save to specific directory
   - Be able to tell bot when certain run is finished
   - have it generate a gif automatically
   - have it remove the photos and save it to a different directory
- more advanced graphing

    




