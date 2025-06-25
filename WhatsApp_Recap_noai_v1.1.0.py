# The recap is now even more oragnised with more features
# Added better filters
#Tapping the overall recap button now resets the settings without the need to press the save settings
# Added Year count graph
# Program will stop if nothing happens on that day
#bug1 floating numbers in bar graph with small values (fixed)
#bug2 repeated long message not counted(resolved)
#bug3 Count of message is still wrong (resolved)
#bug4 longest messages get out of box(resolved)
#bug5 if no messages are sent on a specific time range, error would be thrown
#bug6 Long words (resolved)
#font be wonk

#Have image be on toplevel than photos (Nevermind)
#Added Summarizer
#add warnings
#add bump chart for frequency of words?
import os
import sys
from string import punctuation as punc
import emoji as e
from imojify import imojify as imoj
from random import randint
from pandas import DataFrame as df
from pandas import concat
from pandas import to_numeric as tonum
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import font_manager
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import wordcloud as wc
from PIL import Image,ImageDraw,ImageFont,ImageTk
import tkinter as tk
from tkinter import filedialog
import ctypes
import datetime

from WA2PD import to_pd
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def fontwrap(font,text,paragraphs):
    wrappedtext=""
    line=""
    placeholder=""
    for i in text:
        if len(wrappedtext.splitlines())==paragraphs-1:
            placeholder="..."
        if len(wrappedtext.splitlines())>=paragraphs:
            break
        else:
            if font.getlength(line+i+placeholder)<=719 and i != "\n":
                line+=i
            elif i=="\n":
                wrappedtext+=line+"\n"
                line=""
            else:
                wrappedtext+=line[:line.rfind(" ")]+placeholder+"\n"
                if line.rfind(" ")==-1:
                    line=i
                else:
                    line=line[line.rfind(" ")+1:]+i
    if len(wrappedtext.splitlines())<paragraphs:
        wrappedtext+=line
    return wrappedtext
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# init tk page
root=tk.Tk()
# get images
mascots=[ImageTk.PhotoImage(Image.open(resource_path(f"mascot/Whatsapp Recap Mascot{i}.png")).resize((90,78))) for i in range(1,6)]
root.wm_iconphoto(True, mascots[0])
root.title('WhatsApp Recap noai v1.1.0')
root.geometry('1920x1080')
table=None
txtfile=''
filename=''
complete=''
bg=''
bg2=None
finalbg=None
group=''
names=[]
recapyear=tk.StringVar()
recapmonth=tk.StringVar()
recapday=tk.StringVar()
recaphour=tk.StringVar()
recapyear2=tk.StringVar()
recapmonth2=tk.StringVar()
recapday2=tk.StringVar()
recaphour2=tk.StringVar()
recapname=tk.StringVar()
# recapyear.set(str(datetime.date.today().year))
recapyear.set("All")
recapmonth.set("All")
recapday.set("All")
recaphour.set("All")
recapname.set('All')
listofyears=[i for i in range(2009,datetime.date.today().year+1)]
listofdays=[i for i in range(1,32)]
listofhour=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
canvafont=resource_path("CanvaSans-Bold.otf")
kaiti=resource_path("C:\Windows\Fonts\STKaiti.ttf")
arial=resource_path("C:/Windows/Fonts/arial.ttf")
directory='C:/'

