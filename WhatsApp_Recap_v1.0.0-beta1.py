# The recap is now more oragnised with more features
# Added Instructions
# Added filters
#bug1 floating numbers in bar graph with small values
#bug2 repeated long message not counted
import os
import sys
from random import randint
import textwrap as tw
import numpy as np
import matplotlib.pyplot as plt 
import wordcloud as wc
from PIL import Image,ImageDraw,ImageFont,ImageTk
import tkinter as tk
from tkinter import filedialog
import ctypes
import datetime
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# init tk page
root=tk.Tk()
# get images
mascots=[ImageTk.PhotoImage(Image.open(resource_path(f"mascot/Whatsapp Recap Mascot{i}.png")).resize((90,78))) for i in range(1,6)]
root.wm_iconphoto(False, mascots[0])
root.title('WhatsApp Recap v1.0.0-beta1')
root.geometry('960x600')
txtfile=''
filename=''
complete=''
bg=''
group=''
recapyear=tk.StringVar()
recapmonth=tk.StringVar()
recapday=tk.StringVar()
recaphour=tk.StringVar()
# recapyear.set(str(datetime.date.today().year))
recapyear.set("All")
recapmonth.set("All")
recapday.set("All")
recaphour.set("All")
listofyears=[str(i) for i in range(2009,datetime.date.today().year+1)]
listofdays=["0"+str(i) for i in range(1,10)]+[str(i) for i in range(10,32)]
listofhour=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
canvafont=resource_path("CanvaSans-Bold.otf")
kaiti=resource_path("C:\Windows\Fonts\STKaiti.ttf")
arial=resource_path("C:/Windows/Fonts/arial.ttf")
# #main code below
def recapfunc():
    global txtfile,complete,bg,group,recapyear,recapmonth,recapday,recaphour,listofyears,listofhour,listofdays
    # txtfile='WhatsApp Chat with 22_1.txt'
    plt.rcParams['font.family']=['STKaiti']
    year=[]
    month=[]
    date=[]
    dateofweek=[]
    hr=[]
    min=[]
    user=[]
    message=[]
    # filters
    yearfilter1=monthfilter1=dayfilter1=hourfilter1=None
    if recapyear.get()=="All":
        yearfilter1=listofyears
    else:
        yearfilter1=recapyear.get()
    if recapday.get()=="All":
        dayfilter1=listofdays
    else:
        dayfilter1=recapday.get()
    # group=txtfile.replace('WhatsApp Chat with ','').replace('.txt','')
    group=txtfile[-txtfile[::-1].index('/'):].replace('WhatsApp Chat with ','').replace('.txt','')
    monthname={'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
    timename=['12AM','1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']
    datename=['Monday','Tuesday','Wednesday',"Thursday","Friday","Saturday","Sunday"]
    timedict={j:i for i,j in zip(listofhour,timename)}
    if recapmonth.get()=="All":
        monthfilter1=monthname.keys()
    else:
        monthfilter1=list(monthname.keys())[list(monthname.values()).index(recapmonth.get())]
    if recaphour.get()=="All":
        hourfilter1=listofhour
    else:
        hourfilter1=timedict[recaphour.get()]
    with open(txtfile, 'r',encoding='utf-8') as chats:
        prevchat=None
        filth=None
        for chat in chats.readlines():
            try:
                if chat[2 and 5] == '/':
                    if chat[6:10] in yearfilter1 and chat[3:5] in monthfilter1 and chat[:2] in dayfilter1 and chat[12:14] in hourfilter1:
                        user.append(chat[20:chat.index(':',20)])
                        year.append(chat[6:10])
                        month.append(chat[3:5])
                        date.append(chat[:2])
                        dateofweek.append(datetime.datetime(int(chat[6:10]),int(chat[3:5]),int(chat[:2])).strftime("%A"))
                        hr.append(chat[12:14])
                        min.append(chat[15:17])
                        if ' This message was deleted\n' in chat or ' <Media omitted>\n' in chat or ' <Media omitted>\n' ' POLL:\n'in chat:
                            # TAKE NOTE
                            message.append(' ')
                        else:
                            message.append(chat[chat.index(':',20)+2:])
                    prevchat=chat
                    filth=prevchat[6:10] in yearfilter1 and prevchat[3:5] in monthfilter1 and prevchat[:2] in dayfilter1 and prevchat[12:14] in hourfilter1
                elif filth:
                    message[-1]+=chat
            except IndexError: 
                if len(message)>0 and filth:
                    message[-1]+=chat
            except ValueError:
                continue
        chats.close()
    msglen=[len(i)-1 for i in message]

    #Longest messages
    longmsg=[message[msglen.index(i)] for i in sorted(msglen,reverse=True)[0:5]]
    tuples=[(date[msglen.index(i)],monthname[month[msglen.index(i)]],year[msglen.index(i)],user[msglen.index(i)],hr[msglen.index(i)],min[msglen.index(i)],len(message[msglen.index(i)])) for i in sorted(msglen,reverse=True)[0:5]]
    toplen={i:j for i,j in zip(longmsg,tuples)}
    # BUG! REPEATED LONG MESSAGES AREN'T COUNTED
    def piebar(title, piedata,bardatax,bardatay,xlabel,ylabel):
        global group
        plt.rcParams.update({'font.size': 15})
        fig,(pie,bar)=plt.subplots(1,2,figsize=(20,10))
        fig.suptitle(group+' '+title)
        pie.pie(piedata, autopct='%1.1f%%',pctdistance=1.1,startangle=90,counterclock=False)
        # pie.legend(labels=dic.keys(),loc='lower left',bbox_to_anchor=(-0.2,0))
        bar.barh(list(bardatax)[::-1],list(bardatay)[::-1],color=(15/255,208/255,17/255))
        for index, value in enumerate(list(bardatay)[::-1]):
            bar.text(value, index, str(value),va='center')
        bar.set_xlabel(xlabel)
        bar.set_ylabel(ylabel)
        fig.canvas.draw()
        return Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))
    # User Chat count
    chatdic={}
    for i in user:
        if i in chatdic:
            chatdic[i]+=1
        else:
            chatdic[i]=1
    chatdic=dict(sorted(chatdic.items(), key=lambda item: item[1],reverse=True))
    chatsperuser=piebar('Chats per user',chatdic.values(),chatdic.keys(),chatdic.values(),'Total Chats','User')

    # Length stuff
    plt.clf()
    lendic={}
    sum=0
    for id, person in enumerate(user):
        if person in lendic:
            lendic[person]+=msglen[id]
        else:
            lendic[person]=msglen[id]
    lendic=dict(sorted(lendic.items(), key=lambda item: item[1],reverse=True))
    locchatsperuser=piebar('Length of Chats per user',lendic.values(),lendic.keys(),lendic.values(),'Total Length of Chats','User')
    
    def bargraph(xdata,ydata,title,xlabel,ylabel):
        fig,ax=plt.subplots(figsize=(10,5))
        for index, value in enumerate(ydata):
            plt.text(index,value+1,str(value),ha='center')
        ax.bar(xdata,ydata,color=(15/255,208/255,17/255))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        fig.canvas.draw()
        return Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))
    
    # Messages per time (hr)
    lst=[]
    for i in listofhour:
        lst.append(hr.count(i))
    hfh=timename[lst.index(max(lst))]
    messagepertime=bargraph(listofhour,lst,"Total messages per time (hr)",'Time of message (hr)',"Messages")

    #messages per month
    lst.clear()
    for i in monthname.keys():
        lst.append(month.count(i))
    hfm=list(monthname.values())[lst.index(max(lst))]
    messagepermonth=bargraph(monthname.keys(),lst,"Messages per month",'Month',"Messages")

    #wordcloud
    wordlist=[]
    wordfreq={}
    for i in message:
        for j in i.lower().split():
            wordlist.append(j)
    for i in wordlist:
        if i in wordfreq and i not in wc.STOPWORDS:
            wordfreq[i]+=1
        else:
            wordfreq[i]=1
    wordfreq=dict(sorted(wordfreq.items(), key=lambda item: item[1],reverse=True))
    while len(wordfreq)>10:
        wordfreq.popitem()
    #can deal with two different languages (Chinese and English Only) but FoNt bE WoNk
    wordcloud=wc.WordCloud(font_path=kaiti,width=800, height=400,background_color='white',max_words=100,color_func=lambda *args, **kwargs: (15,208,17)).generate((" ").join(message))
    plt.clf()
    fig,(wcld,bar)=plt.subplots(1,2,figsize=(20,10))
    fig.suptitle(group+' WordCloud')
    wcld.imshow(wordcloud)
    wcld.axis("off")
    bar.barh(list(wordfreq.keys())[::-1],list(wordfreq.values())[::-1],color=(15/255,208/255,17/255))
    for index, value in enumerate(list(wordfreq.values())[::-1]):
        bar.text(value, index, str(value),va='center')
    bar.set_xlabel('Word frequency')
    bar.set_ylabel('Word')
    fig.canvas.draw()
    wc1=Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))

    # I need better organisation skill
    lst.clear()
    for i in datename:
        lst.append(dateofweek.count(i))
    hfd=datename[lst.index(max(lst))]
    messageperdow=bargraph(datename,lst,"Messages per Day of Week",'Day of Week',"Messages")

    #PIL stuff
    recapimg=Image.new("RGB",(1588,2245*2))
    bg=Image.open(resource_path("background.png")).resize((1588,2245))
    Image.Image.paste(recapimg,bg)
    Image.Image.paste(recapimg,bg,(0,2245))
    rcap=ImageDraw.Draw(recapimg)
    # Chinese text and length giving me problems :/
    def drawtext (pos,text,size,align="left"):
        global bg
        bfont=ImageFont.truetype(canvafont,150)
        sfont=ImageFont.truetype(canvafont,50)
        cfont=ImageFont.truetype(kaiti,50)
        msgfont=ImageFont.truetype(arial,40)
        cmsgfont=ImageFont.truetype(resource_path('C:\Windows\Fonts\msyhl.ttc'),30)
        timefont=ImageFont.truetype(arial,20)
        ctimefont=ImageFont.truetype(kaiti,20)
        w,h=pos
        if size=='big':
            _,_,w1,_=rcap.textbbox((0,0),text,font=bfont,align=align)
            rcap.text(((1588-w1)/2+w,h), text, fill=(15,208,17), font=bfont,stroke_width=10, stroke_fill='white',align=align)
        elif size=='small' and text.isascii():
            _,_,w1,_=rcap.textbbox((0,0),text,font=sfont,align=align)
            rcap.text(((1588-w1)/2+w,h), text, fill=(15,208,17), font=sfont,stroke_width=3, stroke_fill='white',align=align)
        elif size=='msg':
            if text.isascii():
                rcap.text((w,h), text,fill='black', font=msgfont,align=align)
            else:
                rcap.text((w,h), text,fill='black', font=cmsgfont,align=align)
        elif size=='time':
            rcap.text((w,h), text,fill='grey', font=timefont,align=align)
        elif size=='name':
            colours=["red","lawngreen","green","cyan","blue","purple","brown"]
            if text.isascii():
                rcap.text((w,h), text,fill=colours[randint(0,6)], font=timefont,align=align)
            else:
                rcap.text((w,h), text,fill=colours[randint(0,6)], font=ctimefont,align=align)
        else:
            _,_,w1,_=rcap.textbbox((0,0),text,font=sfont,align=align)
            rcap.text(((1588-w1)/2+w,h), text, fill=(15,208,17), font=cfont,stroke_width=3, stroke_fill='white',align=align)
    def drawline(ypos):
        rcap.line((0,ypos,1588,ypos),width=4,fill=(15,208,17))
    drawtext((0,0),"Whatsapp Rewind",'big')
    drawtext((0,200),f"{group} has a total of",'small')
    drawtext((0,250),f"{len(message)}",'big')
    drawtext((0,425),"overall conversations!",'small')
    drawline(497)
    drawtext((600,500),f"{list(chatdic)[0]} \nSent most of \nthe messages",'small',"center")
    recapimg.paste(chatsperuser.resize((1200,600)),(0,500))
    recapimg.paste(locchatsperuser.resize((1200,600)),(0,1100))
    drawtext((600,1105),f"{list(lendic)[0]} \n Had the MOST \nto talk about",'small',"center")
    drawtext((0,1710),"Here are the TOP 5 LONGEST messages",'small','center')
    for msg,data in zip(toplen.keys(),toplen.values()):
        num=list(toplen.keys()).index(msg)
        d,m,y,n,h,mins,l=data
        rcap.rounded_rectangle((50,1790+160*num,1588/2,1940+160*num),fill=(217,253,211),radius=10)
        if msg.isascii():
            drawtext((75,1810+160*num),tw.fill(msg,width=32,max_lines=3,placeholder='...'),'msg')
        else:
            drawtext((75,1810+160*num),tw.fill(msg,width=18,max_lines=3,placeholder='...'),'msg')
        drawtext((1588/4,1810+165*num),f'{d} {m} {y}, {l} characters','small','center')
        drawtext((75,1790+160*num),f"~{n}",'name','center')
        drawtext((1588/2-55,1915+160*num),f'{h}:{mins}','time','center')
    drawline(2585)
    #section1
    drawtext((0,2580),"Some of you would have most likely been caught chatting...",'small')
    drawtext((-400,2655),f"in {hfm}",'small')
    drawtext((400,2655),f"at {hfh}",'small')
    recapimg.paste(messagepermonth.resize((800,400)),(0,2730))
    recapimg.paste(messagepertime.resize((800,400)),(800,2730))
    drawtext((0,3140),f"on {hfd}",'small')
    recapimg.paste(messageperdow.resize((800,400)),(400,3235))
    drawline(3640)
    #section2
    drawtext((500,3640),"And... \nto end it off, here's a \nwordcloud of all the \nconversations","small","center")
    recapimg.paste(wc1.resize((1000,500)),(0,3645))
    bg=recapimg
    # tkinter stuff
    if complete == '':
        complete=tk.Label(root,text=f'Recap of {group} Complete!',font=(canvafont,17),fg='#0fd012')
        complete.grid(row=5,column=0)
        tk.Button(root,text="Preview Image",image=mascots[3],font=(canvafont,17),fg='#0fd012',bg='light green',compound=tk.LEFT,command=imgshow).grid(row=6,column=0)
        tk.Button(root,text="Save Recap",image=mascots[4],font=(canvafont,17),fg='#0fd012',bg='light green',compound=tk.LEFT,command=saverecap).grid(row=7,column=0)
    else:
        complete.config(text=f'Recap of {group} Complete!')
