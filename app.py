import tkinter as tk
import threading
import pyaudio
import wave
import speech_recognition as sr


class App():
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
    fs = 44100  
    
    frames = []  
    def __init__(self, master):
       

        self.isrecording = False
        self.button1 = tk.Button(main, text='Start',command=self.startrecording)
        self.button2 = tk.Button(main, text='Stop',command=self.stoprecording)
        self.button3 = tk.Button(main, text='Translate',command=self.translate_voice)
      
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()

    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
        
        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename= 'voice'
        self.filename = self.filename+".wav"
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
    def translate_voice(self):
        r = sr.Recognizer()

        harvard = sr.AudioFile('voice.wav')
        with harvard as source:
            audio = r.record(source)

            data_wav = r.recognize_google(audio, language = 'th')
#             df = pd.DataFrame(data_wav, columns = ['text'])
#             result = df.to_json(orient="records")
#             parsed = json.loads(result)
            print(data_wav)
        
    def record(self):
       
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

main = tk.Tk()
main.title('recorder')
main.geometry('200x100')
app = App(main)
main.mainloop()