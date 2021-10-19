from tkinter import *
import speech_recognition as sr
from tkinter import filedialog as fd

root = Tk()
root.title('Convert Wav to Text')
root.geometry("500x450")


def openFile():
    r = sr.Recognizer()
    
    filepath = fd.askopenfilename(title="Open file okay?",
                                          filetypes= (("text files","*.wav"),
                                          ("all files","*.*")))
    
    harvard = sr.AudioFile(filepath)
    with harvard as source:
        audio = r.record(source)

        data_wav = r.recognize_google(audio, language = 'th')
        my_text.insert(END,data_wav)
        
    
def saveFile():
    text_file = open('test.txt','w',encoding='utf8') 
    text_file.write(my_text.get(1.0, END))

my_text = Text(root, width = 52, height =15, font =('Helvetica', 12))
my_text.pack(pady = 20)

open_button = Button(root, text = 'Open Text File',command = openFile)
open_button.pack(pady = 20)

file_save = Button(root, text="Save file", command = saveFile)
file_save.pack(padx=150)


root.mainloop()