#tkinter window
def selectxt():
    global txtfile, filename
    if txtfile =='':
        txtfile=filedialog.askopenfilename(initialdir="C:/",title='Select WhatsApp Text File',filetypes=(("Text Files",'*.txt'),))
        filename=tk.Label(root,text=txtfile[-txtfile[::-1].index('/'):] +'\nhas been selected',font=(canvafont,17),fg='#0fd012')
        filename.grid(row=3,column=0)
        tk.Button(root,text='Recap Whatsapp',image=mascots[1],font=(canvafont,17),fg='#0fd012',bg='light green',compound=tk.LEFT,command=recapfunc).grid(row=4,column=0)
        return txtfile
    else:
        txtfile=filedialog.askopenfilename(initialdir="C:/",title='Select WhatsApp Text File',filetypes=(("Text Files",'*.txt'),))
        filename.config(text=txtfile[-txtfile[::-1].index('/'):] +'\nhas been selected')
def imgshow():
    global bg
    bg.show()
def saverecap():
    global bg
    bg.save(f"{group} Whatsapp Recap.png")
Title=tk.Label(root,text="Whatsapp Recap",font=(canvafont,50), fg='#0fd012').grid(row=0,column=0)
mascot1=tk.Label(root,image=mascots[0]).grid(row=1,column=0)
select= tk.Button(root,text='Select WhatsApp Text File',font=(canvafont,17),fg='#0fd012',bg='light green',image=mascots[2],compound=tk.LEFT,command=selectxt)
select.grid(row=2,column=0)
Instructions_heading=tk.Label(root,text='Instructions',font=(canvafont,18),fg='#0fd012')
Instructions= tk.Label(root,text="""
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
10. Press 'Save Recap' to save the recap into the computer if you like it :D"""
,justify='left',font=(canvafont,18),fg='#0fd012')
Instructionsshowing=False
def showinstructions():
    global Instructions_heading, Instructions,Instructionsshowing
    if not Instructionsshowing:
        Instructions_heading.grid(row=8,column=1,columnspan=4)
        Instructions.grid(row=9,column=1,columnspan=4)
        Instructionsshowing=True
    else:
        Instructions_heading.grid_remove()
        Instructions.grid_remove()
        Instructionsshowing=False
