# -*- coding: utf-8 -*-
"""
@author: Kosmas Pinitas
"""
import sys
import keyboard
import  os
import PyPDF2
import pyttsx3

# text to speech init
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#cleanning the text
def parser(page_content):
    rows = page_content.split("\n")
    digits = 0
    for r in range(0,len(rows[0])):
        if rows[0][r].isdigit() == True:
            digits = digits+1
        else: 
            break
    if digits>0:
        rows[0] = rows[0][digits :]
    if rows[-1].isdigit() == True:
        rows=rows[0:-1]    
    for i in range (0,len(rows)):
       for l in range(1, len(rows[i])):
           if rows[i][l].isupper() == True and rows[i][l-1].islower() == True:
               rows[i] = rows[i].replace(rows[i][l-1]+rows[i][l],rows[i][l-1]+". "+ rows[i][l])
    return rows               
                
#Book selection
def selectBook():
    folder = input("Choose folder:")
    name = input("Give name:")
    directory = os.path.dirname(os.path.realpath(sys.argv[0]))+"\\"+folder+"\\"+name+".pdf"
    return str(directory)


def handleInput():
    if keyboard.is_pressed('q'):
        print("quit")
        return 1
    elif keyboard.is_pressed('p'):
        print("pause")
        return 2
    elif keyboard.is_pressed('c'):
        print("continue")
        return 3
    return 0


def reader():
    pdf_file = open(selectBook(), 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    
    init_page = int( input("Choose page (starts from 0):"))
    stop_page = int( input("Choose page (for all pages whrite -1):"))
    if stop_page == -1 or stop_page == -1:
        stop_page = number_of_pages
    init_row = int(input("Choose a specific row (starts from 0):"))
    
    for pg in range(init_page,stop_page):
        try:
            page = read_pdf.getPage(pg)
            print("page: "+str(pg)+"\n\n")
            page_content = page.extractText()
            page_rows = parser(page_content)
            for i in range(init_row,len(page_rows)):
                engine.say(page_rows[i])
                engine.setProperty('rate',100)   
                engine.runAndWait()
                handler = handleInput()
                if handler  == 1 or handler  == 2:
                    break
            if handler !=0:
                while True:
                    if handler ==1:
                        return  0
                    if  handler == 3:
                        init_row=init_row-1
                        if init_row ==-1 and init_page ==0:
                            init_row = 0
                        elif init_page !=0 and init_row ==-1:
                           init_page = init_page-1
                           init_row= len(page_rows)-1  
                        break      
                    handler = handleInput()
                
                    
        except EOFError :
            engine.say("The End")
            engine.setProperty('rate',100)   
            engine.runAndWait()
            return -1
        
    

reader()
