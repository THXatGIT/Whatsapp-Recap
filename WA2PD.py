import datetime
from pandas import DataFrame as df
import re
def to_pd(txtfile,group):
    ''' This function converts the Whatsapp text files to Pandas Dataframe
        to_pd(txtfile,group) --> returns DataFrame, groupname(str)'''
    user=[]
    chattype=[]
    message=[]
    dandt=[]
    with open(txtfile, 'r',encoding='utf-8') as chats:
        # ? is for non-greedy and the one in round brackets is to make sure nothing is behind it
        ios=re.compile("(?<!.)\[.*?\]") #regex pattern for ios whatsapp export format
        android=re.compile("(?<!.)..\/..\/.*,.*?:.*?:") #These regex is used to separate human from system messages
        chatlist=chats.readlines()
        if ios.match(chatlist[0]) : #Check for ios mode or not
            iosmode=True
            for chat in chatlist:
                if ios.match(chat.replace("\u200e",'')):
                    text=chat[chat.index(':',chat.index(']'))+2:-1]
                    user.append(chat[chat.index(']')+2:chat.index(':',chat.index(']'))])
                    dandt.append(datetime.datetime.strptime(chat[chat.index('[')+1:chat.index(']')], "%d/%m/%y, %I:%M:%S %p"))
                    if text=="\u200e<Media omitted>" or text=="\u200evideo omitted" or text=="\u200eimage omitted" or text=='\u200esticker omitted' or 'document omitted' in text:
                        message.append('')
                        chattype.append('MEDIA')
                    elif text=="\u200ePOLL:":
                        message.append(text)
                        chattype.append('POLL')
                    elif "This message was deleted."==text or "You deleted this message."==text:
                        message.append('')
                        chattype.append('TEXT')
                    elif "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them." in chat\
                     or "Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more." in chat\
                    or chat.split()[-4:]=="changed the group description".split()\
                    or "created group “" in chat\
                    or "changed this group's settings" in chat\
                    or chat.split()[-2:]=='added you'.split()\
                    or "changed the group name to “" in chat\
                    or f"added {user[-1]}" in chat:
                        user[-1]="System"
                        message.append(text)
                        chattype.append("LOG")
                        if "created group “" in chat or "changed the group name to “"in chat:
                            group=chat[chat.index('“')+1:chat.index('”')]
                        continue
                    else:
                        message.append(text)
                        chattype.append('TEXT')
                else:
                    # if 'OPTION:' not in chat: <-- that was for filtering out polls
                    message[-1]+=chat
                #ends here
            chats.close()
        else:
            for chat in chatlist:
                if android.match(chat):
                    text=chat[chat.index(':',20)+2:-1]
                    user.append(chat[20:chat.index(':',20)])
                    dandt.append(datetime.datetime.strptime(chat[:17], "%d/%m/%Y, %H:%M"))
                    if text=='This message was deleted':
                        message.append('')
                        chattype.append("TEXT")
                    elif text=='<Media omitted>':
                        message.append('')
                        chattype.append("MEDIA")
                    elif text=='POLL:':
                        message.append('')
                        chattype.append("POLL")
                    else:
                        #to remove the \n at the end
                        message.append(text)
                        chattype.append("TEXT")
                else: 
                    #First conditional is for older ver
                    # and there is a problem for added ...
                    if "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them." in chat \
                    or "Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more." in chat\
                    or chat.split()[-4:]=="changed the group description".split() \
                    or "created group “" in chat \
                    or "changed this group's settings" in chat \
                    or chat.split()[-2:]=='added you'.split() \
                    or "changed the group name to “" in chat \
                    or f"added {user[-1]}" in chat:
                        user.append("System")
                        dandt.append(datetime.datetime.strptime(chat[:17], "%d/%m/%Y, %H:%M"))
                        message.append(chat[chat.index('-')+2:])
                        chattype.append("LOG")
                        if "created group “" in chat or "changed the group name to “"in chat:
                            group=chat[chat.index('“')+1:chat.index('”')]
                        continue
                    else:
                        message[-1]+=chat
            chats.close()
    #Table filter
    table=df({'user':user,'type':chattype,"msg":message,"d&t":dandt})
    return table,group