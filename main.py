from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mysql.connector import connect, Error
from pygame import mixer
from time import sleep

    

    

buttonsBackground = "#17a780"
buttonsForeground = "#ffffff"
font = "B Nazanin"
icon = "C:/Book/data/Icon/bookIcon.ico"
buttonSongPath = "C:/Book/data/Music/Button song.mp3"
buttonLSongPath = "C:/Book/data/Music/Button song.mp3"
pageSongPath = "C:/Book/data/Music/Page song.mp3"
pageSong = mixer
pageSong.init()
pageSong.music.load(pageSongPath)
pageSong.music.play()

def size(form, width, height):
    w = width
    h = height
    ws = form.winfo_screenwidth()
    hs = form.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    form.minsize(width, height)
    form.maxsize(width, height)
    form.geometry("%dx%d+%d+%d" % (w, h, x, y))

class CSQL:
    flag=False
    def __init__(self):
        self.SqlGui=Tk()
        size(self.SqlGui,800,350)
        self.SqlGui.iconbitmap(icon)
        self.SqlGui.title("اتصال به دیتابیس")
        self.SqlGui.configure(bg='#404040')
        labelTitle= Label(master=self.SqlGui, text="اتصال به دیتایبس",background="#404040", foreground="#ffffff", font=(font, 30))
        labelTitle.grid(row=0,padx=300,pady=5, sticky="w")
        labelHost= Label(master=self.SqlGui, text="Host",background="#404040", foreground="#ffffff", font=(font, 20))
        labelHost.grid(row=1,padx=15,pady=5, sticky="w")

        entryHost = Entry(master=self.SqlGui,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryHost.setvar("localhost")
        entryHost.grid(row=1,padx=150,pady=5, sticky="w")
        
        
        labelUser= Label(master=self.SqlGui, text="User",background="#404040", foreground="#ffffff", font=(font, 20))
        labelUser.grid(row=2,padx=15,pady=5, sticky="w")


        entryUser = Entry(master=self.SqlGui,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryUser.setvar("root")
        entryUser.grid(row=2,padx=150,pady=5, sticky="w")
        
        labelPassword= Label(master=self.SqlGui, text="Password",background="#404040", foreground="#ffffff", font=(font, 20))
        labelPassword.grid(row=3,padx=15,pady=5, sticky="w")


        entryPassword = Entry(master=self.SqlGui,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryPassword.grid(row=3,padx=150,pady=5, sticky="w")
        
        buttonContinuation=Button(master=self.SqlGui, text="اتصال", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=45)
        buttonContinuation.bind("<Button>",lambda event: self.connection(event,entryHost.get(),entryUser.get(),entryPassword.get()))
        buttonContinuation.grid(row=4, padx=15,pady=5,sticky="w")
        self.SqlGui.mainloop()

    def connection(self,event,Host,User,Password):
        
        try:
            self.SQL =connect(host=Host,user=User,password=Password)
            self.mySQl=self.SQL.cursor()
        except Error as error:
            print(error)
            answer=messagebox.askretrycancel("خطا", error)
            if answer:
                self.SqlGui.mainloop()
        else:
            try:
                self.mySQl.execute("Create Database dbBook")
            except:
                CSQL.flag=True
            else:
                self.mySQl.execute("Create Table dbBook.books(RecordNumber int primary key,HelpNumber varChar(120),Title varChar(120),Creator varChar(120),PublicationDetails varChar(120))")
                messagebox.showinfo("وضعیت","دیتابیس ساخته شد")
                CSQL.flag=True
        self.SqlGui.destroy()
        self.SQL.commit()
    

        
    def delete(self,key):
        self.mySQl.execute(f'delete from dbBook.books where RecordNumber={key}')
        self.SQL.commit()
        
        
    def insert(self,RecordNumber,HelpNumber,Title,Creator,PublicationDetails):
        try:
            self.mySQl.execute(f'Insert Into dbbook.books (RecordNumber,HelpNumber,Title,Creator,PublicationDetails) Values({RecordNumber}, "{HelpNumber}", "{Title}", "{Creator}", "{PublicationDetails}")')
            self.SQL.commit()                     
        except Error as error:
            print(error)
            messagebox.showerror("خطا", f"شماره رکورد ({RecordNumber}) وجود دارد")
        else:
            messagebox.showinfo("وضعیت", "!!!با موفقیت ثبت شد")


    def select(self,RecordNumber):
        self.mySQl.execute(f"Select * from dbBook.books where RecordNumber={RecordNumber}")                                     
        return self.mySQl
    def selects(self):
        self.mySQl.execute(f"select * from dbBook.books")                 
        return self.mySQl




class GUI:
    def addBook(self,event,RecordNumber,HelpNumber,Title,Creator,PublicationDetails,nameForm):
        GUI.buttonSong()
        result = messagebox.askyesnocancel(
            "سوال", "آیا اطمینان برای ذخیره اطلاعات کتاب دارید؟", default=messagebox.NO)
        
    
        if result == True:     
            self.dataBase.insert(RecordNumber,HelpNumber,Title,Creator,PublicationDetails)    
            nameForm.destroy()
        elif result == False:
            nameForm.destroy()

    


    def removeBook(self,event,RecordNumber,nameForm):
        GUI.buttonSong()
        result = messagebox.askyesnocancel("سوال", "آیا اطمینان برای حذف کتاب دارید؟", default=messagebox.NO)
        if result == True:
            self.dataBase.delete(RecordNumber)
            messagebox.showinfo("وضعیت","!!!کتاب حذف شد")
            nameForm.destroy()
        elif result == False:
            nameForm.destroy()
        elif result == None:
            nameForm.destroy()


    def showBook(self,event,RecordNumber,nameForm):
        GUI.buttonSong()
        try:
            books=self.dataBase.select(RecordNumber)
        except Error as error:
            print(error)
            messagebox.showerror("خطا", f"رکوردی یافت نشد")
        else:
            tree = ttk.Treeview(master=nameForm, column=("RecordNumber", "HelpNumber", "Title","Creator","PublicationDetails"), show='headings', height=3)
            tree.grid(row=11, columnspan=3,pady=5,padx=40, sticky="w")
            tree.column("# 1", anchor=CENTER, width=120)
            tree.heading("# 1", text="شماره رکورد")
            tree.column("# 2", anchor=CENTER, width=120)
            tree.heading("# 2", text="شماره راهنما")
            tree.column("# 3", anchor=CENTER, width=120)
            tree.heading("# 3", text="عنوان")
            tree.column("# 4", anchor=CENTER, width=120)
            tree.heading("# 4", text="پدیدآور")
            tree.column("# 5", anchor=CENTER, width=135)
            tree.heading("# 5", text="مشخصات نشر")
            i=1
            for book in books:
                tree.insert('', 'end', text=str(i), values=(book[0], book[1], book[2], book[3],book[4]))
                i+=1
            if i==1:
                messagebox.showerror("خطا", f"رکوردی یافت نشد")
                nameForm.destroy()
    
    def buttonSong():
        buttonSong = mixer
        buttonSong.init()
        buttonSong.music.load(buttonSongPath)
        buttonSong.music.play()
        sleep(0.18)
        pageSong.music.load(pageSongPath)
        buttonSong.music.play()

    def showInfoApp():
        GUI.buttonSong()
        messagebox.showinfo("درباره نرم افزار","نسخه نرم افزار : 1.0.0\nتاریخ ساخت : 14001401-02-22\nسازنده : سورن شاملو")

        

    def music(nameForm):
        unpauseButton = Button(master=nameForm,text="▶",font=("None", 25),width=3,height=0,foreground=buttonsBackground,background="#404040",command=GUI.pause)
        pauseButton = Button(master=nameForm,text="⏸",font=("None", 25),width=3,height=0,foreground=buttonsBackground,background="#404040",command=GUI.unpause)
        stopButton = Button(master=nameForm,text="🔇",font=(font, 20),width=3,height=0,foreground=buttonsBackground,background="#404040",command=GUI.stop)
        playButton = Button(master=nameForm,text="🔊",font=(font, 20),width=3,height=0,foreground=buttonsBackground,background="#404040",command=GUI.play)
        unpauseButton.grid(row=10, padx=20, pady=19,column=0, sticky="w")
        pauseButton.grid(row=10, padx=100, pady=19,column=0, sticky="w")
        stopButton.grid(row=10, padx=180, pady=19,column=0, sticky="w")
        playButton.grid(row=10, padx=255, pady=19,column=0, sticky="w")



    def unpause():
        pageSong.music.unpause()

    def pause():
        pageSong.music.pause()

    def stop():
        pageSong.music.stop()

    def play():
        pageSong.music.play()

    def record(self):
        GUI.buttonSong()
        self.recordForm = Toplevel(self.root)
        self.recordForm.title("ثبت کتاب")
        size(self.recordForm, 700, 800)
        self.recordForm.iconbitmap(icon)
        self.recordForm.configure(bg='#404040')

        menubar = Menu(master=self.recordForm)
        menubar.add_command(label="حذف کتاب", command=self.delete,background="#404040")
        menubar.add_command(label="ثبت کتاب",command=self.record,    background="#404040")
        menubar.add_command(label="نمایش کتاب",command=self.show, background="#404040")
        menubar.add_command(label="نمایش کتاب ها",command=self.shows, background="#404040")
        menubar.add_command(label="درباره نرم افزار",command=GUI.showInfoApp, background="#404040")
        self.recordForm.config(menu=menubar)
        imgForm = Label(master=self.recordForm, text="📖", font=(None, 150), background="#404040", foreground=buttonsBackground)
        imgForm.grid(row=0,padx=230,pady=0, sticky="w")

        labelTextInfo = Label(master=self.recordForm, text=":ثبت کتاب", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=1,padx=560,pady=0, sticky="w")

        labelTextInfo = Label(master=self.recordForm, text=".لطفا اطلاعات خواسته شده را وارد کنید", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=2,padx=205,pady=0, sticky="w")

        labelRecordNumber= Label(master=self.recordForm, text="شماره رکورد",background="#404040", foreground="#ffffff", font=(font, 20))
        labelRecordNumber.grid(row=3,padx=580,pady=5, sticky="w")

        entryRecordNumber = Entry(master=self.recordForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryRecordNumber.grid(row=3,padx=15,pady=5, sticky="w")
        labelHelpNumber= Label(master=self.recordForm, text="شماره راهنما",background="#404040", foreground="#ffffff", font=(font, 20))
        labelHelpNumber.grid(row=4,padx=580,pady=5, sticky="w")

        entryHelpNumber = Entry(master=self.recordForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryHelpNumber.grid(row=4,padx=15,pady=5, sticky="w")

        labelTitle= Label(master=self.recordForm, text="عنوان",background="#404040", foreground="#ffffff", font=(font, 20))
        labelTitle.grid(row=5,padx=640,pady=5, sticky="w")

        entryTitle = Entry(master=self.recordForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryTitle.grid(row=5,padx=15,pady=5, sticky="w")

        labelCreator = Label(master=self.recordForm, text="پدیدآورنده",background="#404040", foreground="#ffffff", font=(font, 20))
        labelCreator.grid(row=6,padx=600,pady=5, sticky="w")

        entryCreator= Entry(master=self.recordForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryCreator.grid(row=6,padx=15,pady=5, sticky="w")


        labelPublicationDetails = Label(master=self.recordForm, text="مشخصات نشر",background="#404040", foreground="#ffffff", font=(font, 20))
        labelPublicationDetails.grid(row=7,padx=570,pady=5, sticky="w")

        entryPublicationDetails= Entry(master=self.recordForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50,)
        entryPublicationDetails.grid(row=7,padx=15,pady=5, sticky="w")
        
        GUI.music(self.recordForm)
        buttonContinuationRecord=Button(master=self.recordForm, text="ثبت", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=21)
        buttonContinuationRecord.bind("<Button>",lambda event: self.addBook(event,int(entryRecordNumber.get()),entryHelpNumber.get(),entryTitle.get(),entryCreator.get(),entryPublicationDetails.get(),self.recordForm))
        buttonContinuationRecord.grid(row=10, padx=325,pady=5,sticky="w")

    def delete(self):
        GUI.buttonSong()
        self.deleteForm = Toplevel(self.root)
        size(self.deleteForm, 700, 580)
        self.deleteForm.title("حذف کتاب")
        self.deleteForm.iconbitmap(icon)
        self.deleteForm.configure(bg='#404040')

        menubar = Menu(master=self.deleteForm)
        menubar.add_command(label="حذف کتاب", command=self.delete,background="#404040")
        menubar.add_command(label="ثبت کتاب",command=self.record,    background="#404040")
        menubar.add_command(label="نمایش کتاب",command=self.show, background="#404040")
        menubar.add_command(label="نمایش کتاب ها",command=self.shows, background="#404040")
        menubar.add_command(label="درباره نرم افزار",command=GUI.showInfoApp, background="#404040")
        self.deleteForm.config(menu=menubar)

        imgForm = Label(master=self.deleteForm, text="📖", font=(None, 150), background="#404040", foreground=buttonsBackground)
        imgForm.grid(row=0,padx=230,pady=0, sticky="w")
        labelTextInfo = Label(master=self.deleteForm, text=":حذف کتاب", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=1,padx=550,pady=0, sticky="w")

        labelTextInfo = Label(master=self.deleteForm, text=".لطفا اطلاعات خواسته شده را وارد کنید", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=2,padx=205,pady=0, sticky="w")

        labelRecordNumber= Label(master=self.deleteForm, text="شماره رکورد",background="#404040", foreground="#ffffff", font=(font, 20))
        labelRecordNumber.grid(row=3,padx=580,pady=5, sticky="w")

        entryRecordNumber = Entry(master=self.deleteForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryRecordNumber.grid(row=3,padx=15,pady=5, sticky="w")

        buttonContinuationDelete=Button(master=self.deleteForm, text="حذف", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=21)
        buttonContinuationDelete.bind("<Button>",lambda event: self.removeBook(event,int(entryRecordNumber.get()),self.deleteForm))
        buttonContinuationDelete.grid(row=10, padx=325,pady=5,sticky="w")
        GUI.music(self.deleteForm)


    def show(self):
        GUI.buttonSong()
        self.showForm = Toplevel(self.root)
        size(self.showForm, 700, 700)
        self.showForm.title("نمایش کتاب")
        self.showForm.iconbitmap(icon)
        self.showForm.configure(bg='#404040')

        menubar = Menu(master=self.showForm)
        menubar.add_command(label="حذف کتاب", command=self.delete,background="#404040")
        menubar.add_command(label="ثبت کتاب",command=self.record,    background="#404040")
        menubar.add_command(label="نمایش کتاب",command=self.show, background="#404040")
        menubar.add_command(label="نمایش کتاب ها",command=self.shows, background="#404040")
        menubar.add_command(label="درباره نرم افزار",command=GUI.showInfoApp, background="#404040")
        self.showForm.config(menu=menubar)
        imgForm = Label(master=self.showForm, text="📖", font=(None, 150), background="#404040", foreground=buttonsBackground)
        imgForm.grid(row=0,padx=230,pady=0, sticky="w")
        labelTextInfo = Label(master=self.showForm, text=":نمایش کتاب", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=1,padx=530,pady=0, sticky="w")

        labelTextInfo = Label(master=self.showForm, text=".لطفا اطلاعات خواسته شده را وارد کنید", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=2,padx=205,pady=0, sticky="w")

        labelRecordNumber= Label(master=self.showForm, text="شماره رکورد",background="#404040", foreground="#ffffff", font=(font, 20))
        labelRecordNumber.grid(row=3,padx=580,pady=5, sticky="w")

        entryRecordNumber = Entry(master=self.showForm,background="#404060",foreground=buttonsBackground, font=(font, 18),width=50)
        entryRecordNumber.grid(row=3,padx=15,pady=5, sticky="w")

        buttonContinuationShow=Button(master=self.showForm, text="جست و جو", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=21)
        buttonContinuationShow.bind("<Button>",lambda event: self.showBook(event,int(entryRecordNumber.get()),self.showForm))
        buttonContinuationShow.grid(row=10, padx=325,pady=5,sticky="w")
        GUI.music(self.showForm)
    def shows(self):
        GUI.buttonSong()
        self.showsForm = Toplevel(self.root)
        size(self.showsForm, 700, 700)
        self.showsForm.title("نمایش کتاب ها")
        self.showsForm.iconbitmap(icon)
        self. showsForm.configure(bg='#404040')
       
        menubar = Menu(master=self.showsForm)
        menubar.add_command(label="حذف کتاب", command=self.delete,background="#404040")
        menubar.add_command(label="ثبت کتاب",command=self.record,    background="#404040")
        menubar.add_command(label="نمایش کتاب",command=self.show, background="#404040")
        menubar.add_command(label="نمایش کتاب ها",command=self.shows, background="#404040")
        menubar.add_command(label="درباره نرم افزار",command=GUI.showInfoApp, background="#404040")
        self.showsForm.config(menu=menubar)

        imgForm = Label(master=self.showsForm, text="📖", font=(None, 150), background="#404040", foreground=buttonsBackground)
        imgForm.grid(row=0,padx=230,pady=0, sticky="w")
        labelTextInfo = Label(master=self.showsForm, text=":نمایش کتاب ها", font=(font, 30), background="#404040", foreground="#ffffff")
        labelTextInfo.grid(row=1,padx=480,pady=0, sticky="w")
        GUI.music(self.showsForm)
        books=self.dataBase.selects()
        tree = ttk.Treeview(master=self.showsForm, column=("RecordNumber", "HelpNumber", "Title","Creator","PublicationDetails"), show='headings', height=12)
        tree.grid(row=11, columnspan=3,pady=5,padx=40, sticky="w")
        tree.column("# 1", anchor=CENTER, width=120)
        tree.heading("# 1", text="شماره رکورد")
        tree.column("# 2", anchor=CENTER, width=120)
        tree.heading("# 2", text="شماره راهنما")
        tree.column("# 3", anchor=CENTER, width=120)
        tree.heading("# 3", text="عنوان")
        tree.column("# 4", anchor=CENTER, width=120)
        tree.heading("# 4", text="پدیدآور")
        tree.column("# 5", anchor=CENTER, width=135)
        tree.heading("# 5", text="مشخصات نشر")
        item=1
        for book in books:
            tree.insert('', 'end', text=str(item), values=(book[0], book[1], book[2], book[3],book[4]))
            item+=1
    def __init__(self):
        
        self.dataBase =CSQL()
        self.root = Tk()
        size(self.root, 750, 850)
        self.root.iconbitmap(icon)
        self.root.title("سیستم کتابداری")
        self.root.configure(bg='#404040')
        self.imgForm = Label(master=self.root,text="📖",font=(None, 150),background="#404040",foreground=buttonsBackground)
        self.imgForm.grid(row=0, column=0, pady=5, padx=250, sticky="w")
        self.labelTitleText = Label(master=self.root, text="سیستم کتابداری", font=(font, 30), background="#404040", foreground="#ffffff")
        self.labelTitleText.grid(row=1, column=0, sticky="we")
        self.labelSelectionText = Label(master=self.root, text=".گزینه مورد نظر خود را انتخاب کنید", font=(font, 25), background="#404040", foreground="#ffffff")
        self.labelSelectionText.grid(row=2, column=0, sticky="we")
        self.buttonRecord = Button(master=self.root, text="ثبت کتاب", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=42, command=self.record)
        self.buttonRecord.grid(row=3, column=0, padx=13,pady=5)
        self.buttonDelete=Button(master=self.root, text="حذف کتاب", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=42, command=self.delete)
        self.buttonDelete.grid(row=4, column=0, padx=13,pady=5)
        self.buttonShow=Button(master=self.root, text="نمایش کتاب", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=42, command=self.show)
        self.buttonShow.grid(row=5, column=0, padx=13,pady=5)
        self.buttonShows=Button(master=self.root, text="نمایش کتاب ها", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=42, command=self.shows)
        self.buttonShows.grid(row=6, column=0, padx=13,pady=5)
        self.buttonShowInfo=Button(master=self.root, text="درباره نرم افزار", font=(font, 20), background=buttonsBackground, foreground=buttonsForeground, width=23, command=GUI.showInfoApp)
        self.buttonShowInfo.grid(row=10, column=0, padx=16,pady=5,sticky="e")
        GUI.music(self.root)


        menubar = Menu(master=self.root)
        menubar.add_command(label="حذف کتاب", command=self.delete,background="#404040")
        menubar.add_command(label="ثبت کتاب",command=self.record,    background="#404040")
        menubar.add_command(label="نمایش کتاب",command=self.show, background="#404040")
        menubar.add_command(label="نمایش کتاب ها",command=self.shows, background="#404040")
        menubar.add_command(label="درباره نرم افزار",command=GUI.showInfoApp, background="#404040")
        self.root.config(menu=menubar)
        if CSQL.flag == True:
                self.root.mainloop()
        









g = GUI()
