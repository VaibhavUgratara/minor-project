from tkinter import *
from tkextrafont import Font
from fontTools.ttLib import TTFont
import os
import mysql.connector as sqltor
from tkinter import *
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
import random
import smtplib
import ssl
from email.message import EmailMessage
from tkinter import messagebox
from tkinter.simpledialog import askstring
import time

cwd=os.getcwd()+"\icons_minor_project"
root=Tk()
root.state("zoomed")
root.title("Student Data Manager")
root.iconbitmap(f"{cwd}\images.ico")
sc_img=PhotoImage(file=f"{cwd}\~button_scholarship.png")
ac_img=PhotoImage(file=f"{cwd}\~button_activity.png")
ma_img=PhotoImage(file=f"{cwd}\~button_marks.png")
ad_img=PhotoImage(file=f"{cwd}\~button_attendance.png")
home_img=PhotoImage(file=f"{cwd}\~button_marks.png")
logut_img=PhotoImage(file=f"{cwd}\~button_attendance.png")
mydb=sqltor.connect(host="localhost",user="root",password="root",database="test")
flag=True


h_font=Font(file="Montserrat-VariableFont_wght.ttf",family="Montserrat",font="Montserrat 40 bold")
# sh_font="Montserrat 20"
# sh_font=h_font.copy()
# sh_font.config(size=20)

def show_pass(btn,pass_entry):
    if(pass_entry['show']=="●"):
        btn.configure(text="🙉",fg="green")
        pass_entry.configure(show="")
    else:
        btn.configure(text="🙈",fg="red")
        pass_entry.configure(show="●")

try:
    global sender,server
    sender="bbaustudentmanager@outlook.com"
    server=smtplib.SMTP('smtp-mail.outlook.com',587)
    server.starttls()
    server.login(sender,"BBAUsatelliteManager")
