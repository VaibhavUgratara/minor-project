import mysql.connector as sqltor
import os
import random
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from captcha.image import ImageCaptcha
from datetime import date
from PIL import ImageTk, Image
import smtplib
from email.message import EmailMessage
from tkinter import messagebox
from tkextrafont import Font


cwd=os.getcwd()+"\icons_minor_project"

mydb=sqltor.connect(host="localhost",user="root",password="root",database="test")

key1="AXYZ-33#4-231B"
key2="AXYZ-33#5-231B"
pwd_f=False

def trycon():
    global server, sender
    status=server.noop()[0]
    if(status==250):
        return
    try:
        server=smtplib.SMTP('smtp-mail.outlook.com',587)
        server.starttls()
        server.login(sender,"BBAUsatelliteManager")
    except Exception as e:
        raise e

def send_st_otp(recipient,ID,name):
    trycon()
    try:
        global sender
        global server
        message=f"""Dear
{name},

Welcome to Babasaheb Bhimrao Ambedkar University,
Satellite Centre, Amethi

Your Student ID is {ID}.

Now you can generate a password using this ID.
"""

        email = EmailMessage()
        email["From"] = sender
        email["To"] = recipient
        email["Subject"] = "Welcome to BBAU"
        email.set_content(message)
        server.sendmail(sender,recipient,email.as_string())
    except:
        raise Exception("No Internet")





def appear(event,st_pwd_cat_l,st_pwd_cat_en,val):
    global pwd_f
    if(val=="Yes"):
        st_pwd_cat_l.grid(row=16,column=0,sticky=E)
        st_pwd_cat_en.grid(row=16,column=1,pady=5)
        pwd_f=True
    else:
        if(pwd_f is True):
            st_pwd_cat_l.grid_forget()
            st_pwd_cat_en.grid_forget()


flag=True

try:
    sender="bbaustudentmanager@outlook.com"
    server=smtplib.SMTP('smtp-mail.outlook.com',587)
    server.starttls()
    server.login(sender,"BBAUsatelliteManager")
except:
    flag=False


def send_otp():
    trycon()
    try:
        global sender
        global server
        otp=random.randint(1000,9999)+random.randint(1,9)
        message=f"Admin Your OTP is: {otp}"
        email = EmailMessage()
        email["From"] = sender
        email["To"] = "v.assertive@gmail.com"
        email["Subject"] = "Admin OTP"
        email.set_content(message)
        server.sendmail(sender,"v.assertive@gmail.com",email.as_string())
    except:
        raise Exception("No Internet")
    return otp;
def send_teacher_otp(t_email):
    trycon()
    try:
        global sender
        global server
        otp=random.randint(1000,9999)+random.randint(1,9)
        message=f"Your OTP is: {otp}"
        email = EmailMessage()
        email["From"] = sender
        email["To"] = t_email
        email["Subject"] = "Teacher Login OTP"
        email.set_content(message)
        server.sendmail(sender,t_email,email.as_string())
    except:
        raise Exception("No Internet")
    return otp;


def on_click(event):
    global key_entry
    key_entry.delete(0,END)