daterangeactive=False
recapyear2.set("All")
recapmonth2.set("All")
recapday2.set("All")
recaphour2.set("All")
complete=tk.Label(root,font=(canvafont,17),fg='#0fd012')
recaps=[recapyear,recapmonth,recapday,recaphour]
rangerecaps=[recapyear2,recapmonth2,recapday2,recaphour2]
filteredtextstring=''
# #main code below
def recapfunc():
    global txtfile,complete,bg,bg2,finalbg,group,recapyear,recapmonth,recapday,recaphour,listofyears,listofhour,listofdays,table,AI,filteredtextstring
    plt.rcParams['font.family']=['STKaiti']
    iosmode=False
    year=[]
    month=[]
    date=[]
    dateofweek=[]
    hr=[]
    min=[]
    user=[]
    message=[]
    group=txtfile[-txtfile[::-1].index('/'):].replace('WhatsApp Chat with ','').replace('.txt','')
    monthname={'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
    timename=['12AM','1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']
    datename=['Monday','Tuesday','Wednesday',"Thursday","Friday","Saturday","Sunday"]
    timedict={j:i for i,j in zip(listofhour,timename)}
    table,group=to_pd(txtfile,group)
    # Prevents impossible dates from entering
    if recapmonth.get()!="All" and recapday.get()!="All":
        try:
            datetime.datetime(2024,int(list(monthname.keys())[list(monthname.values()).index(recapmonth.get())]),int(recapday.get()))
            if recapyear.get()!= "All":
                if datetime.datetime(int(recapyear.get()),int(list(monthname.keys())[list(monthname.values()).index(recapmonth.get())]),int(recapday.get())) > datetime.datetime.now():
                    complete.config(text=f"The date does not exist... Yet") #Not going to bother about month or hour
                    complete.grid(row=5,column=0)
                    return
        except ValueError:
            complete.config(text=f"This date does not exist")
            complete.grid(row=5,column=0)
            return
        
    if recapmonth2.get()!="All" and recapday2.get()!="All":
        try:
            datetime.datetime(2024,int(list(monthname.keys())[list(monthname.values()).index(recapmonth2.get())]),int(recapday2.get()))
            if recapyear2.get()!= "All":
                if datetime.datetime(int(recapyear2.get()),int(list(monthname.keys())[list(monthname.values()).index(recapmonth2.get())]),int(recapday2.get()))>datetime.datetime.now():
                    complete.config(text=f"The date does not exist... Yet")
                    complete.grid(row=5,column=0)
                    return
        except ValueError:
            complete.config(text=f"This date does not exist")
            complete.grid(row=5,column=0)
            return
    #Filter time!
    filteredtable=table
    #more complicated filter
    #note to self, prevent smaller dates at bottom and ensure catergories are filled
    if daterangeactive:
        #restrict incomplete date ranges
        if sum(1 for i in [recapyear.get(),recapyear2.get()] if i!='All')==1:
            complete.config(text=f"Fill up Both Year catergories")
            complete.grid(row=5,column=0)
            return
        if sum(1 for i in [recapmonth.get(),recapmonth2.get()] if i!='All')==1:
            complete.config(text=f"Fill up Both Month catergories")
            complete.grid(row=5,column=0)
            return
        if sum(1 for i in [recapday.get(),recapday2.get()] if i!='All')==1:
            complete.config(text=f"Fill up Both Day catergories")
            complete.grid(row=5,column=0)
            return
        if sum(1 for i in [recaphour.get(),recaphour2.get()] if i!='All')==1:
            complete.config(text=f"Fill up Both Hour catergories")
            complete.grid(row=5,column=0)
            return
        # Where the 'fun' part begins
        if any(i.get()=='All' for i in recaps+rangerecaps):
            if sum(1 for i in recaps if i.get()!='All')==1:
                if recapyear.get()!='All':
                    filteredtable=filteredtable.loc[(table['d&t'].dt.year>=int(recapyear.get()))&(table['d&t'].dt.year<=int(recapyear2.get()))]
                elif recapmonth.get()!='All':
                    filteredtable=filteredtable.loc[(table['d&t'].dt.month>=int(list(monthname.keys())[list(monthname.values()).index(recapmonth.get())]))&(table['d&t'].dt.month<=int(list(monthname.keys())[list(monthname.values()).index(recapmonth2.get())]))]
                elif recapday.get()!="All":
                    filteredtable=filteredtable.loc[(table['d&t'].dt.day>=int(recapday.get()))&(table['d&t'].dt.day<=int(recapday2.get()))]
                elif recaphour.get()!='All':
                    filteredtable=filteredtable.loc[(table['d&t'].dt.hour>=int(timedict[recaphour.get()]))&(table['d&t'].dt.hour<=int(timedict[recaphour2.get()]))]
            elif sum(1 for i in recaps if i.get()!='All')==2:
                if recapyear.get()!='All':
                    if recapmonth.get()!='All':
                        filteredtable=filteredtable.loc[(table['d&t'].dt.floor('m')>=f"{recapyear.get()}-{recapmonth.get()}")&(table['d&t'].dt.floor('m')<=f"{recapyear2.get()}-{recapmonth2.get()}")]
                    elif recapday.get()!='All':
                        filteredtable=filteredtable.loc[(table['d&t'].dt.year>=int(recapyear.get()))&(table['d&t'].dt.year<=int(recapyear2.get()))]
                        filteredtable=filteredtable.loc[(table['d&t'].dt.day>=int(recapday.get()))&(table['d&t'].dt.day<=int(recapday2.get()))]
                    else:
                        filteredtable=filteredtable.loc[(table['d&t'].dt.year>=int(recapyear.get()))&(table['d&t'].dt.year<=int(recapyear2.get()))]
                        filteredtable=filteredtable.loc[(table['d&t'].dt.hour>=int(recaphour.get()))&(table['d&t'].dt.hour<=int(recaphour2.get()))]
                elif recapmonth.get()!='All':
                    if recapday.get()!='All':
                        dfmerge=[]
                        for y in listofyears:
                            dfmerge.append(filteredtable.loc[(table['d&t'].dt.floor('d')>=f"{y}-{recapmonth.get()}-{recapday.get()}")&(table['d&t'].dt.floor('d')<=f"{y}-{recapmonth2.get()}-{recapday2.get()}")])
                        filteredtable=concat(dfmerge)
                    else:
                        filteredtable=filteredtable.loc[(table['d&t'].dt.month>=int(list(monthname.keys())[list(monthname.values()).index(recapmonth.get())]))&(table['d&t'].dt.month<=int(list(monthname.keys())[list(monthname.values()).index(recapmonth.get())]))]
                        filteredtable=filteredtable.loc[(table['d&t'].dt.hour>=int(recaphour.get()))&(table['d&t'].dt.hour<=int(recaphour2.get()))]
                else:
                    filteredtable=filteredtable.loc[(table['d&t'].dt.day>=int(recapday.get()))&(table['d&t'].dt.day<=int(recapday2.get()))]
                    filteredtable=filteredtable.loc[(table['d&t'].dt.hour>=int(recaphour.get()))&(table['d&t'].dt.hour<=int(recaphour2.get()))]
            else:
                if recapyear.get()!='All':
                    if recapmonth.get()!='All':
                        if recapday.get()!='All':
                            filteredtable=filteredtable.loc[(table['d&t'].dt.floor('d')>=f"{recapyear.get()}-{recapmonth.get()}-{recapday.get()}")&(table['d&t'].dt.floor('d')<=f"{recapyear2.get()}-{recapmonth2.get()}-{recapday2.get()}")]
                        else:
                            filteredtable=filteredtable.loc[(table['d&t'].dt.floor('m')>=f"{recapyear.get()}-{recapmonth.get()}")&(table['d&t'].dt.floor('m')<=f"{recapyear2.get()}-{recapmonth2.get()}")]
                            filteredtable=filteredtable.loc[(table['d&t'].dt.hour>=int(timedict[recaphour.get()]))&(table['d&t'].dt.hour<=int(timedict[recaphour2.get()]))]
                    #else: 
                        #why, why do you want this?
                else:
                    dfmerge=[]
                    for y in listofyears:
                        dfmerge.append(filteredtable.loc[(table['d&t'].dt.floor('h')>=f"{y}-{recapmonth.get()}-{recapday.get()}-{recaphour.get()}")&(table['d&t'].dt.floor('h')<=f"{y}-{recapmonth2.get()}-{recapday2.get()}-{recaphour2.get()}")])
                    filteredtable=concat(dfmerge)
        else:
            filteredtable=filteredtable.loc[(table['d&t'].dt.floor('h')>=f"{recapyear.get()}-{recapmonth.get()}-{recapday.get()}-{recaphour.get()}")&(table['d&t'].dt.floor('h')<=f"{recapyear2.get()}-{recapmonth2.get()}-{recapday2.get()}-{recaphour2.get()}")]
    else:
        if recapyear.get()!="All":
            filteredtable=filteredtable.loc[table['d&t'].dt.year==int(recapyear.get())]
        if recapmonth.get()!="All":
            filteredtable=filteredtable.loc[table['d&t'].dt.month==int(list(monthname.keys())[list(monthname.values()).index(recapmonth.get())])]
        if recapday.get()!="All":
            filteredtable=filteredtable.loc[table['d&t'].dt.day==int(recapday.get())]
        if recaphour.get()!="All":
            filteredtable=filteredtable.loc[table['d&t'].dt.hour==int(timedict[recaphour.get()])]
    if recapname.get()!="All":
        namerank=user=filteredtable["user"].to_list()
        msglenrank=[len(i) for i in filteredtable["msg"].to_list()]
        filteredtable=filteredtable.loc[table["user"]==recapname.get()]
    user=filteredtable["user"].to_list()
    year=filteredtable['d&t'].dt.strftime("%Y").to_list()
    month=filteredtable['d&t'].dt.strftime("%m").to_list()
    date=filteredtable['d&t'].dt.strftime("%d").to_list()
    dateofweek=filteredtable['d&t'].dt.day_name().to_list()
    hr=filteredtable['d&t'].dt.strftime("%H").to_list()
    min=filteredtable['d&t'].dt.strftime("%M").to_list()
    message=filteredtable["msg"].to_list()
    daytime=filteredtable['d&t'].dt.date.to_list()
    if filteredtable.empty:
        complete.config(text=f"There's Nothing to recap here.")
        complete.grid(row=5,column=0)
        return
    # print(table.loc[tonum(table["month"])==1])
    filteredtextstring="".join(f"{u}:{m}\n" for u, m in zip(user,message))

    msglen=[len(i) for i in message]

    #Longest messages
    longmsg=sorted(list(set(message)),key=len,reverse=True)[0:5]
    tuples=[(date[message.index(i)],monthname[month[message.index(i)]],year[message.index(i)],user[message.index(i)],hr[message.index(i)],min[message.index(i)],len(i)) for i in longmsg]
    toplen={i:j for i,j in zip(longmsg,tuples)}
    def piebar(title, piedata,bardatax,bardatay,xlabel,ylabel):
        global group
        plt.rcParams.update({'font.size': 15})
        fig,(pie,bar)=plt.subplots(1,2,figsize=(20,10))
        fig.suptitle(group+' '+title,fontsize=40)
        pie.pie(piedata, autopct='%1.1f%%',pctdistance=1.1,startangle=90,counterclock=False)
        # pie.legend(labels=dic.keys(),loc='lower left',bbox_to_anchor=(-0.2,0))
        bar.barh(list(bardatax)[::-1],list(bardatay)[::-1],color=(15/255,208/255,17/255))
        for index, value in enumerate(list(bardatay)[::-1]):
            bar.text(value, index, str(value),va='center')
        bar.set_xlabel(xlabel)
        bar.set_ylabel(ylabel)
        fig.canvas.draw()
        plt.close()
        return Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))
    # User Chat count
    if recapname.get()!="All":
        chatsperuser=piebar('Chats of user%',[len(user),len(namerank)-len(user)],[recapname.get(),"Others"],[len(user),len(namerank)-len(user)],'Total Chats','User')
    else:
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
    if recapname.get()!="All":
        locchatsperuser=piebar('Length of Chats of user%',[sum(msglen),sum(msglenrank)-sum(msglen)],[recapname.get(),"Others"],[sum(msglen),sum(msglenrank)-sum(msglen)],'Total Length of Chats','User')
    else:
        lendic={}
        for id, person in enumerate(user):
            if person in lendic:
                lendic[person]+=msglen[id]
            else:
                lendic[person]=msglen[id]
        lendic=dict(sorted(lendic.items(), key=lambda item: item[1],reverse=True))
        locchatsperuser=piebar('Length of Chats per user',lendic.values(),lendic.keys(),lendic.values(),'Total Length of Chats','User')
    
    def bargraph(xdata,ydata,title,xlabel,ylabel,width=10,barlabel=True):
        fig,ax=plt.subplots(figsize=(width,5))
        # for index, value in enumerate(ydata):
        #     plt.text(index,value+1,str(value),ha='center')
        ax.bar(xdata,ydata,color=(15/255,208/255,17/255))
        if barlabel:
            ax.bar_label(ax.containers[0], label_type='edge')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=30)
        fig.canvas.draw()
        plt.close()
        return Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))
    
    # Messages per time (hr)
    lst=[]
    for i in listofhour:
        lst.append(hr.count(i))
    hfh=timename[lst.index(max(lst))]
    messagepertime=bargraph(listofhour,lst,"Total messages per time (hr)",'Time of message (hr)',"Messages")

    #Messages per day
    lst.clear()
    listofday=sorted(list(set(daytime)))
    for i in listofday:
        lst.append(daytime.count(i))
    hfday=listofday[lst.index(max(lst))]
    messageperday=bargraph(listofday,lst,"Total messages per day",'Day',"Messages",20,False)

    #messages per month
    lst.clear()
    for i in monthname.keys():
        lst.append(month.count(i))
    hfm=list(monthname.values())[lst.index(max(lst))]
    messagepermonth=bargraph(monthname.keys(),lst,"Messages per month",'Month',"Messages")

    #messages per year
    lst.clear()
    deets=sorted(list(set(year)))
    for i in deets:
        lst.append(year.count(i))
    hfy=deets[lst.index(max(lst))]
    messageperyear=bargraph(deets,lst,"Messages per year",'Year',"Messages")

    #wordcloud
    wordlist=[]
    wordfreq={}
    for i in message:
        for j in i.lower().translate(str.maketrans(dict.fromkeys(punc))).split():
            wordlist.append(j) #removes punctuations
    for i in wordlist:
        if i in wordfreq and i not in wc.STOPWORDS and not any(k in i for k in e.EMOJI_DATA) and not i.isnumeric(): #oops, might take longer now
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
    fig.suptitle(group+' WordCloud',fontsize=30)
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

    #emojitime!
    emodict={}
    for m in message:
        for i in m.split():
            if i in e.EMOJI_DATA:
                if i in emodict:
                    emodict[i]+=1
                else:
                    emodict[i]=1
    emodict=dict(sorted(emodict.items(), key=lambda item: item[1],reverse=True))
    plt.clf()
    fig,ax=plt.subplots(figsize=(20,10))
    ax.barh(list(emodict.keys())[:10],list(emodict.values())[:10],color=(15/255,208/255,17/255))
    ax.bar_label(ax.containers[0], label_type='edge')
    ax.set_xlabel('Emoji Frequency')
    ax.set_ylabel('Emoji')
    ax.set_title('Frequently used emojis',fontsize=30)
    ax.invert_yaxis()
    for i,j in enumerate(list(emodict.keys())[:10]):
        getemoji = plt.imread(imoj.get_img_path(j))
        im = OffsetImage(getemoji, zoom=0.05)
        im.image.axes = ax
        ab = AnnotationBbox(im, (0,i), frameon=False, pad=0)
        ax.add_artist(ab)
    plt.tight_layout()
    fig.canvas.draw()
    emograph=Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))
    plt.close()


    #PIL stuff
    recapimg=Image.new("RGB",(1588,2245*2))
    bg=Image.open(resource_path("background.png")).resize((1588,2245))
    Image.Image.paste(recapimg,bg)
    Image.Image.paste(recapimg,bg,(0,2245))
    sentirecapimg=Image.new("RGB",(1588,2245*2))
    Image.Image.paste(sentirecapimg,bg)
    Image.Image.paste(sentirecapimg,bg,(0,2245))
    rcap=ImageDraw.Draw(recapimg)
    sentircap=ImageDraw.Draw(sentirecapimg)
    # Chinese text and length giving me problems :/ NOTE: probably try noto font?
    # Try combining Canva with Kaiti and (arial with kaiti) Segoe ui?
    def drawtext (pos,text,size,align="left",surface=rcap):
        global bg
        bfont=ImageFont.truetype(canvafont,150)
        sfont=ImageFont.truetype(canvafont,50)
        cfont=ImageFont.truetype(kaiti,50)
        msgfont=ImageFont.truetype(arial,35)
        cmsgfont=ImageFont.truetype(resource_path('C:\Windows\Fonts\msyh.ttc'),30) #Looks better when it's not light    
        timefont=ImageFont.truetype(arial,20)
        ctimefont=ImageFont.truetype(kaiti,20)
        w,h=pos
        if size=='big':
            _,_,w1,_=surface.textbbox((0,0),text,font=bfont,align=align)
            surface.text(((1588-w1)/2+w,h), text, fill=(15,208,17), font=bfont,stroke_width=10, stroke_fill='white',align=align)
        elif size=='small' and text.isascii():
            _,_,w1,_=surface.textbbox((0,0),text,font=sfont,align=align)
            surface.text(((1588-w1)/2+w,h), text, fill=(15,208,17), font=sfont,stroke_width=3, stroke_fill='white',align=align)
        elif size=='msg':
            if text.isascii():
                surface.text((w,h), fontwrap(msgfont,text,3),fill='black', font=msgfont,align=align)
            else:
                surface.text((w,h), fontwrap(cmsgfont,text,3),fill='black', font=cmsgfont,align=align)
        elif size=='time':
            surface.text((w,h), text,fill='grey', font=timefont,align=align)
        elif size=='name':
            colours=["red","lawngreen","green","cyan","blue","purple","brown"]
            if text.isascii():
                surface.text((w,h), text,fill=colours[randint(0,6)], font=timefont,align=align)
            else:
                surface.text((w,h), text,fill=colours[randint(0,6)], font=ctimefont,align=align)
        else:
            _,_,w1,_=surface.textbbox((0,0),text,font=sfont,align=align)
            surface.text(((1588-w1)/2+w,h), text, fill=(15,208,17), font=cfont,stroke_width=3, stroke_fill='white',align=align)
    def drawline(ypos,surface=rcap):
        surface.line((0,ypos,1588,ypos),width=4,fill=(15,208,17))
    drawtext((0,0),"Whatsapp Rewind",'big')
    if recapname.get() != 'All':
        drawtext((0,200),f"{recapname.get()} in {group} has a total of",'small')
    else:
        drawtext((0,200),f"{group} has a total of",'small')
    drawtext((0,250),f"{len(message)}",'big')
    if recapfilter.get()==1:
        drawtext((0,425),"overall conversations!",'small')
    elif recapfilter.get()==2:
        if prevfilter.get()!="Day":
            drawtext((0,425),f"conversations last {prevfilter.get().lower()}!",'small')
        else:
            drawtext((0,425),f"conversations yesterday!",'small')
    elif recapfilter.get()==3 and not daterangeactive:
        discardtext=""
        preposition=""
        if recapyear.get()!="All":
            discardtext=recapyear.get()
            preposition="in"
        if recapmonth.get()!="All":
            discardtext= recapmonth.get()+" "+discardtext
            preposition="in"
        if recapday.get()!="All":
            discardtext=recapday.get()+" "+discardtext
            preposition="on"
        if recaphour.get()!="All":
            discardtext="at "+recaphour.get()+" "+discardtext
        drawtext((0,425),f"conversations {preposition} {discardtext}!",'small')
    elif daterangeactive:
        firstdate=''
        secondate=''
        if recapyear.get()!="All":
            firstdate=recapyear.get()
            secondate=recapyear2.get()
        if recapmonth.get()!="All":
            firstdate=f"{recapmonth.get()} {firstdate}"
            secondate=f"{recapmonth2.get()} {secondate}"
        if recapday.get()!="All":
            firstdate=f"{recapday.get()} {firstdate}"
            secondate=f"{recapday2.get()} {secondate}"
        if recaphour.get()!="All":
            firstdate=f"{recaphour.get()} {firstdate}"
            secondate=f"{recaphour2.get()} {secondate}"
        drawtext((0,425),f"conversations from {firstdate} to {secondate}!",'small')
    drawline(497)
    if recapname.get()!="All":
        if len(user)/len(namerank) < 0.5:
            drawtext((600,500),f"{recapname.get()} sent \n{len(user)*100/len(namerank):.1f}% \nof the messages",'small',"center")
        else:
            drawtext((600,500),f"{recapname.get()} sent \n{len(user)*100/len(namerank):.1f}% \nof \nTHE \nMESSAGES",'small',"center")
        if sum(msglen)/sum(msglenrank) < 0.5:
            drawtext((600,1105),f"{recapname.get()} had \n{sum(msglen)*100/sum(msglenrank):.1f}% \nof the talk ",'small',"center")
        else:
            drawtext((600,1105),f"{recapname.get()} had \n{sum(msglen)*100/sum(msglenrank):.1f}% \nof THE TALK ",'small',"center")
    else:
        drawtext((600,500),f"{list(chatdic)[0]} \nSent most of \nthe messages",'small',"center")
        drawtext((600,1105),f"{list(lendic)[0]} \n Had the MOST \nto talk about",'small',"center")
    recapimg.paste(chatsperuser.resize((1200,600)),(0,500))
    recapimg.paste(locchatsperuser.resize((1200,600)),(0,1100))
    drawtext((0,1710),"Here are the TOP 5 LONGEST messages",'small','center')
    for msg,data in zip(toplen.keys(),toplen.values()):
        num=list(toplen.keys()).index(msg)
        d,m,y,n,h,mins,l=data
        rcap.rounded_rectangle((50,1790+160*num,1588/2,1940+160*num),fill=(217,253,211),radius=10)
        if msg.isascii():
            drawtext((75,1810+160*num),msg,'msg')
        else:
            drawtext((75,1810+160*num),msg,'msg')
        drawtext((1588/4,1810+165*num),f'{d} {m[:3]} {y}, {l} characters','small','center')
        drawtext((75,1790+160*num),f"~{n}",'name','center')
        drawtext((1588/2-55,1915+160*num),f'{h}:{mins}','time','center')
    drawline(2585)
    #section1
    drawtext((0,2580),"Some of you would have most likely been caught chatting...",'small')
    drawtext((-400,2655),f"in {hfy}",'small')
    drawtext((400,2655),f"in {hfm}",'small')
    drawtext((-400,3140),f"at {hfh}",'small')
    recapimg.paste(messageperyear.resize((800,400)),(0,2730))
    recapimg.paste(messagepermonth.resize((800,400)),(800,2730))
    recapimg.paste(messagepertime.resize((800,400)),(0,3235))
    drawtext((400,3140),f"on {hfd}",'small')
    recapimg.paste(messageperdow.resize((800,400)),(800,3235))
    drawtext((0,3640),f"You had the most conversation on {hfday}",'small')
    recapimg.paste(messageperday.resize((1600,400)),(0,3720))
    # drawline(3640)

    #sentiment/linguistics section
    drawtext((500,0),"Here's a \nwordcloud of all the \nconversations","small","center",surface=sentircap)
    sentirecapimg.paste(wc1.resize((1000,500)),(0,0))
    drawtext((500,500),"Here's a \ngraph of the TOP emojis \nused","small","center",surface=sentircap)
    sentirecapimg.paste(emograph.resize((1000,500)),(0,500))
    drawline(1000,sentircap)
    drawtext((-20,1000),"Here are some other linguistic statistics","small","center",surface=sentircap) #Which has some problems
    wordlist=set()
    for i in message:
        for j in i.lower().split():
            if not any(l in j for l in [".com","http"]) and not any(d.isdigit() for d in j ):
                wordlist.add(j)
    wordlist=sorted(sorted(list(wordlist)),key=len,reverse=True)
    drawtext((-400,1100),"The TOP 3 \nlongest words used are:","small","center",surface=sentircap)
    for index, word in enumerate(wordlist[:3]):
        if len(word)>20:
            wordlist[index]=word[:20]+"..."
    for index, word in enumerate(wordlist[:3]):
        if word.isascii():
            sentircap.text((100,1250+index*80),f"{index+1}.{word}",fill=(15,208,17), font=ImageFont.truetype(canvafont,50),stroke_width=10, stroke_fill='white')
        else:
            sentircap.text((100,1250+index*80),f"{index+1}.{word}",fill=(15,208,17), font=ImageFont.truetype(kaiti,30),stroke_width=10, stroke_fill='white')
    drawtext((400,1100),f"There is a total of \n{len(wordlist)} \nUNIQUE words used\n(excluding links or numbers)","small","center",surface=sentircap)
    drawline(1500,sentircap)
    bg=recapimg.crop((0,0,1588,4150))
    bg2=sentirecapimg
    finalbg=Image.new('RGB',(bg.width,bg.height+bg2.height))
    finalbg.paste(bg,(0,0))
    finalbg.paste(bg2,(0,bg.height))
    finalbg=finalbg.crop((0,0,1588,bg.height+1500))
    # tkinter stuff
    complete.config(text=f'Recap of {group} Complete!')
    complete.grid(row=5,column=0)