except:
        flag=False
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
def minorproject(root):

    # flag=True
    # server=""
    # sender="bbaustudentmanager@outlook.com"
    # from tkextrafont import Font
    sh_font=h_font.copy()
    sh_font.config(size=30)

    n1_font=sh_font.copy()
    n1_font.config(size=10)
    n2_font=sh_font.copy()
    n2_font.config(weight='normal',size=10)
    def send_otp(recipient,otp,name,messg=" your OTP is: "):
        try:
            trycon()
            global sender
            global server
            message=name+messg+str(otp)+"."
            email = EmailMessage()
            email["From"] = sender
            email["To"] = recipient
            email["Subject"] = "Student OTP"
            email.set_content(message)
            server.sendmail(sender,recipient,email.as_string())
        except:
            raise Exception("No Internet")


    class Student:
        def catch_data(self):
            global mydb
            self.id=[]
            self.name=[]
            self.passwd=[]
            self.e_mail=[]
            query='select * from student'
            cursor=mydb.cursor()
            cursor.execute(query)
            l=cursor.fetchall()
            for i in l:
                self.id+=i[0],
                self.name+=i[1],
                self.passwd+=i[2],
                self.e_mail+=i[3],
            query="select * from student_gen"
            cursor.execute(query)
            l=cursor.fetchall()
            self.present_id=[]
            self.name_of_student=[]
            self.email_of_student=[]
            for i in l:
                self.present_id+=i[0],
                self.name_of_student+=i[1],
                self.email_of_student+=i[2],

        def check_passwd(self,db,st_root,ID,Passwd,CaptchaEntered,CaptchaShown,mes_box,forget_pass_btn):
            self.catch_data()
            try:
                ID=int(ID)
            except:
                mes_box.configure(text="Invalid ID")
            else:
                if ID in self.id:
                    x=self.id.index(ID)
                    if Passwd==self.passwd[x]:
                        if CaptchaShown==CaptchaEntered:
                            for i in st_root.slaves():
                                i.destroy()
                            self.fetch_student(ID,st_root)
                        else:
                            mes_box.configure(text="Incorrect Captcha")
                            forget_pass_btn.forget()
                    else:
                        mes_box.configure(text="Incorrect Password")
                        forget_pass_btn.pack(pady=5)
                else:
                    if ID in self.present_id:
                        mes_box.configure(text="Password not generated.")
                    else:
                        mes_box.configure(text="Invalid ID")
                    forget_pass_btn.forget()

        def fetch_student(self,st_id,st_root):
            global mydb
            query="select * from student_details where st_ID=%s"
            args=(st_id,)
            cursor=mydb.cursor()
            cursor.execute(query,args)
            l=cursor.fetchall()
            l=l[0]
            l1=Label(st_root,text=f"Welcome {l[0]}",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,0))


            menu_frame=Frame(st_root,bg="#fdfdfd")
            menu_frame.place(x=0,y=250)



            st_f=Frame(st_root,bg="#fdfdfd")
            # st_f.pack()
            st_f.place(x=300,y=150)

            st_f2=Frame(st_root,bg="#fdfdfd")
            st_f2.place(x=700,y=150)

            st_f3=Frame(st_root,bg="#fdfdfd")
            st_f3.place(x=400,y=580)

            course_label=Label(st_f,text=f"Course:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            course=Label(st_f,text=f" {l[1]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            course_label.grid(row=0,column=0,sticky="e")
            course.grid(row=0,column=1,sticky="w")

            sem_label=Label(st_f,text=f"Semester:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            sem=Label(st_f,text=f" {l[2]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            
            sem_label.grid(row=1,column=0,sticky="e")
            sem.grid(row=1,column=1,sticky="w")

            year_label=Label(st_f,text=f"Year:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            year=Label(st_f,text=f" {l[3]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            year_label.grid(row=2,column=0,sticky="e")
            year.grid(row=2,column=1,sticky="w")

            f_name_label=Label(st_f,text=f"Father's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_name=Label(st_f,text=f" {l[4]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_name_label.grid(row=3,column=0,sticky="e")
            f_name.grid(row=3,column=1,sticky="w")

            m_name_label=Label(st_f,text=f"Mother's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_name=Label(st_f,text=f" {l[5]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_name_label.grid(row=4,column=0,sticky="e")
            m_name.grid(row=4,column=1,sticky="w")

            g_name_label=Label(st_f,text=f"Guardian's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            g_name=Label(st_f,text=f" {l[6]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            g_name_label.grid(row=5,column=0,sticky="e")
            g_name.grid(row=5,column=1,sticky="w")

            St_id_label=Label(st_f,text=f"Student ID:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            St_id=Label(st_f,text=f" {l[7]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            St_id_label.grid(row=6,column=0,sticky="e")
            St_id.grid(row=6,column=1,sticky="w")

            St_enroll_label=Label(st_f,text=f"Enrollment Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            St_enroll=Label(st_f,text=f" {l[8]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            St_enroll_label.grid(row=7,column=0,sticky="e")
            St_enroll.grid(row=7,column=1,sticky="w")

            mob_no_label=Label(st_f,text=f"Mobile Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            mob_no=Label(st_f,text=f" {l[9]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            mob_no_label.grid(row=8,column=0,sticky="e")
            mob_no.grid(row=8,column=1,sticky="w")

            email_ID_label=Label(st_f,text=f"Email ID:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            email_ID=Label(st_f,text=f" {l[10]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            email_ID_label.grid(row=9,column=0,sticky="e")
            email_ID.grid(row=9,column=1,sticky="w")

            x=l[11]
            x=str(x)
            x=x[8:]+'-'+x[5:7]+'-'+x[0:4]
            dob_label=Label(st_f,text=f"D.O.B.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            dob=Label(st_f,text=f" {x}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            dob_label.grid(row=10,column=0,sticky="e")
            dob.grid(row=10,column=1,sticky="w")

            pass_12_label=Label(st_f,text=f"12th Passing Year:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            pass_12=Label(st_f,text=f" {l[12]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            pass_12_label.grid(row=11,column=0,sticky="e")
            pass_12.grid(row=11,column=1,sticky="w")

            pass_10_label=Label(st_f,text=f"10th Passing Year:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            pass_10=Label(st_f,text=f" {l[13]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            pass_10_label.grid(row=12,column=0,sticky="e")
            pass_10.grid(row=12,column=1,sticky="w")

            b_grp_label=Label(st_f,text=f"Blood Group:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            b_grp=Label(st_f,text=f" {l[14]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            b_grp_label.grid(row=13,column=0,sticky="e")
            b_grp.grid(row=13,column=1,sticky="w")

            address_label=Label(st_f,text=f"Address:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            address=Label(st_f,text=f" {l[15]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            address_label.grid(row=14,column=0,sticky="e")
            address.grid(row=14,column=1,sticky="w")

            pwd_label=Label(st_f,text=f"Is PwD?:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            pwd=Label(st_f,text=f" {l[16]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            pwd_label.grid(row=15,column=0,sticky="e")
            pwd.grid(row=15,column=1,sticky="w")

            if(l[16]=="Yes"):
                dis_label=Label(st_f2,text=f"Disability:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
                dis=Label(st_f2,text=f" {l[17]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
                dis_label.grid(row=14,column=0,sticky="e")
                dis.grid(row=14,column=1,sticky="w")
            
            per_12_label=Label(st_f2,text=f"12th Percentage:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            per_12=Label(st_f2,text=f" {l[18]}%",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            per_12_label.grid(row=15,column=0,sticky="e")
            per_12.grid(row=15,column=1,sticky="w")

            per_10_label=Label(st_f2,text=f"10th Percentage:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            per_10=Label(st_f2,text=f" {l[19]}%",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            per_10_label.grid(row=16,column=0,sticky="e")
            per_10.grid(row=16,column=1,sticky="w")

            nationality_label=Label(st_f2,text=f"Nationality:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            nationality=Label(st_f2,text=f" {l[20]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            nationality_label.grid(row=17,column=0,sticky="e")
            nationality.grid(row=17,column=1,sticky="w")

            gender_label=Label(st_f2,text=f"Gender:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            gender=Label(st_f2,text=f" {l[21]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            gender_label.grid(row=18,column=0,sticky="e")
            gender.grid(row=18,column=1,sticky="w")

            aadhar_label=Label(st_f2,text=f"Aadhar Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            aadhar=Label(st_f2,text=f" {l[22]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            aadhar_label.grid(row=19,column=0,sticky="e")
            aadhar.grid(row=19,column=1,sticky="w")

            f_qual_label=Label(st_f2,text=f"Father's Qualification:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_qual=Label(st_f2,text=f" {l[23]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_qual_label.grid(row=20,column=0,sticky="e")
            f_qual.grid(row=20,column=1,sticky="w")

            m_qual_label=Label(st_f2,text=f"Mother's Qualification:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_qual=Label(st_f2,text=f" {l[24]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_qual_label.grid(row=21,column=0,sticky="e")
            m_qual.grid(row=21,column=1,sticky="w")

            f_occ_label=Label(st_f2,text=f"Father's Occcupation:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_occ=Label(st_f2,text=f" {l[25]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_occ_label.grid(row=22,column=0,sticky="e")
            f_occ.grid(row=22,column=1,sticky="w")

            m_occ_label=Label(st_f2,text=f"Mother's Occcupation:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_occ=Label(st_f2,text=f" {l[26]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_occ_label.grid(row=23,column=0,sticky="e")
            m_occ.grid(row=23,column=1,sticky="w")

            f_no_label=Label(st_f2,text=f"Father's Mob. No.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_no=Label(st_f2,text=f" {l[27]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_no_label.grid(row=24,column=0,sticky="e")
            f_no.grid(row=24,column=1,sticky="w")

            m_no_label=Label(st_f2,text=f"Mother's Mob. No.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_no=Label(st_f2,text=f" {l[28]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_no_label.grid(row=25,column=0,sticky="e")
            m_no.grid(row=25,column=1,sticky="w")

            alt_no_label=Label(st_f2,text=f"Alternate Mob. No.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            alt_no=Label(st_f2,text=f" {l[29]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            alt_no_label.grid(row=26,column=0,sticky="e")
            alt_no.grid(row=26,column=1,sticky="w")

            alt_email_label=Label(st_f2,text=f"Alternate Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            alt_email=Label(st_f2,text=f" {l[30]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            alt_email_label.grid(row=27,column=0,sticky="e")
            alt_email.grid(row=27,column=1,sticky="w")

            f_email_label=Label(st_f2,text=f"Father's Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_email=Label(st_f2,text=f" {l[31]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_email_label.grid(row=28,column=0,sticky="e")
            f_email.grid(row=28,column=1,sticky="w")

            m_email_label=Label(st_f2,text=f"Mother's Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_email=Label(st_f2,text=f" {l[32]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_email_label.grid(row=29,column=0,sticky="e")
            m_email.grid(row=29,column=1,sticky="w")


            Scholarship_btn=Button(st_f3,image=sc_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.scholarship(l[7]))
            Scholarship_btn.grid(row=0,column=0)
            Activity_btn=Button(st_f3,image=ac_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.activity(l[7]))
            Activity_btn.grid(row=0,column=1,padx=60)

            Marks_btn=Button(st_f3,image=ma_img,activebackground="white",cursor="target",border=0,background="white")
            Marks_btn.grid(row=0,column=2)
            Attendance_btn=Button(st_f3,image=ad_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.check_attendance(l[7]))
            Attendance_btn.grid(row=0,column=3,padx=60)

        
        def activity(self,id):
            ac_root=Tk()
            ac_root.iconbitmap(f"{cwd}\images.ico")
            ac_root.geometry("400x100")
            ac_root.resizable(False,False)
            ac_root.title("Activity")
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select club1,club2,club3,applied,granted from activity where s_ID=%s",(id,))
            temp=cursor.fetchone()
            c1,c2,c3,applied,granted=temp

            if(applied=='no'):
                ac_frame=Frame(ac_root)
                ac_frame.pack()
                club1_label=Label(ac_frame,text="Enter First Club: ")
                club2_label=Label(ac_frame,text="Enter Second Club: ")
                club3_label=Label(ac_frame,text="Enter Third Club: ")
                club1_entry=Entry(ac_frame)
                club2_entry=Entry(ac_frame)
                club3_entry=Entry(ac_frame)
                club1_label.grid(row=0,column=0)
                club2_label.grid(row=1,column=0)
                club3_label.grid(row=2,column=0)
                club1_entry.grid(row=0,column=1)
                club2_entry.grid(row=1,column=1)
                club3_entry.grid(row=2,column=1)
                apply_btn=Button(ac_root,text="Apply",command=lambda:self.activity_applied(ac_root,ac_frame,club1_entry.get(),club2_entry.get(),club3_entry.get(),id,apply_btn))
                apply_btn.pack()
            else:
                if(granted=='no'):
                    ac_label=Label(ac_root,text="Applied Waiting for approval.")
                    ac_label.pack(pady=20)
                else:
                    ac_label=Label(ac_root,text=f"Your Clubs:\n1.          {c1}\n2.           {c2}\n3.            {c3}")
                    ac_label.pack()

        def activity_applied(self,ac_root,frame,c1,c2,c3,id,a_btn):
            a_btn.destroy()
            frame.destroy()
            global mydb
            cursor=mydb.cursor()
            args=(c1,c2,c3,'yes',id)
            cursor.execute("update activity set club1=%s,club2=%s,club3=%s,applied=%s where s_ID=%s",args)
            try:
                mydb.commit()
            except:
                ac_label=Label(ac_root,text="Something went wrong!",fg="red")
                ac_label.pack()
                btn=Button(ac_root,text="Ok",command=lambda:ac_root.destroy())
                btn.pack()
                return
            ac_label=Label(ac_root,text="Applied Successfully",fg="green")
            ac_label.pack()
            btn=Button(ac_root,text="Ok",command=lambda:ac_root.destroy())
            btn.pack()
        def scholarship(self,ID):
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select applied,granted from scholarship where s_ID=%s",(ID,))
            temp=cursor.fetchone()
            applied,granted=temp
            if(applied=='no'):
                a=askstring('Scholarship','Enter Annual Salary\n(*Note -> Please submit all the required documents in the office)')
                time.sleep(1)
                b=askstring('Scholarship','Enter Bank Account Number\n(*Note -> Please submit all the required documents in the office)')
                args=(a,'yes',b,ID)
                cursor.execute("update scholarship set salary=%s, applied=%s, bank=%s where s_ID=%s",args)
                mydb.commit()
                n=messagebox.showinfo("Scholarship","Applied Successfully!\nWaiting for approval.")
            else:
                if(granted=='no'):
                    a=messagebox.showinfo("Scholarship","Applied Successfully!\nWaiting for approval.")
                else:
                    a=messagebox.showinfo("Scholarship","Congratulations!\nYour Scholarship has been approved.")

        def check_attendance(self,i):
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select total_days, present from attendance where s_ID=%s",(i,))
            temp=cursor.fetchone()
            total,present=temp
            per=round(((present/total)*100),2)
            mes=f"""Classes Attended: {present}\nTotal Classes: {total}\nAttendance: {per}%"""
            a=messagebox.showinfo(title="Attendance",message=mes)
    
        def student_login(self,st_root):
            for i in st_root.slaves():
                i.destroy()
            st_root.title("Student's Section")
            l1=Label(st_root,text="Student Login",font=(sh_font),bg="#fdfdfd")
            l1.pack(pady=(100,40))
            form=Frame(st_root,bg="#fdfdfd")
            form.pack()
            mes1=Label(form,text="Student ID: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            s_id=Entry(form)
            mes1.grid(row=0,column=0,pady=5)
            s_id.grid(row=0,column=1)
            mes2=Label(form,text="  Password: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            passwd=Entry(form,show="●")
            forget_pass_btn=Button(st_root,text="Forgot Password?",cursor="target",command=lambda:self.forget_passwd(st_root))
            show_pass_btn=Button(form,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,passwd))
            mes2.grid(row=1,column=0,pady=5)
            passwd.grid(row=1,column=1)
            show_pass_btn.grid(row=1,column=2,padx=5)
            
            captcha_mes=Label(form,text="Enter Captcha:",bg="#fdfdfd",fg="#000000",font=(n2_font))
            captcha_mes.grid(row=2,column=0)
            captcha_entry=Entry(form)
            captcha_entry.grid(row=2,column=1,pady=5)

            image_cap=ImageCaptcha(width=220,height=80)
            captcha_text=str(random.randint(1001,9999))
            image_cap.write(chars=captcha_text,output=f'{cwd}\~captcha.png')

            img_cap=PhotoImage(file=f'{cwd}\~captcha.png')
            captcha_label=Label(st_root,image=img_cap)
            captcha_label.pack(pady=20)
            sub=Button(st_root,text="Submit",cursor="target",command= lambda: self.check_passwd(mydb,st_root,s_id.get(),passwd.get(),captcha_entry.get(),captcha_text,mes,forget_pass_btn))
            sub.pack(pady=5)
            mes=Label(st_root,text=" ",bg="#fdfdfd",fg="red",font=(n2_font))
            mes.pack(pady=5)
            try_gen_pass=Button(st_root,text="Generate Password?",cursor="target",command=lambda:self.add_student(st_root))
            try_gen_pass.pack(pady=5)
            st_root.mainloop()

        def add_student(self,st_root):
            for i in st_root.slaves():
                i.destroy()
            st_root.title("Student's Section")
            l1=Label(st_root,text="Generate Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            entry_frame=Frame(st_root,bg="#fdfdfd")
            entry_frame.pack()
            id_mes=Label(entry_frame,text="Enter Student ID:",bg="#fdfdfd",fg="#000000",font=(n2_font))
            id_enter=Entry(entry_frame)
            id_mes.grid(row=0,column=0,pady=5)
            id_enter.grid(row=0,column=1)
            st_btn_sp=Label(st_root,text="",bg="#fdfdfd",fg="#000000",font=(n2_font))
            st_btn_sp.pack()
            id_btn=Button(st_root,text="Check ID",cursor="target",command=lambda:self.check_st_id(st_root,entry_frame,id_btn,id_enter.get(),st_btn_sp,label_space,next_btn))
            id_btn.pack(pady=10)
            label_space=Label(st_root,text="or",bg="#fdfdfd",fg="#000000",font=(n2_font))
            label_space.pack()
            next_btn=Button(st_root,text="Try Login?",cursor="target",command=lambda:self.student_login(st_root))
            next_btn.pack(pady=10)


        def check_st_id(self,st_root,form_frame,btn,st_ID,mes_box,l_sp,l_btn):
            self.catch_data()
            k=1
            try:
                st_ID=int(st_ID)
                if st_ID in self.id:
                    mes_box.config(text="Password is already generated.",fg="red")
                    return
            except:
                mes_box.config(text="Invalid ID",fg="red")
                k=0
            if st_ID in self.present_id:
                l_sp.destroy()
                l_btn.destroy()
                index_of_student=self.present_id.index(st_ID)
                mes_box.config(text="")
                gen_pass=Label(form_frame,text="Enter Password:",bg="#fdfdfd",fg="#000000",font=(n2_font))
                gen_pass_entry=Entry(form_frame,show="●")
                show_pass_btn=Button(form_frame,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,gen_pass_entry))
                gen_pass.grid(row=1,column=0,pady=5)
                gen_pass_entry.grid(row=1,column=1)
                show_pass_btn.grid(row=1,column=2)
                btn.destroy()
                new_btn=Button(st_root,text="Generate Password",cursor="target",command=lambda:self.otp_checker(st_root,form_frame,self.email_of_student[index_of_student],self.name_of_student[index_of_student],new_btn,st_ID,gen_pass_entry.get()))
                new_btn.pack(pady=5)
            else:
                if k==1:
                    mes_box.config(text="ID not registered.",fg="red")
            
        def otp_checker(self,st_root,form_frame,st_email,st_name,btn,st_ID,st_pass):
            form_frame.destroy()
            btn.destroy()
            one_time_password=random.randint(1000,9999)
            try:
                send_otp(st_email,one_time_password,st_name)
            except:
                err_frame=Frame(st_root,bg="#fdfdfd")
                mes=Label(err_frame,text="Error!! Check Internet Connection",fg="red",bg="#fdfdfd",font=(n2_font))
                mes.pack(pady=5)
                try_btn=Button(err_frame,text="Try Again",cursor="target",command=lambda:self.add_student(st_root))
                try_btn.pack()
                err_frame.pack()
            else:
                otp_form=Frame(st_root,bg="#fdfdfd")
                otp_form.pack(pady=10)
                otp_enter_mes=Label(otp_form,text="Enter OTP:",bg="#fdfdfd",fg="#000000",font=(n2_font))
                otp_enter_box=Entry(otp_form)
                otp_enter_mes.grid(row=0,column=0,pady=5)
                otp_enter_box.grid(row=0,column=1)
                otp_message=Label(st_root,text="\n\n",bg="#fdfdfd",fg="red",font=(n2_font))
                otp_message.pack()
                otp_submit_btn=Button(st_root,text="Submit",cursor="target",command=lambda:self.otp_verification(st_root,one_time_password,otp_enter_box.get(),otp_message,st_ID,st_name,st_pass,st_email))
                otp_submit_btn.pack(pady=5)

        def otp_verification(self,st_root,otp_gen,otp_enter,message_box,st_ID,st_name,st_pass,st_email):
            try:
                otp_enter=int(otp_enter)
            except:
                message_box.config(text="Invalid OTP")
            else:
                if otp_enter==otp_gen:
                    global mydb
                    cursor=mydb.cursor()
                    query="insert into student values (%s,%s,%s,%s)"
                    args=(st_ID,st_name,st_pass,st_email)
                    cursor.execute(query,args)
                    mydb.commit()
                    query="delete from student_gen where id=(%s)"
                    args=(st_ID,)
                    cursor.execute(query,args)
                    mydb.commit()
                    for i in st_root.slaves():
                        i.destroy()
                    heading=Label(st_root,text="Generate Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
                    heading.pack(pady=(80,10))
                    login_mes=Label(st_root,text="Password Generated Successfully\nClick below to login",bg="#fdfdfd",fg="#000000",font=(n2_font))
                    login_mes.pack()
                    login_btn=Button(st_root,text="Login",cursor="target",command=lambda:self.student_login(st_root))
                    login_btn.pack()
                else:
                    message_box.config(text="Invalid OTP")

        def forget_passwd(self,st_root):
            for i in st_root.slaves():
                i.destroy()
            st_root.title("Student's Section")
            l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            form_frame=Frame(st_root,bg="#fdfdfd")
            form_frame.pack()
            id_label=Label(form_frame,text="Enter ID: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            email_label=Label(form_frame,text="Confirm Email: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            id_input=Entry(form_frame,width=30)
            email_entry=Entry(form_frame,width=30)
            id_label.grid(row=0,column=0,pady=5)
            id_input.grid(row=0,column=1)
            email_label.grid(row=1,column=0,pady=5)
            email_entry.grid(row=1,column=1)
            validate_btn=Button(st_root,text="Verify",command=lambda:self.validate_details(st_root,form_frame,id_input,email_entry,mes,validate_btn),cursor="target")
            validate_btn.pack(pady=10)
            mes=Label(st_root,text="",fg="red",bg="#fdfdfd",font=(n2_font))
            mes.pack()

        def validate_details(self,st_root,form_frame,id_input,email_entry,mes,validate_btn):
            mes.config(text="")
            self.catch_data()
            ID=id_input.get()
            try:
                ID=int(ID)
                ind=self.id.index(ID)
            except:
                mes.config(text="Invalid ID")
            else:
                if(ID in self.id):
                    if(email_entry.get() in self.e_mail):
                        mes.config(text="Details Verified",fg="green")
                        validate_btn.destroy()
                        next_btn=Button(st_root,text="Next",command=lambda:self.forgetpass_otp(st_root,ID,self.e_mail[ind],self.name[ind]),cursor="target")
                        next_btn.pack(pady=5)
                    else:
                        mes.config(text="Incorrect Email")
                else:
                    if(ID in self.present_id):
                        mes.config("Password Not Generated Yet")
                        gen_pass=Button(st_root,text="Generate Password?",command=lambda:self.add_student(st_root))
                        gen_pass.pack()
                    else:
                        mes.config(text="Invalid ID")
        def forgetpass_otp(self,st_root,ID,st_email,st_name):
            for i in st_root.slaves():
                i.destroy()
            l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            new_mes=Label(st_root,text="",fg="red",bg="#fdfdfd",font=(n2_font))
            new_mes.pack(pady=5)
            try:
                otp=random.randint(1001,9999);
                send_otp(st_email,otp,st_name," to reset your password your OTP is: ")
            except:
                new_mes.config(text="Error!! Check Internet Connection")
                back_btn=Button(st_root,text="Back",command=lambda:self.forget_passwd(st_root),cursor="target")
                back_btn.pack()
                return
            else:
                new_form=Frame(st_root,bg="#fdfdfd")
                new_form.pack(pady=5)
                otp_label=Label(new_form,text="Enter OTP: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
                otp_entry=Entry(new_form)
                otp_label.grid(row=0,column=0,pady=5)
                otp_entry.grid(row=0,column=1)
                submit_btn=Button(st_root,text="Submit",cursor="target",command=lambda:self.check_forget_otp(st_root,otp,otp_entry.get(),ID,new_mes))
                submit_btn.pack(pady=5)
                new_mes=Label(st_root,text="",bg="#fdfdfd",fg="red",font=(n2_font))
                new_mes.pack()

        def check_forget_otp(self,st_root,otp,received_otp,ID,mes):
            otp=str(otp)
            if(otp==received_otp):
                for i in st_root.slaves():
                    i.destroy()
                l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
                l1.pack(pady=(80,10))
                new_fr=Frame(st_root,bg="#fdfdfd")
                new_fr.pack()
                new_pass_label=Label(new_fr,text="Enter New Password: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
                new_pass_entry=Entry(new_fr,show="●")
                show_pass_btn=Button(new_fr,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,new_pass_entry))
                new_pass_label.grid(row=0,column=0,pady=5)
                new_pass_entry.grid(row=0,column=1)
                show_pass_btn.grid(row=0,column=2)
                change_btn=Button(st_root,text="Change Password",cursor="target",command=lambda:self.change_passwd(st_root,new_pass_entry.get(),ID,new_mes))
                change_btn.pack(pady=5)
                new_mes=Label(st_root,text="",bg="#fdfdfd",fg="red",font=(n2_font))
                new_mes.pack(pady=5)
            else:
                mes.configure(text="Invalid OTP")

        def change_passwd(self,st_root,new_pass,ID,mes):
            if(new_pass==""):
                mes.configure(text="Enter a password")
                return   
            global mydb
            cursor=mydb.cursor()
            query="update student set st_pass=%s where st_id=%s"
            args=(new_pass,ID)
            cursor.execute(query,args)
            mydb.commit()
            for i in st_root.slaves():
                i.destroy()
            l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            final_label=Label(st_root,text="Password Reset Successful",fg="green",bg="#fdfdfd",font=(n2_font))
            final_label.pack(pady=5)
            login_btn=Button(st_root,text="Click here to login",cursor="target",command=lambda:self.student_login(st_root))
            login_btn.pack(pady=5)
            




    # root=Tk()
    # root.title("Data Manager")
    # root.state("zoomed")
    # root.iconbitmap(f"{cwd}\images.ico")
    # root.wm_attributes('-transparentcolor','#fdfdfd')
    # root.resizable(False,False)
    # root.configure(bg="#fdfdfd")

    for i in root.slaves():
        i.destroy()

    b_g=Image.open(f"{cwd}\~bg.png")
    bg=ImageTk.PhotoImage(b_g)
    bg_lab=Label(root,image=bg)
    bg_lab.place(x=0,y=0)


    f1=Frame(root,bg="#fdfdfd")
    f1.pack(pady=90)
    # space1=Label(f1,text=" ",bg="#fdfdfd")
    # space1.pack()
    heading=Label(f1,text="Student Section",font=(h_font),bg="#fdfdfd",fg="#000000")
    heading.pack()
    f2=Frame(root,bg="#fdfdfd")
    f2.pack()
    student_obj=Student()
    if mydb.is_connected() or (flag):
        login_img=PhotoImage(file=f"{cwd}\~login_button.png")
        student=Button(f2,image=login_img,bg="#fdfdfd",activebackground="#fdfdfd",border="0",cursor="target",command=lambda:student_obj.student_login(root))
        student.pack()

        space2=Label(f2,text="\n\n",bg="#fdfdfd")
        space2.pack()
        gen_pass_img=PhotoImage(file=f"{cwd}\~generate-password_button.png")
        student_pass_generate=Button(f2,image=gen_pass_img,bg="#fdfdfd",activebackground="#fdfdfd",border="0",cursor="target",command= lambda:student_obj.add_student(root))
        student_pass_generate.pack()
        space3=Label(f2,text="\n\n",bg="#fdfdfd")
        space3.pack()

        forget_pass_image=PhotoImage(file=f"{cwd}\~forgot-password_button.png")
        student_forgot_generate=Button(f2,image=forget_pass_image,bg="#fdfdfd",activebackground="#fdfdfd",border="0",cursor="target",command=lambda:student_obj.forget_passwd(root))
        student_forgot_generate.pack()

    else:
        err_message=Label(f1,text="Error!! Not Connected To Internet",bg="#fdfdfd",font=(sh_font),fg="red")
        err_message.pack()

    root.mainloop()
    try:
        server.quit()
        mydb.close()
    except:
        pass


bg=PhotoImage(file=f"{cwd}\~bg.png")


# c_font=Font(file="Montserrat-VariableFont_wght.ttf",family="Montserrat",font="Montserrat 40 bold")


canvas1=Canvas(root,width=400,height=400)
canvas1.pack(fill="both",expand=True)

canvas1.create_image(0,0,image=bg,anchor="nw")

canvas1.create_text(700,120,font=(h_font),text="Student Data Management System")
# canvas1.create_text(700,100,text="Student Data Management System",font=(50))

b1_img=PhotoImage(file=f"{cwd}\~b1.png")
b2_img=PhotoImage(file=f"{cwd}\~b2.png")
b1=Button(root,activebackground="white",image=b1_img,border=0,background="white",command=lambda:[minorproject(root)])
b2=Button(root,activebackground="white",image=b2_img,border=0,background="white")

b1_canvas=canvas1.create_window(675,300,window=b1)
b2_canvas=canvas1.create_window(675,450,window=b2)


root.mainloop()