class Teacher:
    def teacher_login(self,t_root):
        for i in t_root.slaves():
            i.destroy()
        global mydb
        T_heading=Label(t_root,text="Teacher Login",font=(h_font),bg="white")
        T_heading.pack(pady=(80,10))
        t_frame=Frame(t_root,bg="white")
        t_frame.pack()
        id_label=Label(t_frame,text="Enter Teacher ID: ",font="Arial 10 bold",justify="right",anchor="e",bg="white")
        id_entry=Entry(t_frame,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        id_label.grid(row=0,column=0,sticky=E)
        id_entry.grid(row=0,column=1)
        pass_label=Label(t_frame,text="Enter Password: ",font="Arial 10 bold",justify="right",anchor="e",bg="white")
        pass_entry=Entry(t_frame,width=23,highlightbackground="grey",highlightthickness=1,bd=0,show="●")
        pass_label.grid(row=1,column=0,sticky=E)
        pass_entry.grid(row=1,column=1)
        submit_btn=Button(t_root,text="Submit",cursor="target",command=lambda:self.teacher_validation(t_root,id_entry.get(),pass_entry.get(),mes))
        submit_btn.pack(pady=(30,0))
        mes=Label(t_root,text="",bg="white")
        mes.pack(pady=20)
    def teacher_validation(self,t_root,tID,tPass,mes):
        global mydb
        cursor=mydb.cursor()
        cursor.execute("select t_pass from teacher where t_id=%s",(tID,))
        t_pass=cursor.fetchone()
        if t_pass is None:
            mes.config(text="No such ID exist!!",fg="red")
            return
        t_pass=t_pass[0]
        if(tPass==t_pass):
            for i in t_root.slaves():
                i.destroy()
            cursor.execute("select t_email from teacher where t_id=%s",(tID,))
            t_email=cursor.fetchone()
            t_email=t_email[0]
            # try:
            #     otp=send_teacher_otp(t_email)
            # except:
            #     T_heading=Label(t_root,text="Teacher Login",font=(h_font),bg="white")
            #     T_heading.pack(pady=(80,10))
            #     Label(t_root,text="No Internet",bg="white",fg="red").pack()
            #     back_btn=Button(t_root,text="Back",cursor="target",command=lambda:self.teacher_login(t_root))
            #     back_btn.pack()
            #     return
            otp=random.randint(1000,9999)
            print(otp)
            print(t_email)
            T_heading=Label(t_root,text="Teacher Login",font=(h_font),bg="white")
            T_heading.pack(pady=(80,10))
            t_frame=Frame(t_root,bg="white")
            t_frame.pack()
            otp_label=Label(t_frame,text="Enter OTP: ",bg="white")
            otp_entry=Entry(t_frame,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            otp_label.grid(row=0,column=0)
            otp_entry.grid(row=0,column=1)
            submit_btn=Button(t_root,text="Submit",cursor="target",command=lambda:self.validate_t_otp(t_root,mes,otp,otp_entry.get()))
            submit_btn.pack(pady=20)
            mes=Label(t_root,text="",bg="white")
            mes.pack()
        else:
            mes.config(text="Incorrect Password",fg="red")
    def validate_t_otp(self,t_root,mes,otp,otp_e):
        otp=str(otp)
        if(otp==otp_e):
            self.t_functions(t_root)
        else:
            mes.config(text="Incorrect OTP",fg="red")

    def t_functions(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        a_fn_head=Label(a_root,text="TEACHER FUNCTIONS",bg="white",font=(h_font))
        a_fn_head.pack(pady=(80,2))
        fn_frame=Frame(a_root,bg="white")
        fn_frame.pack(pady=20)
        upload_res=Button(fn_frame,text="Upload Result",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_result(a_root))
        upload_res.grid(pady=20,padx=5,row=0,column=0)
        attendance=Button(fn_frame,text="Upload Attendance",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.upload_attendance(a_root))
        attendance.grid(pady=20,row=1,column=0)
        view_student=Button(fn_frame,text="View Students",height=4,width=25,cursor="target",relief=RIDGE)
        view_student.grid(pady=20,row=2,column=0)

    def add_result(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Upload Student Result",font=(sh_font),bg="white")
        head_l.pack(pady=(80,0))

        f1=Frame(a_root,bg="white")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="white")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=10)
        name_label=Label(f1,text="Enter Student Name: ",font="Arial 10 bold",bg="white")
        name_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        name_label.grid(row=1,column=0)
        name_entry.grid(row=1,column=1,pady=10)
        sem_label=Label(f1,text="Enter Semester: ",font="Arial 10 bold",bg="white")
        sem_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        sem_label.grid(row=2,column=0)
        sem_entry.grid(row=2,column=1,pady=10)
        
        x=[]
        y=[]
        f2=Frame(a_root,bg="#fdfdfd")
        f2.pack()
        for i in range(1,6):
            lab=Label(f2,text=f"Subject {i}: ",bg="#fdfdfd").grid(row=0,column=i-1,padx=10,pady=(20,5))
            sub_label=Label(f2,text=f"Code: ",bg="#fdfdfd").grid(row=1,column=i-1)
            sub_ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
            sub_ent.grid(row=2,column=i-1,padx=10)
            en_lab=Label(f2,text="Grade: ",bg="#fdfdfd").grid(row=3,column=i-1)
            ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
            ent.grid(row=4,column=i-1,padx=10,pady=(0,0))
            y.append(sub_ent)
            x.append(ent)
        f3=Frame(a_root,bg="white")
        f3.pack()
        cgpa_label=Label(f3,text="Enter CGPA: ",bg="white")
        cgpa_entry=Entry(f3,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
        cgpa_label.grid(row=0,column=0)
        cgpa_entry.grid(row=0,column=1,pady=15)
        z=[id_entry,name_entry,sem_entry,cgpa_entry]
        sub_bt=Button(a_root,text="Submit",cursor="target",command=lambda:self.upload_result(a_root,mes,id_entry.get(),name_entry.get(),sem_entry.get(),cgpa_entry.get(),x,y))
        sub_bt.pack(pady=(20,0))
        mes=Label(a_root,text="",bg="white")
        mes.pack()
        back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
        back_btn.pack()

    def upload_result(self,a_root,mess,sID,sName,sem,cgpa,a,b):
        if(sID=="" or sName=="" or cgpa=="" or sem==""):
            mess.config(text="Fill all fields!!",fg="red")
            return
        global mydb
        cursor=mydb.cursor()
        cursor.execute('select s_ID,semester from marks')
        t1=cursor.fetchall()
        cursor.execute('select st_ID from student_details')
        temp=cursor.fetchall()
        ids=[]
        for i in temp:
            ids.append(i[0])
        try:
            sID=int(sID)
            sem=int(sem)
        except:
            mess.config(text="Invalid Entry!!",fg="red")
            return
        if sID not in ids:
            mess.config(text="Invalid ID!!",fg="red")
            return
        t2=(sID,sem)
        if(t2 in t1):
            mess.config(text="Result Already Uploaded",fg="red")
            return
        cursor=mydb.cursor()
        cursor.execute('select st_name from student_details')
        temp=cursor.fetchall()
        names=[]
        for i in temp:
            names.append(i[0])
        if(sName not in names):
            mess.config(text="Enter Correct Name!!",fg="red")
            return
        cursor.execute('insert into marks (s_ID,s_name) values (%s,%s)',(sID,sName))
        sub=[]
        marks=[]
        for i in range(0,len(a)):
            marks.append(a[i].get())
            sub.append(b[i].get())
            if(a[i].get()=="" or b[i].get()==""):
                mess.config(text="Fill all fields!!",fg="red")
                return
        sub.append(sID)
        marks.append(sID)
        a=tuple(sub)
        b=tuple(marks)
        cursor.execute('update marks set sub1=%s,sub2=%s,sub3=%s,sub4=%s,sub5=%s where s_ID=%s',a)
        cursor.execute('update marks set grade1=%s,grade2=%s,grade3=%s,grade4=%s,grade5=%s where s_ID=%s',b)
        cursor.execute('update marks set semester=%s,cgpa=%s where s_ID=%s',(sem,cgpa,sID))
        try:
            mydb.commit()
        except:
            mess.config(text="No Internet",fg="red")
        else:
            mess.config(text="Result Uploaded",fg="green")

    def upload_attendance(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Upload Student Attendance",font=(sh_font),bg="white")
        head_l.pack(pady=(80,10))

        f1=Frame(a_root,bg="white")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="white")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)
        mes=Label(f1,text="",fg="red",bg="white")
        mes.grid(row=1,column=0,columnspan=2)

        sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.uploading_attendance(a_root,id_entry.get(),mes))
        sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

        back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
        back_btn.pack()

    def uploading_attendance(self,a_root,entered_ID,mes):
        if(entered_ID==""):
            mes.config(text="Enter ID")
            return
        try:
            entered_ID=int(entered_ID)
        except:
            mes.config(text="Invalid ID format")
            return
        global mydb
        query="select st_ID from student_details"
        l=[]
        cursor=mydb.cursor()
        cursor.execute(query)
        x=cursor.fetchall()
        for i in x:
            l.append(i[0])
        if(entered_ID not in l):
            mes.config(text="ID not present")
            return
        for i in a_root.slaves():
            i.destroy()
        cursor.execute("select st_name from student_details where st_ID=%s",(entered_ID,))
        s_name=cursor.fetchone()
        s_name=s_name[0]
        h1=Label(a_root,text=f"Upload Attendance of {s_name}",font=(sh_font),bg="white")
        h1.pack(pady=10)
        cursor.execute("select total_days, present from attendance where s_ID=%s",(entered_ID,))
        temp=cursor.fetchone()
        total,present=temp
        add_f=Frame(a_root,bg="#fdfdfd")
        add_f.pack(pady=40)
        total_label=Label(add_f,text="Total Classes (last week): ",bg="#fdfdfd")
        total_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        total_label.grid(row=0,column=0)
        total_entry.grid(row=0,column=1,pady=10)
        attendend_label=Label(add_f,text="Classes Attended: ",bg="#fdfdfd")
        attendend_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        attendend_label.grid(row=1,column=0)
        attendend_entry.grid(row=1,column=1,pady=10)

        submit_btn=Button(a_root,text="Submit",command=lambda:self.update_attendance(entered_ID,int(total)+int(total_entry.get()),int(present)+int(attendend_entry.get()),mes_box))
        submit_btn.pack()

        mes_box=Label(a_root,text="",bg="#fdfdfd",fg="green")
        mes_box.pack(pady=20)

        back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
        back_btn.pack()

    def update_attendance(self,i,t,p,mes_box):
        global mydb
        query="update attendance set total_days=%s,present=%s where s_ID=%s"
        args=(t,p,i)
        cursor=mydb.cursor()
        cursor.execute(query,args)
        mydb.commit()
        mes_box.config(text="Updated")

class Admin:
    
    def otp_section(self,a_root,KEY,mes_lab):
        global key
        KEY=KEY.lstrip()
        if (KEY==""):
            mes_lab.config(text="Enter Key!!")
            return
        elif(KEY==key2):
            global t
            t.teacher_login(a_root)
            return
        elif(KEY!=key1):
            mes_lab.config(text="Wrong Key!!")
            return
        c=0
        for i in a_root.slaves():
            if(c==0):
                c+=1
                continue
            i.destroy()
        try:
            # OTP=send_otp()
            OTP=random.randint(1000,9999)
            print(OTP)
        except:
            n_m=Label(a_root,text="No Internet",fg="red",bg="white")
            n_m.pack(pady=10)
            q_btn=Button(a_root,text="Quit",command=a_root.destroy,cursor="target")
            q_btn.pack()
        else:
            f=Frame(a_root,bg="white")
            f.pack()
            otp_Label=Label(f,text="Enter OTP: ",bg="white")
            otp_entry=Entry(f)
            otp_Label.grid(row=0,column=0)
            otp_entry.grid(row=0,column=1,pady=5)
            sub_btn=Button(a_root,text="Submit",cursor="target",command=lambda:self.otp_checker(a_root,otp_entry.get(),OTP,mes))
            sub_btn.pack(pady=10)
            mes=Label(a_root,text="",fg="red",background="white")
            mes.pack()
    def otp_checker(self,a_root,OTP_entered,OTP_sent,mes):
        try:
            OTP_entered=int(OTP_entered)
        except:
            mes.config(text="INVALID O.T.P. !!")
        else:
            if(OTP_entered==OTP_sent):
                self.adm_functions(a_root)
            else:
                mes.config(text="INVALID O.T.P. !!")
    def adm_functions(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        a_fn_head=Label(a_root,text="ADMIN FUNCTIONS",bg="white",font=(h_font))
        a_fn_head.pack(pady=(80,2))
        fn_frame=Frame(a_root,bg="white")
        fn_frame.pack(pady=20)
        add_st_btn=Button(fn_frame,text="Add Student",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_student(a_root))
        add_st_btn.grid(row=0,column=0,pady=20)
        delete_st_btn=Button(fn_frame,text="Delete Student",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.delete_student(a_root))
        delete_st_btn.grid(pady=20,row=0,column=1,padx=5)
        upload_res=Button(fn_frame,text="Upload Result",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_result(a_root))
        upload_res.grid(pady=20,padx=5,row=1,column=0)
        attendance=Button(fn_frame,text="Upload Attendance",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.upload_attendance(a_root))
        attendance.grid(pady=20,row=1,column=1)
        scholarship=Button(fn_frame,text="Scholarship",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.approve_scholarship(a_root))
        scholarship.grid(pady=20,row=2,column=0)
        activity=Button(fn_frame,text="Activity",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.approve_activity(a_root))
        activity.grid(pady=20,row=2,column=1)
    def approve_activity(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Student Activity",font=(sh_font),bg="white")
        head_l.pack(pady=(80,10))

        f1=Frame(a_root,bg="white")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="white")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)
        mes=Label(f1,text="",fg="red",bg="white")
        mes.grid(row=1,column=0,columnspan=2)

        sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.final_activity_approval(a_root,id_entry.get(),mes))
        sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack()

    def final_activity_approval(self,a_root,entered_ID,mes):
        if(entered_ID==""):
            mes.config(text="Enter ID")
            return
        try:
            entered_ID=int(entered_ID)
        except:
            mes.config(text="Invalid ID format")
            return
        global mydb
        query="select st_ID from student_details"
        l=[]
        cursor=mydb.cursor()
        cursor.execute(query)
        x=cursor.fetchall()
        for i in x:
            l.append(i[0])
        if(entered_ID not in l):
            mes.config(text="ID not present")
            return
        cursor.execute("select applied,granted,s_name,club1,club2,club3 from activity where s_ID=%s",(entered_ID,))
        temp=cursor.fetchone()
        applied,granted,name_s,c1,c2,c3=temp
        if(granted=="yes"):
            mes.config("Already joined a club")
        else:
            if(applied=="yes"):
                a=messagebox.askquestion("Activity",f"Name: {name_s}\nClub 1: {c1}\nClub 2: {c2}\nClub 3: {c3}")
                if(a=="yes"):
                    cursor.execute("update activity set granted=%s where s_ID=%s",('yes',entered_ID))
                    try:
                        mydb.commit()

                    except:
                        mes.config(text="Something went wrong!",fg="red")
                    else:
                        mes.config(text="Club Request Approved",fg="green")
                else:
                    mes.config(text="")
            else:
                mes.config(text="No pending request",fg="black")

    def add_student(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        year12=[]
        for i in range(2024,1989,-1):
            year12.append(i)
        year10=[]
        year10.extend(year12)
        year10.remove(2024)
        year10.remove(2023)
        year10.append(1989)
        year10.append(1988)
        heading_s=Label(a_root,text="Add New Student",font=(sh_font),bg="white")
        heading_s.pack(pady=(80,0))
        false_frame=Frame(a_root)
        false_frame.pack(pady=(0,430))
        f1=Frame(a_root,bg="white")
        f1.place(x=300,y=150)
        f2=Frame(a_root,bg="white")
        f2.place(x=700,y=150)

        name_label=Label(f1,text="*Enter Name: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        name_label.grid(row=0,column=0,sticky=E)
        name_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        name_entry.grid(row=0,column=1)
        course_label=Label(f1,text="*Select Course: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        course_selector=ttk.Combobox(f1,state="readonly",values=["B.C.A.","B.Sc. I.T.","B.A.","B.Com.","B.Sc. F.S.T","D. Pharma","M.A."],width=20)
        course_label.grid(row=1,column=0,sticky=E)
        course_selector.grid(row=1,column=1)

        sem_label=Label(f1,text="*Enter Semester: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        sem_label.grid(row=2,column=0,sticky=E)
        sem_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        sem_entry.grid(row=2,column=1)

        year_label=Label(f1,text="*Enter Year: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        year_label.grid(row=3,column=0,sticky=E)
        year_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        year_entry.grid(row=3,column=1)

        f_name_l=Label(f1,text="*Father's name: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_name_l.grid(row=4,column=0,sticky=E)
        f_name_en.grid(row=4,column=1)
        m_name_l=Label(f1,text="*Mother's name: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_name_l.grid(row=5,column=0,sticky=E)
        m_name_en.grid(row=5,column=1)
        g_name_l=Label(f1,text="*Guardian's name: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        g_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        g_name_l.grid(row=6,column=0,sticky=E)
        g_name_en.grid(row=6,column=1)
        st_ID_l=Label(f1,text="*Enter ID: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_ID_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_ID_l.grid(row=7,column=0,sticky=E)
        st_ID_en.grid(row=7,column=1)
        st_enroll_l=Label(f1,text="*Enrollment No.: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_enroll_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_enroll_l.grid(row=8,column=0,sticky=E)
        st_enroll_en.grid(row=8,column=1)
        st_mob_l=Label(f1,text="*Enter Mob. No.: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_mob_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_mob_l.grid(row=9,column=0,sticky=E)
        st_mob_en.grid(row=9,column=1)
        st_email_l=Label(f1,text="*Enter Email: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_email_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_email_l.grid(row=10,column=0,sticky=E)
        st_email_en.grid(row=10,column=1)
        st_dob_l=Label(f1,text="*D.O.B.: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_dob_en=DateEntry(f1,selectmode='day',date_pattern='dd-MM-yyyy',width=20,mindate=date(1965,1,1),maxdate=date(2006,12,31))
        st_dob_l.grid(row=11,column=0,sticky=E)
        st_dob_en.grid(row=11,column=1)
        st_12_l=Label(f1,text="*12th Passing Year: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_12_en=ttk.Combobox(f1,state="readonly",values=year12,width=20)
        st_12_l.grid(row=12,column=0,sticky=E)
        st_12_en.grid(row=12,column=1)
        st_10_l=Label(f1,text="*10th Passing Year: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_10_en=ttk.Combobox(f1,state="readonly",values=year10,width=20)
        st_10_l.grid(row=13,column=0,sticky=E)
        st_10_en.grid(row=13,column=1)
        st_b_group_l=Label(f1,text="*Enter Blood Group: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_b_group_en=ttk.Combobox(f1,state="readonly",values=["A+","A-","AB+","AB-","B+","B-","O+","O-"],width=20)
        st_b_group_l.grid(row=14,column=0,sticky=E)
        st_b_group_en.grid(row=14,column=1)
        
        st_pwd_l=Label(f1,text="*PwD: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_pwd_en=ttk.Combobox(f1,state="readonly",values=["Yes","No"],width=20)
        st_pwd_l.grid(row=15,column=0,sticky=E)
        st_pwd_en.grid(row=15,column=1)
        st_pwd_cat_l=Label(f1,text="Enter Disability : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_pwd_cat_en=Text(f1,width=17,height=2,highlightbackground="grey",highlightthickness=1,bd=0)

        st_address_l=Label(f2,text="*Address : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        st_address_en=Text(f2,width=17,height=3,font="Calibri",highlightbackground="grey",highlightthickness=1,bd=0)
        st_address_l.grid(row=0 ,column=0,sticky=E)
        st_address_en.grid(row=0,column=1)

        marks_12=Label(f2,text="*Enter 12th Percentage : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        marks_12_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        marks_12.grid(row=1,column=0,sticky=E)
        marks_12_en.grid(row=1,column=1)
        l_per=Label(f2,text="%",bg="white",font="Arial 10 bold")
        l_per.grid(row=1,column=2)

        marks_10=Label(f2,text="*Enter 10th Percentage : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        marks_10_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        marks_10.grid(row=2,column=0,sticky=E)
        marks_10_en.grid(row=2,column=1)
        l_per2=Label(f2,text="%",bg="white",font="Arial 10 bold")
        l_per2.grid(row=2,column=2)

        nationality=Label(f2,text="*Nationality : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        nationality_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        nationality.grid(row=3,column=0,sticky=E)
        nationality_en.grid(row=3,column=1)

        aadhar=Label(f2,text="Enter Aadhar Number : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        aadhar_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        aadhar.grid(row=4,column=0,sticky=E)
        aadhar_en.grid(row=4,column=1)

        gender_l=Label(f2,text="*Gender: ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        gender_en=ttk.Combobox(f2,state="readonly",values=["Male","Female","Others"],width=20)
        gender_l.grid(row=5,column=0,sticky=E)
        gender_en.grid(row=5,column=1)

        f_qualification=Label(f2,text="Enter Father's Qualification : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_qualification_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_qualification.grid(row=6,column=0,sticky=E)
        f_qualification_en.grid(row=6,column=1)

        m_qualification=Label(f2,text="Enter Mother's Qualification : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_qualification_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_qualification.grid(row=7,column=0,sticky=E)
        m_qualification_en.grid(row=7,column=1)

        f_occupation=Label(f2,text="Enter Father's Occupation : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_occupation_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_occupation.grid(row=8,column=0,sticky=E)
        f_occupation_en.grid(row=8,column=1)

        m_occupation=Label(f2,text="Enter Mother's Occupation : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_occupation_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_occupation.grid(row=9,column=0,sticky=E)
        m_occupation_en.grid(row=9,column=1)

        f_mob=Label(f2,text="Father's Mobile Number : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_mob.grid(row=10,column=0,sticky=E)
        f_mob_en.grid(row=10,column=1)

        m_mob=Label(f2,text="Mother's Mobile Number : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_mob.grid(row=11,column=0,sticky=E)
        m_mob_en.grid(row=11,column=1)
        
        alt_mob=Label(f2,text="Alternate Mobile Number : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        alt_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        alt_mob.grid(row=12,column=0,sticky=E)
        alt_mob_en.grid(row=12,column=1)

        alt_email=Label(f2,text="Alternate Email : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        alt_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        alt_email.grid(row=13,column=0,sticky=E)
        alt_email_en.grid(row=13,column=1)

        f_email=Label(f2,text="Father's Email : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_email.grid(row=14,column=0,sticky=E)
        f_email_en.grid(row=14,column=1)

        m_email=Label(f2,text="Mother's Email : ",bg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_email.grid(row=15,column=0,sticky=E)
        m_email_en.grid(row=15,column=1)

        label_astrick=Label(f2,text="* to be filled neccesserily",font="Arial 10 italic",bg="white")
        label_astrick.grid(row=16,column=0,columnspan=2)

        data=[name_entry,course_selector,sem_entry,year_entry,f_name_en,m_name_en,g_name_en,st_ID_en,st_enroll_en,st_mob_en,st_email_en,st_dob_en,st_12_en,st_10_en,st_b_group_en,st_address_en,marks_12_en,marks_10_en,nationality_en,gender_en]

        data2=[aadhar_en,f_qualification_en,m_qualification_en,f_occupation_en,m_occupation_en,f_mob_en,m_mob_en,alt_mob_en,alt_email_en,f_email_en,m_email_en]

        st_submit_btn=Button(a_root,text="Submit",cursor="target",command=lambda:self.get_st_data(a_root,data,data2,st_pwd_en,st_pwd_cat_en,mes))
        st_submit_btn.pack()

        mes=Label(a_root,text="",bg="white")
        mes.pack()

        

        back_btn=Button(a_root,text="Back",cursor="target",command=lambda:[self.adm_functions(a_root),f1.destroy(),f2.destroy()])
        back_btn.pack()

        st_pwd_en.bind("<<ComboboxSelected>>",lambda event :appear(event,st_pwd_cat_l,st_pwd_cat_en,st_pwd_en.get()))

    def get_st_data(self,a_root,data,data2,st_pwd_en,st_pwd_cat_en,mes):
        pwd=""
        id=-1
        mob=0
        if st_pwd_en.get()=="Yes":
            pwd=pwd+st_pwd_cat_en.get("1.0","end-1c")
        l=[]
        for i in data:
            try:
                if(i.get()==""):
                    mes.config(text="Enter * fields",fg="red")
                    return
                l.append(i.get())
            except:
                if(i.get("1.0","end-1c")==""):
                    mes.config(text="Enter * fields",fg="red")
                    return
                l.append(i.get("1.0","end-1c"))
        l.insert(16,st_pwd_en.get())
        l.insert(17,pwd)
        for i in data2:
            x=i.get()
            if(x==""):
                x=None
            l.append(x)
        try:
            sem=int(l[2])
            id=int(l[7])
              #16,17,20,25,26,27,
            mob=int(l[9])
            if(l[22]!=None):
                adhar=int(l[22])
            if(l[27]!=None):
                F_no=int(l[27])
                if(len(str(F_no)) != 10):
                    mes.config(text="Invalid Father's Mobile Number",fg="red")
                    return
            if(l[28]!=None):
                M_no=int(l[28])
                if(len(str(M_no)) != 10):
                    mes.config(text="Invalid Mohter's Mobile Number",fg="red")
                    return
            if(l[29]!=None):
                alt_no=int(l[29])
                if(len(str(alt_no)) != 10):
                    mes.config(text="Invalid Alternate Mobile Number",fg="red")
                    return
        except:
            mes.config(text="Invalid Entry!!",fg="red")
        if(len(str(mob)) != 10):
             mes.config(text="Invalid Mobile Number",fg="red")
             return
        dob=l[11][6:]+'-'+l[11][3:5]+'-'+l[11][0:2]
        l[11]=dob
        
        l=tuple(l)



        global mydb
        cursor=mydb.cursor()
        cursor.execute("select st_ID from student_details")
        i=cursor.fetchall()
        j=(int(l[7]),)
        if(j in i):
            mes.config(text="ID already present",fg="red")
            return
        query="insert into student_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,l)

        query="insert into student_gen values(%s,%s,%s)";
        val=(id,l[0],l[10])
        cursor.execute(query,val)

        query="insert into attendance values(%s,%s,%s)";
        val=(id,0,0)
        cursor.execute(query,val)

        query="insert into scholarship (s_ID) values(%s);";
        val=(id)
        cursor.execute(query,val)

        query="insert into activity (s_Id,s_name) values(%s,%s);";
        val=(id,l[0])
        cursor.execute(query,val)

        try:
            send_st_otp(l[10],id,l[0])
        except Exception as e:
            print(e)
            mes.config(text="No internet!!",fg="red")
            return
        
        mydb.commit()
        mes.config(text="Data set",fg="green")


    def delete_student(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Delete Student Record",font=(sh_font),bg="white")
        head_l.pack(pady=(80,10))
        del_f=Frame(a_root,bg="white")
        del_f.pack()
        
        st_id=Label(del_f,text="Enter Student ID: ",font="Arial 10 bold",justify="right",anchor="e",bg="white")
        st_id.grid(row=0,column=0,sticky=E)

        st_id_en=Entry(del_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_id_en.grid(row=0,column=1,pady=80)

        mes_box=Label(del_f,text="",bg="white")
        mes_box.grid(row=1,column=0,columnspan=2)
        sub_btn=Button(del_f,text="Submit",cursor="target",command=lambda:self.final_delete(a_root,st_id_en.get(),mes_box))
        sub_btn.grid(row=2,column=0,columnspan=2)

        back_btn=Button(a_root,text="Back",cursor="target",command=lambda:self.adm_functions(a_root))
        back_btn.pack(pady=40)

    def final_delete(self,a_root,entered_id,mes):
        if(entered_id==""):
            mes.config(text="Enter ID!!",fg="red")
            return
        global mydb
        s_ID=[]
        query='select st_ID from student_details'
        cursor=mydb.cursor()
        cursor.execute(query)
        for i in cursor:
            s_ID.append(i[0])
        x=0
        a=""
        try:
            x=int(entered_id)
        except:
            mes.config(text="Wrong Format!!",fg="red")
        else:
            if(x in s_ID):
                query="select st_name from student_details where st_ID=%s"
                args=(entered_id,)
                cursor.execute(query,args)
                l=cursor.fetchone()
                a=messagebox.askquestion("Delete Record",f"You want to delete student {l[0]}?",icon="warning")
                mes.config(text="")
            else:
                mes.config(text="ID doesn't exist!!",fg="red")
        if(a=="yes"):
            query1="delete from student_details where st_ID=%s"
            query2="delete from student_gen where id=%s"
            query3="delete from student where st_id=%s"
            args=(x,)
            cursor.execute(query1,args)
            cursor.execute(query2,args)
            cursor.execute(query3,args)
            mydb.commit()
            mes.config(text="Record Deleted!!",fg="green")
        
    def add_result(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Upload Student Result",font=(sh_font),bg="white")
        head_l.pack(pady=(80,0))

        f1=Frame(a_root,bg="white")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="white")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=10)
        name_label=Label(f1,text="Enter Student Name: ",font="Arial 10 bold",bg="white")
        name_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        name_label.grid(row=1,column=0)
        name_entry.grid(row=1,column=1,pady=10)
        sem_label=Label(f1,text="Enter Semester: ",font="Arial 10 bold",bg="white")
        sem_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        sem_label.grid(row=2,column=0)
        sem_entry.grid(row=2,column=1,pady=10)
        
        x=[]
        y=[]
        f2=Frame(a_root,bg="#fdfdfd")
        f2.pack()
        for i in range(1,6):
            lab=Label(f2,text=f"Subject {i}: ",bg="#fdfdfd").grid(row=0,column=i-1,padx=10,pady=(20,5))
            sub_label=Label(f2,text=f"Code: ",bg="#fdfdfd").grid(row=1,column=i-1)
            sub_ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
            sub_ent.grid(row=2,column=i-1,padx=10)
            en_lab=Label(f2,text="Grade: ",bg="#fdfdfd").grid(row=3,column=i-1)
            ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
            ent.grid(row=4,column=i-1,padx=10,pady=(0,0))
            y.append(sub_ent)
            x.append(ent)
        f3=Frame(a_root,bg="white")
        f3.pack()
        cgpa_label=Label(f3,text="Enter CGPA: ",bg="white")
        cgpa_entry=Entry(f3,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
        cgpa_label.grid(row=0,column=0)
        cgpa_entry.grid(row=0,column=1,pady=15)
        z=[id_entry,name_entry,sem_entry,cgpa_entry]
        sub_bt=Button(a_root,text="Submit",cursor="target",command=lambda:self.upload_result(a_root,mes,id_entry.get(),name_entry.get(),sem_entry.get(),cgpa_entry.get(),x,y))
        sub_bt.pack(pady=(20,0))
        mes=Label(a_root,text="",bg="white")
        mes.pack()
        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack()

    def upload_result(self,a_root,mess,sID,sName,sem,cgpa,a,b):
        if(sID=="" or sName=="" or cgpa=="" or sem==""):
            mess.config(text="Fill all fields!!",fg="red")
            return
        global mydb
        cursor=mydb.cursor()
        cursor.execute('select s_ID,semester from marks')
        t1=cursor.fetchall()
        cursor.execute('select st_ID from student_details')
        temp=cursor.fetchall()
        ids=[]
        for i in temp:
            ids.append(i[0])
        try:
            sID=int(sID)
            sem=int(sem)
        except:
            mess.config(text="Invalid Entry!!",fg="red")
            return
        if sID not in ids:
            mess.config(text="Invalid ID!!",fg="red")
            return
        t2=(sID,sem)
        if(t2 in t1):
            mess.config(text="Result Already Uploaded",fg="red")
            return
        cursor=mydb.cursor()
        cursor.execute('select st_name from student_details')
        temp=cursor.fetchall()
        names=[]
        for i in temp:
            names.append(i[0])
        if(sName not in names):
            mess.config(text="Enter Correct Name!!",fg="red")
            return
        cursor.execute('insert into marks (s_ID,s_name) values (%s,%s)',(sID,sName))
        sub=[]
        marks=[]
        for i in range(0,len(a)):
            marks.append(a[i].get())
            sub.append(b[i].get())
            if(a[i].get()=="" or b[i].get()==""):
                mess.config(text="Fill all fields!!",fg="red")
                return
        sub.append(sID)
        marks.append(sID)
        a=tuple(sub)
        b=tuple(marks)
        cursor.execute('update marks set sub1=%s,sub2=%s,sub3=%s,sub4=%s,sub5=%s where s_ID=%s',a)
        cursor.execute('update marks set grade1=%s,grade2=%s,grade3=%s,grade4=%s,grade5=%s where s_ID=%s',b)
        cursor.execute('update marks set semester=%s,cgpa=%s where s_ID=%s',(sem,cgpa,sID))
        try:
            mydb.commit()
        except:
            mess.config(text="No Internet",fg="red")
        else:
            mess.config(text="Result Uploaded",fg="green")

        
    def upload_attendance(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Upload Student Attendance",font=(sh_font),bg="white")
        head_l.pack(pady=(80,10))

        f1=Frame(a_root,bg="white")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="white")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)
        mes=Label(f1,text="",fg="red",bg="white")
        mes.grid(row=1,column=0,columnspan=2)

        sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.uploading_attendance(a_root,id_entry.get(),mes))
        sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack()

    def uploading_attendance(self,a_root,entered_ID,mes):
        if(entered_ID==""):
            mes.config(text="Enter ID")
            return
        try:
            entered_ID=int(entered_ID)
        except:
            mes.config(text="Invalid ID format")
            return
        global mydb
        query="select st_ID from student_details"
        l=[]
        cursor=mydb.cursor()
        cursor.execute(query)
        x=cursor.fetchall()
        for i in x:
            l.append(i[0])
        if(entered_ID not in l):
            mes.config(text="ID not present")
            return
        for i in a_root.slaves():
            i.destroy()
        cursor.execute("select st_name from student_details where st_ID=%s",(entered_ID,))
        s_name=cursor.fetchone()
        s_name=s_name[0]
        h1=Label(a_root,text=f"Upload Attendance of {s_name}",font=(sh_font),bg="white")
        h1.pack(pady=10)
        cursor.execute("select total_days, present from attendance where s_ID=%s",(entered_ID,))
        temp=cursor.fetchone()
        total,present=temp
        add_f=Frame(a_root,bg="#fdfdfd")
        add_f.pack(pady=40)
        total_label=Label(add_f,text="Total Classes (last week): ",bg="#fdfdfd")
        total_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        total_label.grid(row=0,column=0)
        total_entry.grid(row=0,column=1,pady=10)
        attendend_label=Label(add_f,text="Classes Attended: ",bg="#fdfdfd")
        attendend_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        attendend_label.grid(row=1,column=0)
        attendend_entry.grid(row=1,column=1,pady=10)

        submit_btn=Button(a_root,text="Submit",command=lambda:self.update_attendance(entered_ID,int(total)+int(total_entry.get()),int(present)+int(attendend_entry.get()),mes_box))
        submit_btn.pack()

        mes_box=Label(a_root,text="",bg="#fdfdfd",fg="green")
        mes_box.pack(pady=20)

        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack()

    def update_attendance(self,i,t,p,mes_box):
        global mydb
        query="update attendance set total_days=%s,present=%s where s_ID=%s"
        args=(t,p,i)
        cursor=mydb.cursor()
        cursor.execute(query,args)
        mydb.commit()
        mes_box.config(text="Updated")

    def approve_scholarship(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Scholarship",font=(sh_font),bg="white")
        head_l.pack(pady=(80,10))

        f1=Frame(a_root,bg="white")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="white")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)

        sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.checkapplied(id_entry.get(),mes_box))
        sub_bt.grid(row=1,column=0,columnspan=2)

        mes_box=Label(a_root,text="",bg="#fdfdfd",fg="red")
        mes_box.pack()

        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack(pady=40)

    def checkapplied(self,id,mes_box):
        global mydb
        cursor=mydb.cursor()
        cursor.execute("select st_ID from student_details")
        l=[]
        for i in cursor:
            l.append(i[0])
        try:
            id=int(id)
        except:
            mes_box.config(text="Invalid Entry!!",fg="red")
            return
        else:
            if(id not in l):
                mes_box.config(text="ID not Present",fg="red")
            else:
                cursor.execute("select * from scholarship")
                s=cursor.fetchone()
                if s[2]=='no':
                    mes_box.config(text="Student has not applied for scholarship",fg="red")
                else:
                    if(s[3]=='no'):
                        a=messagebox.askquestion("Scholarship",f"Student ID: {s[0]}\nAnnual Income: {s[1]}\nBank Account No.: {s[4]}")
                        if a=='yes':
                            args=('yes',id)
                            cursor.execute("update scholarship set granted=%s where s_ID=%s",args)
                            mydb.commit()
                            mes_box.config(text="Scholarship Granted",fg="green")
                    else:
                        mes_box.config(text="Scholarship Already Granted",fg="green")


adm=Admin()
t=Teacher()
root=Tk()
root.title("Admin")
root.state("zoomed")
root.configure(bg="white")
root.iconbitmap(f"{cwd}\images.ico")
h_font=Font(file="Montserrat-VariableFont_wght.ttf",family="Montserrat",font="Montserrat 40 bold")
sh_font=h_font.copy()
sh_font.config(size=20)
bg=PhotoImage(file=f"{cwd}\~bg.png")
bg_lab=Label(root,image=bg)
bg_lab.place(x=0,y=0)

heading=Label(root,text="MODERATOR MODE\n",font=(h_font),bg="white")
heading.pack(pady=(80,5))
if(True):
    key_entry=Entry(root,width=30,font=100)
    key_entry.insert(0,"Enter Key Here...")
    key_entry.bind("<FocusIn>",on_click)
    key_entry.pack(pady=20)
    submit_btn=Button(root,text="Submit",cursor="target",command=lambda:adm.otp_section(root,key_entry.get(),m_label))
    # submit_btn=Button(root,text="Submit",cursor="target",command=lambda:adm.adm_functions(root))

    submit_btn.pack(pady=5)
    m_label=Label(root,text="",fg="red",bg="white")
    m_label.pack()
else:
    err_mess=Label(root,text="No Internet",font="Georgia 30",bg="white",fg="red")
    err_mess.pack()

root.mainloop()

try:
    mydb.close()
    server.quit()
except:
    pass