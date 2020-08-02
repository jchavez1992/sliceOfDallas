modules to install:
pypdf2
pdfminer



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