#tkinter window
def selectxt():
    global txtfile, filename,names,directory
    if txtfile =='':
        txtfile=filedialog.askopenfilename(initialdir=directory,title='Select WhatsApp Text File',filetypes=(("Text Files",'*.txt'),))
        filename=tk.Label(root,text=txtfile[-txtfile[::-1].index('/'):] +'\nhas been selected',font=(canvafont,17),fg='#0fd012')
        directory=txtfile[:-txtfile[::-1].index('/')]
        filename.grid(row=3,column=0)
        tk.Button(root,text='Recap Whatsapp',image=mascots[1],font=(canvafont,17),fg='#0fd012',bg='light green',compound=tk.LEFT,command=recapfunc).grid(row=4,column=0)
    else:
        txtfile=filedialog.askopenfilename(initialdir=directory,title='Select WhatsApp Text File',filetypes=(("Text Files",'*.txt'),))
        filename.config(text=txtfile[-txtfile[::-1].index('/'):] +'\nhas been selected')
        directory=directory=txtfile[:-txtfile[::-1].index('/')]
    if len(names)!=0:
        names.clear()
    with open(txtfile, 'r',encoding='utf-8') as chats:
        for chat in chats.readlines():
            try:
                if chat[2 and 5] == '/' and chat[20:chat.index(':',20)] not in names:
                    names.append(chat[20:chat.index(':',20)])
            except (IndexError, ValueError): 
                continue
        chats.close()
    names=['All']+sorted(names)
    recapname.set('All')
    #IDK how, but it works
    namefilter['menu'].delete(0, 'end')
    # Insert list of new options (tk._setit hooks them up to var)
    for i in names:
       namefilter['menu'].add_command(label=i, command=tk._setit(recapname, i))
    return txtfile