Instructbutton=tk.Button(root,text='Show Instructions',command=showinstructions).grid(row=7,column=1,columnspan=4)
#filter
prevfilter=tk.StringVar()
recapfilter=tk.IntVar()
recapfilter.set(1)
prev=["Overall","Year","Month","Day"]
prevfilter.set(prev[0])
def overall():
    global recapday,recapyear,recapmonth,recaphour,recapfilter,listofdays
    recaps=[recapyear,recapmonth,recapday,recaphour]
    if recapfilter.get()==1:
        for r in recaps:
            r.set("All")
        prevfilter.set("Overall")
    if recapfilter.get()==2:
        if prevfilter.get()=="Overall":
            for r in recaps:
                r.set("All")
        elif prevfilter.get()=="Year":
            recapyear.set(str(datetime.date.today().year-1))
            for r in recaps[1:]:
                r.set("All")
        elif prevfilter.get()=="Month":
            lastmonth=datetime.date.today().replace(day=1)-datetime.timedelta(days=1)
            recapyear.set(lastmonth.strftime('%Y'))
            recapmonth.set(lastmonth.strftime('%B'))
            for r in recaps[2:]:
                r.set("All")
        elif prevfilter.get()=="Day":
            lastday=datetime.date.today()-datetime.timedelta(days=1)
            recapyear.set(lastday.strftime('%Y'))
            recapmonth.set(lastday.strftime('%B'))
            recapday.set(lastday.strftime('%d'))
            recaphour.set("All")
