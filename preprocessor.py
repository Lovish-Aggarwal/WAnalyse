import re
import pandas as pd

# Extract the Date time
def date_time(s):
    pattern='^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result=re.match(pattern, s)
    if result:
        return True
    return False 

# Extract contacts
def find_contact(s):
    s=s.split(":")
    if len(s)==2:
        return True
    else:
        return False
    
# Extract Message
def getMassage(line):
    splitline=line.split(' - ')
    datetime= splitline[0];
    date, time= datetime.split(', ')
    message=" ".join(splitline[1:])
    
    if find_contact(message):
        splitmessage=message.split(": ")
        author=splitmessage[0]
        message=splitmessage[1]
    else:
        author=None
    return date, time, author, message

def preprocess(fp):
    data=[]
    messageBuffer=[]
    date, time, author= None, None, None
    # print(type(fp))
    fp=fp.splitlines( )
    for line in fp:
        line=line.strip()
        if date_time(line):
            if len(messageBuffer) >0:
                data.append([date, time, author, ''.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message=getMassage(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

    df=pd.DataFrame(data, columns=["date", "Time", "user", "message"])
    # df.drop(df[(df['message']=='<Media omitted>')].index, inplace=True)
    df['date']=pd.to_datetime(df['date'],format='%d/%m/%y')
    # Extracting Years moths days from date 
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['month_num']=df['date'].dt.month
    df['day_name']=df['date'].dt.day_name()
    df['date']=df['date'].dt.date  
    dataFrame=df.dropna()
    return dataFrame