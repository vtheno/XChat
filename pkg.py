#coding=utf-8
from html.parser import HTMLParser
def isNotAscii(s):
    b = s.encode('utf8')
    l = len(b)
    if l == 3:
        return True
    return False

def length(string):
    return sum(2 if isNotAscii(s) else 1 for s in string)

def calcOffSet(string, limit: int):
    temp = 0
    ret = None
    for i, s in enumerate(string):
        if isNotAscii(s):
            temp += 2
        else:
            temp += 1
        if temp > limit:
            ret = i
            break

    return ret

def autoWrap(text):
    strings = text.split("\n")
    buff = [ ]
    for s in strings:
        l = length(s)
        # print( l, s )
        if l < 100:
            buff.append(s)
        else:
            idx = calcOffSet(s, 100)
            #print( idx )
            head = s[:idx]
            buff.append(head)
            #print( "head:", length(head) )
            tail = s[idx:]
            #print( "tail:", length(tail) )
            while length(tail) > 100:
                idx = calcOffSet(tail, 100)
                # print(idx)
                head = tail[:idx]
                #print( length(head) )
                buff.append(head)
                tail = tail[idx:]
            else:
                buff.append(tail)
    return '\n'.join(buff)

# b = autoWrap("你"*200 + "A"*100)
# print( b )

class MHTMLParser(HTMLParser): 
    def __init__(self): 
        HTMLParser.__init__(self) 
        self.datas = []
        self.start = None
    def handle_endtag(self, tag):
        if self.start and tag == 'p':
            self.start = False
    def handle_data(self, data):
        #print( repr(data.strip()) )
        msg = data.strip()
        if self.start and msg:
            self.datas += [("txt", msg)]
    def handle_starttag(self, tag, attrs): 
        #print "Enncountered the beginning of a %s tag" % tag 
        #print( tag, attrs )
        if tag == "img": 
            if len(attrs) == 0: 
                pass 
            else:
                for (variable, value) in attrs: 
                    if variable == "src":
                        self.datas += [("img", value)]

        elif tag == "p":
            self.start = True
def getAllTypeMsg(html):
    html_parser = MHTMLParser()
    from pprint import pprint
    pprint( html )
    html_parser.feed(html)
    html_parser.close()
    data = html_parser.datas
    if data:
        msg_list = []
        txt_msg = []
        while data:
            (typ, msg), data = data[0], data[1:]
            print( typ, msg )
            if typ == 'txt':
                txt_msg.append(msg)
            elif typ == 'img':
                buff = '\n'.join(txt_msg)
                txt_msg = []
                if buff:
                    msg_list.append( ('txt', buff )  )
                msg_list.append( ('img', msg) )
        if txt_msg:
            buff = '\n'.join(txt_msg)
            msg_list.append( ('txt', buff) )
            print( msg_list )
    return msg_list

__all__ = ["autoWrap", "getAllTypeMsg"]