for i in range (1,5):
    root.columnconfigure(i,minsize=100)
advancedoptionshowing=False
defautoption=tk.Radiobutton(root,text="Overall Recap (Default)",variable=recapfilter,value=1)
previousoption=tk.Radiobutton(root,text="Recap Previous",variable=recapfilter,value=2)
customoption=tk.Radiobutton(root,text="Custom Recap",variable=recapfilter,value=3)
previousfilter=tk.OptionMenu(root,prevfilter,*prev)
years=["All"]+listofyears
months=["All","January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November","December"]
days=["All"]+listofdays
hours=["All",'12AM','1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']
year_header=tk.Label(root,text="Year")
month_header=tk.Label(root,text="Month")
day_header=tk.Label(root,text="Day")
hour_header=tk.Label(root,text="Hour")
yearfilter=tk.OptionMenu(root,recapyear,*years)
monthfilter=tk.OptionMenu(root,recapmonth,*months)
dayfilter=tk.OptionMenu(root,recapday,*days)
hourfilter=tk.OptionMenu(root,recaphour,*hours)
savesettings=tk.Button(root,text='Save Settings',command=overall)
def advanced():
    global customoption,defautoption,advancedoptionshowing
    if not advancedoptionshowing:
        defautoption.grid(row=1,column=1,columnspan=4)
        previousoption.grid(row=2,column=2,sticky="E")
        previousfilter.grid(row=2,column=3,sticky="W")
        customoption.grid(row=3,column=1,columnspan=4)
        year_header.grid(row=4,column=1,pady=10)
        month_header.grid(row=4,column=2,pady=10)
        day_header.grid(row=4,column=3,pady=10)
        hour_header.grid(row=4,column=4,pady=10)
        yearfilter.grid(row=5,column=1)
        monthfilter.grid(row=5,column=2)
        dayfilter.grid(row=5,column=3)
        hourfilter.grid(row=5,column=4)
        savesettings.grid(row=6,column=1,columnspan=4,pady=10)
        advancedoptionshowing=True
    else:
        widgets=[defautoption,
        customoption,
        previousoption,
        previousfilter,
        year_header,
        month_header,
        day_header,
        hour_header,
        yearfilter,
        monthfilter,
        dayfilter,
        hourfilter,
        savesettings]
        for i in widgets:
            i.grid_remove()
        advancedoptionshowing=False
tk.Button(root,text='Advanced',command=advanced).grid(row=0,column=1,columnspan=4)
root.mainloop()