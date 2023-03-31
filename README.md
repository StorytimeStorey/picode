# picode


Here we will set out implentation plans and major updates.
If there are any major changes, please put explanations and date/time here

Personal writing style:
I don't like a ton of nesting. It's ugly and difficult to follow. If possible, please write anything that can be a function into one. 
For an example, look at the data_rec_final file. You'll see I don't go past 4 tabs. If i go beyond that, I should probably be making a function.
Obviously this doesn't always work, but it makes for clean running code that is easier to work on, as the specific funtion that throws an error is easier to work on this way.

Known errors:
    csv randomly got deleted? Can't figure out why. 3/30 @ 11pm
    @tasks not working --don't really want alerts working through tasks anyways
    @tree isn't working currently

Bot:
    change to class form
    get slash commands working
        Graph:
            slash commands for graph time desired
                X days, weeks, months, years desired
            slash commands for type of graph desired
                temp/hum
        Alerts:
            pipe to look for alerts from the alerts function
            move alerts to data and have it work while writing to raw
            see Alerts section for more

Alerts:
    test if current rendition works
    pipe to bot to alert server when outside of range
        test server alerts
    Get it to work while writing to raw 
    Saving
        Make sure alerts are saving to file
        Be able to access history easily through bot
        integrate with graphs to see error history

Saved Data
    ~~Move data saved to a specific place in the pi so it doesn't get deleted on resetting code.~~ 3/30 all data beyond raw now saved to root/data, or just data/(name).csv
        considering removing the ending _dot and just placing it in a directory named dot. 
            ERROR:
                Last data taken at 9.0. <- should say 0009 (12:09 am). reads as 0009 in the text file, so its an error in the comprehension
        --only useful if we agree we are finished with changing naming conventions.

    

TO BE MADE:
    code for triggering on/off states for relays
        check if on/off
        make alert for "on for too long"
        make electrical plans, include safety contingencies (fuses are easiest)
            3 5v -> 120V AC relays (I think I have enough)
            possibly transistors to account for amp needs
            fuses to ensure amps aren't above safety specs
            who knows what else lol

    code for tiggering camera
        have save to specific directory
        Be able to tell bot when certain run is finished
        have it generate a gif automatically
        have it remove the photos and save it to a different directory

    


data_rec_final:
~~Each CSV should eventually be seperated by days and saved with a naming convention easy to find.~~ finished 3/30, each daily csv named DD_MM_YY_dot.csv
~~Need to reset the data list after each run. ~~  finished 3/30, line 35 in data_rec_final.py. 
Sometimes return weird times, remove instances of XXX9 and XXX4 from timestamp

