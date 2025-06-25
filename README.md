# **My first ever Python Program :DD**

This program takes in a WhatsApp text file and generates an image of a summary of its content

![UI](https://github.com/THXatGIT/Whatsapp-Recap/blob/Work-in-progress/Just%20for%20show%202.png)

# **Content includes:**

-Pie and Bar chart of total messages sent (in a time range) by each person

-Pie and bar chart of total length of messages sent (in a time range) by each person

-Total messages sent per month

-Total messages sent per hour (e.g 00 for 12AM, 20 for 8AM, etc)

-Total messages sent per day of week (e.g Friday)

-Top 5 longest messages, a short snippet of it, length of message, who sent it, at what time and date,

-Word cloud of top 100 used words and a bar graph of top ten used words.

# $${\color{#00ff00}NEW}$$
- The recap is now even more oragnised with more features

- Added better filters
  
- Tapping the overall recap button now resets the settings without the need to press the save settings

- Added Year count graph

- Add Day count graph

- Added Top longest words and Lexicon Count*
  
- Added Bar Chart for top 10 most used emojis

- Sentiment Analysis Function

- Summarisation function**

** Summarisation is a different button and is not included in summary image.

# **Filters:**

By Overall

By previous Year, Month, day

By Year, by Month by Day or by Hour

By date range

# **Instructions:**
1. Go to WhatsApp 
2. Click the three dots at the top left of your selected WhatsApp chat group
3. Click 'More' > 'Export Chat'
4. Download the text file into the computer
4. Go to this app
5. Press 'Select WhatsApp Text File' and select a WhatsApp text file
6. Press 'Recap WhatsApp'
7. Wait 3s
8. Now your WhatsApp Recap is ready! 
9. Press 'Preview Image' to see the recap
10. Press 'Save Recap' to save the recap into the computer if you like it :D

Additional Settings:
There are 4 different setting:
Name, Overall, Previous and Custom

Name
Select who you want to recap after selecting the text file

Overall
Recaps the whole text file. (Default)

Previous
Recaps previous
Year, Month or day

Custom
Recaps any custom date and date range
If ONLY Year or Month or day or hour is selected, that is what is recapped

If Two catergories are selected, 
For year and month, it just works like you think
For year and day/hour, It recaps the range of days/hours selected between the years
For month and day/hour, It recaps the range of days/hours selected between the months
For day and hour, it recaps the range of hours selected within the days

If Three Catergories are selected,
For Year, Month and Day, it works like you think
For Year, Month and Hour, It recaps the range of hours selected between the year and months
For Year, Day and Hour, I can't be bothered, this is beyond useless
For Month, Day and Hour, It recaps all the month, days and hours ranges given across all available 
Whatsapp Years.

If all are selected, it works like you think.

Less recent dates at the top, more recent dates at the bottom
Ensure both catergories are filled if the range functions are selected.

# **Bugs log**
1. Chats which are too long would be unable to generate sentiment analysis.
2. Program will stop if nothing happens on that day.
3. Top longest words and lexicon count does not work for languages which are not separated by space*
4. Summarisation only works for English

Note: This should work for both android and IOS files

Refer to the NOAI branch for a lightweight version without AI 
https://github.com/THXatGIT/Whatsapp-Recap/tree/NOAI
