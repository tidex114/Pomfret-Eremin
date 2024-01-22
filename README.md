# Pomfret-Eremin
**This is my worklog!****

_Week 1:_
- **Transfered to registration by ID from the table in gspread**
  To login as a student or a faculty member, user should type in only the ID he was given. All the info such as first and last name, gmail and graduation year are stored in a gspread table and is taken from there.
  
-  **Started working on Canvas notifications.**
  To have it done, I need user's secret API key which can be generated from user's account (or I suppose can be generated from organisation's admin's account). For now, I've done a part of the
  frontend - user gets a message that notifications were enabled when he presses the button.
- **Currently planning to make a poll about usage of Discord among the school community.**
    Are Canvas's notifications are good/convinient enough?
    Are Google services convinient to use in different apps?
    Would it be better if all of above were in one app?

    In other words, I'm making a poll which will show how my product wiil be used and will it be used at all?
  
**TOTAL HOURS: 8**

_Week 2:_
- **Created and conducted the Discord Poll**
  In total got 47 responses, inlcuding both faculty and students.
  - Almost half (22 - 46.8%) of the survey respondents answered that they do not use Discord. Among those who use it (25 - 53.2%), almost half (21 - 44.7%) use      Discord exclusively for gaming, 18 people (38.3%) for communication, and 4 for various purposes (8.4%).
  -   Overall, the school community assesses the benefit of Discord for its cohesion on a five-point scale at 3.
  -   The majority of respondents (41 - 87.2%) believe that the sign-up system can be improved by adding live statistics and automating the entire process.
- **Created proposal to the tech office**
- **Added live stats to the sign-up system**
  -   Now, the sign-up message shows current count of participants and room left. Count updates by editing message on button.interaction (when user presses the button)
  -   All the sign-ups are now stored in a google sheet "trip list". It's needed due to discordpy not saving any info about what has been done during the running proccess. During the bot's initialisation all Views (buttons pinned to messages) are added to the queue and info about trips is being loaded to each sign-up message. Also, the current count is stored and updated in the google sheet

**TOTAL HOURS: 5**


_Week 3:_
- **Strated working on message filtering system**
  Filters done and working: 
  - _Profanity filter._ Detects profanity using ML profanity_check library. Not accurate with caveats and other forms of offensive language, but still better than just a list of bad words.
  Filters in progress:
  -   _Link filter._ No links are allowed in public chats on the server
  -   _Image scanner._ Have not started working on it yet, but probably will use some sort of existing AI to check safety of the picture sent.
    
- **Created Guide Lines list**
  - Decorated and sent the Guide Lines message to the #rules channel. The result can be seen there.
  - Changed RULES_MESSAGE_ID in the config.py, so the rules acknowledgment works with another message
  - The first easter egg was created. **Go find it!**
    
- **Starting working on violations/punishment system**
  - /_mute_ - mutes user for customizable period of time
  - /_ban_ - kickbans user from the server
  - /_warns_ - gives a warning to the user. If 3 accumulated, user gets muted or kickbanned.
  - **All of above can be used only by authorized faculty and/or server moderators ONLY if user has violated server's guidelines**

**TOTAL HOURS: 4**