def imgshow():
    global finalbg
    finalbg.show()
def saverecap():
    global finalbg
    finalbg.save(f"{group} Whatsapp Recap.png")
Title=tk.Label(root,text="Whatsapp Recap",font=(canvafont,50), fg='#0fd012').grid(row=0,column=0)
mascot1=tk.Label(root,image=mascots[0]).grid(row=1,column=0)
select= tk.Button(root,text='Select WhatsApp Text File',font=(canvafont,17),fg='#0fd012',bg='light green',image=mascots[2],compound=tk.LEFT,command=selectxt)
select.grid(row=2,column=0)
tk.Button(root,text="Preview Image",image=mascots[3],font=(canvafont,17),fg='#0fd012',bg='light green',compound=tk.LEFT,command=imgshow).grid(row=6,column=0)
tk.Button(root,text="Save Recap",image=mascots[4],font=(canvafont,17),fg='#0fd012',bg='light green',compound=tk.LEFT,command=saverecap).grid(row=7,column=0)
#width adjustments
root.columnconfigure(0,weight=1)
for i in range(1,5):
    root.columnconfigure(i,weight=1)
#Instructions

def showinstructions():
    # It has acended due to space constraints
    secondwindow=tk.Toplevel()
    secondwindow.title('Instructions')
    secondwindow.geometry('1280x1080')
    # Guide https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/full_scroll.py
    instructframe=tk.Frame(secondwindow)
    # row=10,column=1,columnspan=4, 
    instructframe.pack(fill='both',expand=1)
    instructcanvas=tk.Canvas(instructframe) #Because scroll bar can't be applied on a frame
    instructcanvas.pack(side='left', fill='both', expand=1)
    instructscrollbar=tk.Scrollbar(instructframe,orient='vertical',command=instructcanvas.yview)
    instructscrollbar.pack(side='right', fill='y')
    #Apparently I need to configure my canvas?
    # Configure The Canvas
    instructcanvas.configure(yscrollcommand=instructscrollbar.set)
    instructcanvas.bind('<Configure>', lambda e: instructcanvas.configure(scrollregion = instructcanvas.bbox("all")))
    #need another frame
    frameinframe=tk.Frame(instructcanvas)
    # Add that New frame To a Window In The Canvas
    instructcanvas.create_window((0,0), window=frameinframe, anchor="nw")
    #https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
    def onmousewheel(event):
        instructcanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
    frameinframe.bind_all('<MouseWheel>',onmousewheel)
    Instructions_heading=tk.Label(frameinframe,text='\nInstructions',font=(canvafont,18),fg='#0fd012')
    Instructions= tk.Label(frameinframe,text="""
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
    """
    ,justify='left',font=(canvafont,15),fg='#0fd012')
    Instructions_heading.grid()
    Instructions.grid()
