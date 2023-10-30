from tkinter import *
from PIL import Image, ImageTk

class cMainWindow(Frame):
    temporaryScale = 0.9

    canvas_w = 0
    canvas_h = 0
    cursor_x = 0
    cursor_y = 0
    cursor_w = 0
    cursor_h = 0

    def __init__(self,core,master = None):
        super().__init__(master)

        screen_w = self.master.winfo_screenwidth()
        screen_h = self.master.winfo_screenheight()
        w = int(screen_w * self.temporaryScale)
        h = int(screen_h * self.temporaryScale)

        (cursor_w,cursor_h) = self._loadCursorImage()

        self.core = core

        self.master.title("Amber")
        self.master.geometry(str(w)+'x'+str(h))
        self.master.bind("<KeyPress>", self._key_press)
        self.master.bind("<KeyRelease>", self._key_release)

        self.canvas = Canvas(self.master, bg='#FFFFFF',width=w,height=h)
        self.canvas.grid(row=0, column=0)
        self.canvas.pack(expand = False, side=LEFT,anchor=N,padx=0,pady=0 )

        self.core.configure(w,h,cursor_w,cursor_h,self._onCursolDraw,self._onColorIndicatorCallbackDraw,self._onObjectDraw)

        usageFile = open('resource/usage.txt', 'r')
        usageText = usageFile.read()
        usageFile.close()

        self.canvas.create_text(w-470,100,text=usageText,anchor='nw', font=('ＭＳ ゴシック',12,'bold'), tag='usage',fill='Gray')

        self.master.mainloop()

    def _key_press(self,e):
        self.core.setPressEvent(str(e.keysym),str(e.char))

    def _key_release(self,e):
        self.core.setReleaseEvent(str(e.keysym))

    def _loadCursorImage(self):
        self.normal_img    = ImageTk.PhotoImage(Image.open("resource/cursor_1.png"))
        self.editing_img   = ImageTk.PhotoImage(Image.open("resource/cursor_2.png"))
        self.selecting_img = ImageTk.PhotoImage(Image.open("resource/cursor_3.png"))

        return (self.normal_img.width() , self.normal_img.height() )

    def _onCursolDraw(self,tag,x,y,cursorType):
        self.canvas.delete(tag)

        icon = self.normal_img

        if cursorType == 'editing':
            icon = self.editing_img
        elif cursorType == 'selecting':
            icon = self.selecting_img

        self.canvas.create_image(x,y,image=icon,tag=tag)

    def _onColorIndicatorCallbackDraw(self,tag,x,y,w,h,color):
        self.canvas.delete(tag)
        self.canvas.create_oval(x,y,x+w,y+h,fill=color,outline=color,width=5, tag=tag)

    def _onObjectDraw(self,x,y,objType,tag,text,points,color):
        self.canvas.delete(tag)

        if objType == 'text':
            self.canvas.create_text(x,y,text=text,anchor='nw', font=('ＭＳ ゴシック',18), tag=tag,fill=color)
        elif objType == 'line':
            self.canvas.create_line(points,fill=color,width=5, tag=tag)
        elif objType == 'arrow':
            self.canvas.create_line(points,fill=color,width=5, tag=tag, arrow=LAST)
        elif objType == 'curve':
            self.canvas.create_line(points,fill=color,width=5, tag=tag, arrow=LAST, smooth=1)
        elif objType == 'rectangle':
            self.canvas.create_rectangle(points,outline=color,width=5, tag=tag)
        elif objType == 'triangle':
            self.canvas.create_line(points,fill=color,width=5, tag=tag)
        elif objType == 'ellipse':
            self.canvas.create_oval(points,outline=color,width=5, tag=tag)
        elif objType == 'freeline':
            self.canvas.create_line(points,fill=color,width=5, tag=tag, smooth=1)
        elif objType == 'freearrow':
            self.canvas.create_line(points,fill=color,width=5, tag=tag, arrow=LAST, smooth=1)




