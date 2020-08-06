Issues: tried to grab future meeting agenda item texts, but the link to the text
disappeared (from Aug 2 to Aug 3). 

Features to highlight:
Caching of bio and agenda text

Limitations:
At the last minute, I discovered my locale encoder is ascii.  It was causing 
the utils.csv_to_model to crash. The function utils.API_changed appears to work
 correctly and download the correct file from the API, but in csv_to_model,
 I read from a local and slightly older voting record.
 
Also, I didn't have time to investigate why there are duplicates in the 
councilmember database. I thought the get_or_create() function would prevent
that.  

So that I remember later:
Getting the agenda item: 
    views.agenda_text calls utils.meeting_text passing in the
    html to the calendar page (which I simply downloaded locally)
        meeting_text calls agenda_link
            agenda_link calls meeting_table
                meeting_table calls meeting_link
                    meeting_link parses the calendar table for the url
                    to the meeting which has that agenda item
                meeting_table returns the beautifulsoup object for the 
                table for that meeting
            agenda_link searches that beautifulsoup table for the url 
            the specific agenda item desired
        meeting_text grabs the text for the agenda item and sends it to 
        view.agenda_text to be displayed.
    The stuff about the agenda_id being from the future worked before 3 Aug 
    when the link to the meeting agenda was available in HTMl. After, the 
    link disappeared to the html table of future agenda items.

File structure
sliceOfDallas  
    - sliceOfDallas  
        * settings.py - included votingRecord app in Installed Apps  
        * urls.py - included votingRecord.urls   
        * wsgi.py - didn't touch  
    - votingRecord  
        - migrations  
            Files automated through makemigration  
        - static  
            style.css - styling that did not come from Bootstrap  
        - templates
            -votingRecord 
                layout.html - base layout for the web app  
                index.html - ????Something to start
        * admin.py  
        * apps.py  
        * models.py  
        * tests.py  
        * urls.py  
        * views.py  
    
Models 

AgendaItem:  
    - id: string combo of date, type, and number; make this primary key  
    - number: number on agenda
    - date: datetime.date   
    - type: string, options are Agenda or Addendum  
    - action: action taken on agenda item  
    - description: description of agenda item  
    - voter - many-to-many to Vote model
    Try: get a link to full resolution or ordinance
    
Vote:  
    - voter: ForeignKey to CouncilMember
    - agenda_item: ForeignKey to AgendaItem
    - vote_for: True or False
    
CouncilMember:
    - name: Text
    - district: Number  [comment]: <> (ToDo: make key to Districts)
    - role: Allowed values: CouncilMember, Deputy Mayor Pro Tem, Mayor, Mayor Pro Tem
    
ToDo: Districts
    
https://cityofdallas.legistar.com/MeetingDetail.aspx?ID=606245&GUID=E64BAE2E-51B2-4D45-80F1-F27C62B10B24&Options=info|&Search=