# Instructionsshowing=False
# def showinstructions():
#     global Instructions_heading, Instructions,Instructionsshowing,Instructbutton
#     if not Instructionsshowing:
#         Instructions_heading.grid(row=10,column=1,columnspan=4)
#         Instructions.grid(row=11,column=1,columnspan=4)
#         Instructbutton.config(text='Hide Instructions')
#         Instructionsshowing=True
#     else:
#         Instructions_heading.grid_remove()
#         Instructions.grid_remove()
#         Instructbutton.config(text='Show Instructions')
#         Instructionsshowing=False
Instructbutton=tk.Button(root,text='Show Instructions',command=showinstructions)
Instructbutton.grid(row=9,column=1,columnspan=4)

#filter
prevfilter=tk.StringVar()
recapfilter=tk.IntVar()
recapfilter.set(1)
prev=["Year","Month","Day"]
prevfilter.set(prev[0])
def overall(idc='irdc'):
    global recaps, listofdays, rangerecaps, daterangeactive
    if recapfilter.get()==1:
        for r in recaps+rangerecaps:
            r.set("All")
        prevfilter.set("Year")
        yearfilter.grid_remove()
        monthfilter.grid_remove()
        dayfilter.grid_remove()
        hourfilter.grid_remove()
        year_header.grid_remove()
        month_header.grid_remove()
        day_header.grid_remove()
        hour_header.grid_remove()
        previousfilter.grid_remove()
        addrange.grid_remove()
        yearfilter2.grid_remove()
        monthfilter2.grid_remove()
        dayfilter2.grid_remove()
        hourfilter2.grid_remove()
        year_header2.grid_remove()
        month_header2.grid_remove()
        day_header2.grid_remove()
        hour_header2.grid_remove()
        addrange.config(text="+ Add Range")
        daterangeactive=False
        previousoption.grid(row=2,column=1,columnspan=4,sticky="news")
    if recapfilter.get()==2:
        for r in rangerecaps:
                r.set("All")
        yearfilter.grid_remove()
        monthfilter.grid_remove()
        dayfilter.grid_remove()
        hourfilter.grid_remove()
        year_header.grid_remove()
        month_header.grid_remove()
        day_header.grid_remove()
        hour_header.grid_remove()
        addrange.grid_remove()
        yearfilter2.grid_remove()
        monthfilter2.grid_remove()
        dayfilter2.grid_remove()
        hourfilter2.grid_remove()
        year_header2.grid_remove()
        month_header2.grid_remove()
        day_header2.grid_remove()
        hour_header2.grid_remove()
        addrange.config(text="+ Add Range")
        daterangeactive=False
        previousfilter.grid(row=2,column=3,sticky="W")
        previousoption.grid(row=2,column=2,sticky="E",columnspan=1)
        # if prevfilter.get()=="Overall":
        #     for r in recaps:
        #         r.set("All")
        if prevfilter.get()=="Year":
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
    if recapfilter.get()==3:
        yearfilter.grid(row=5,column=1)
        monthfilter.grid(row=5,column=2)
        dayfilter.grid(row=5,column=3)
        hourfilter.grid(row=5,column=4)
        year_header.grid(row=4,column=1,pady=10)
        month_header.grid(row=4,column=2,pady=10)
        day_header.grid(row=4,column=3,pady=10)
        hour_header.grid(row=4,column=4,pady=10)
        addrange.grid(row=6,column=1,columnspan=4)
        previousfilter.grid_remove()
        previousoption.grid(row=2,column=1,columnspan=4,sticky="news")

def daterange():
    global daterangeactive
    if daterangeactive:
        yearfilter2.grid_remove()
        monthfilter2.grid_remove()
        dayfilter2.grid_remove()
        hourfilter2.grid_remove()
        year_header2.grid_remove()
        month_header2.grid_remove()
        day_header2.grid_remove()
        hour_header2.grid_remove()
        addrange.config(text="+ Add Range")
        daterangeactive=False
    else:
        yearfilter2.grid(row=8,column=1)
        monthfilter2.grid(row=8,column=2)
        dayfilter2.grid(row=8,column=3)
        hourfilter2.grid(row=8,column=4)
        year_header2.grid(row=7,column=1,pady=10)
        month_header2.grid(row=7,column=2,pady=10)
        day_header2.grid(row=7,column=3,pady=10)
        hour_header2.grid(row=7,column=4,pady=10)
        addrange.config(text="- Rmf Range")
        daterangeactive=True 
        
for i in range (1,5):
    root.columnconfigure(i,minsize=100)
defautoption=tk.Radiobutton(root,text="Overall Recap (Default)",variable=recapfilter,value=1,command=overall)
previousoption=tk.Radiobutton(root,text="Recap Previous",variable=recapfilter,value=2,command=overall)
customoption=tk.Radiobutton(root,text="Custom Recap",variable=recapfilter,value=3,command=overall)
previousfilter=tk.OptionMenu(root,prevfilter,*prev,command=overall)
years=["All"]+listofyears
months=["All","January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November","December"]
days=["All"]+listofdays
hours=["All",'12AM','1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']
year_header=tk.Label(root,text="Year")
month_header=tk.Label(root,text="Month")
day_header=tk.Label(root,text="Day")
hour_header=tk.Label(root,text="Hour")
namefilter=tk.OptionMenu(root,recapname, "All")
yearfilter=tk.OptionMenu(root,recapyear,*years)
monthfilter=tk.OptionMenu(root,recapmonth,*months)
dayfilter=tk.OptionMenu(root,recapday,*days)
hourfilter=tk.OptionMenu(root,recaphour,*hours)
#Date Ranges
addrange=tk.Button(root,text="+ Add Range",command=daterange)
yearfilter2=tk.OptionMenu(root,recapyear2,*years)
monthfilter2=tk.OptionMenu(root,recapmonth2,*months)
dayfilter2=tk.OptionMenu(root,recapday2,*days)
hourfilter2=tk.OptionMenu(root,recaphour2,*hours)
year_header2=tk.Label(root,text="Year")
month_header2=tk.Label(root,text="Month")
day_header2=tk.Label(root,text="Day")
hour_header2=tk.Label(root,text="Hour")

namefilter.grid(row=0,column=1,columnspan=4,*names)
defautoption.grid(row=1,column=1,columnspan=4)
previousoption.grid(row=2,column=1,columnspan=4)
customoption.grid(row=3,column=1,columnspan=4)
def close():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()