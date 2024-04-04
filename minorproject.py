import os
import mysql.connector as sqltor
from tkinter import *
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
import random
import smtplib
import ssl
from email.message import EmailMessage

cwd=os.getcwd()+"\icons_minor_project"

mydb=sqltor.connect(host="localhost",user="root",password="root",database="test")
flag=True

def show_pass(btn,pass_entry):
    if(pass_entry['show']=="●"):
        btn.configure(text="🙉",fg="green")
        pass_entry.configure(show="")
    else:
        btn.configure(text="🙈",fg="red")
        pass_entry.configure(show="●")

try:
    sender="bbaustudentmanager@outlook.com"
    server=smtplib.SMTP('smtp-mail.outlook.com',587)
    server.starttls()
    server.login(sender,"BBAUsatelliteManager")
except:
    flag=False


def send_otp(recipient,otp,name,messg=" your OTP is: "):
    try:
        global sender
        global server
        message=name+messg+str(otp)+"."
        email = EmailMessage()
        email["From"] = sender
        email["To"] = recipient
        email["Subject"] = "Your OTP"
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
        l1=Label(st_root,text=f"Welcome {l[0]}",font="Georgia 20",bg="#333333",fg="#efcdfb")
        l1.pack(pady=20)
        st_f=Frame(st_root,bg="#333333")
        # st_f.pack()
        st_f.place(x=300,y=80)

        st_f2=Frame(st_root,bg="#333333")
        st_f2.place(x=700,y=80)

        course_label=Label(st_f,text=f"Course:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        course=Label(st_f,text=f" {l[1]}",bg="#333333",fg="white",justify="left",anchor="w")
        course_label.grid(row=0,column=0,sticky="e")
        course.grid(row=0,column=1,sticky="w",pady=10)

        f_name_label=Label(st_f,text=f"Father's Name:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_name=Label(st_f,text=f" {l[2]}",bg="#333333",fg="white",justify="left",anchor="w")
        f_name_label.grid(row=1,column=0,sticky="e")
        f_name.grid(row=1,column=1,sticky="w",pady=10)

        m_name_label=Label(st_f,text=f"Mother's Name:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_name=Label(st_f,text=f" {l[3]}",bg="#333333",fg="white",justify="left",anchor="w")
        m_name_label.grid(row=2,column=0,sticky="e")
        m_name.grid(row=2,column=1,sticky="w",pady=10)

        g_name_label=Label(st_f,text=f"Guardian's Name:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        g_name=Label(st_f,text=f" {l[4]}",bg="#333333",fg="white",justify="left",anchor="w")
        g_name_label.grid(row=3,column=0,sticky="e")
        g_name.grid(row=3,column=1,sticky="w",pady=10)

        St_id_label=Label(st_f,text=f"Student ID:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        St_id=Label(st_f,text=f" {l[5]}",bg="#333333",fg="white",justify="left",anchor="w")
        St_id_label.grid(row=4,column=0,sticky="e")
        St_id.grid(row=4,column=1,sticky="w",pady=10)

        St_enroll_label=Label(st_f,text=f"Enrollment Number:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        St_enroll=Label(st_f,text=f" {l[6]}",bg="#333333",fg="white",justify="left",anchor="w")
        St_enroll_label.grid(row=5,column=0,sticky="e")
        St_enroll.grid(row=5,column=1,sticky="w",pady=10)

        mob_no_label=Label(st_f,text=f"Mobile Number:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        mob_no=Label(st_f,text=f" {l[7]}",bg="#333333",fg="white",justify="left",anchor="w")
        mob_no_label.grid(row=6,column=0,sticky="e")
        mob_no.grid(row=6,column=1,sticky="w",pady=10)

        email_ID_label=Label(st_f,text=f"Email ID:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        email_ID=Label(st_f,text=f" {l[8]}",bg="#333333",fg="white",justify="left",anchor="w")
        email_ID_label.grid(row=7,column=0,sticky="e")
        email_ID.grid(row=7,column=1,sticky="w",pady=10)

        x=l[9]
        x=str(x)
        x=x[8:]+'-'+x[5:7]+'-'+x[0:4]
        dob_label=Label(st_f,text=f"D.O.B.:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        dob=Label(st_f,text=f" {x}",bg="#333333",fg="white",justify="left",anchor="w")
        dob_label.grid(row=8,column=0,sticky="e")
        dob.grid(row=8,column=1,sticky="w",pady=10)

        pass_12_label=Label(st_f,text=f"12th Passing Year:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        pass_12=Label(st_f,text=f" {l[10]}",bg="#333333",fg="white",justify="left",anchor="w")
        pass_12_label.grid(row=9,column=0,sticky="e")
        pass_12.grid(row=9,column=1,sticky="w",pady=10)

        pass_10_label=Label(st_f,text=f"10th Passing Year:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        pass_10=Label(st_f,text=f" {l[11]}",bg="#333333",fg="white",justify="left",anchor="w")
        pass_10_label.grid(row=10,column=0,sticky="e")
        pass_10.grid(row=10,column=1,sticky="w",pady=10)

        b_grp_label=Label(st_f,text=f"Blood Group:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        b_grp=Label(st_f,text=f" {l[12]}",bg="#333333",fg="white",justify="left",anchor="w")
        b_grp_label.grid(row=11,column=0,sticky="e")
        b_grp.grid(row=11,column=1,sticky="w",pady=10)

        address_label=Label(st_f,text=f"Address:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        address=Label(st_f,text=f" {l[13]}",bg="#333333",fg="white",justify="left",anchor="w")
        address_label.grid(row=12,column=0,sticky="e")
        address.grid(row=12,column=1,sticky="w",pady=10)

        pwd_label=Label(st_f,text=f"Is PwD?:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        pwd=Label(st_f,text=f" {l[14]}",bg="#333333",fg="white",justify="left",anchor="w")
        pwd_label.grid(row=13,column=0,sticky="e")
        pwd.grid(row=13,column=1,sticky="w",pady=10)

        if(l[14]=="Yes"):
            dis_label=Label(st_f,text=f"Disability:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
            dis=Label(st_f,text=f" {l[15]}",bg="#333333",fg="white",justify="left",anchor="w")
            dis_label.grid(row=14,column=0,sticky="e")
            dis.grid(row=14,column=1,sticky="w",pady=10)
        
        per_12_label=Label(st_f2,text=f"12th Percentage:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        per_12=Label(st_f2,text=f" {l[16]}%",bg="#333333",fg="white",justify="left",anchor="w")
        per_12_label.grid(row=15,column=0,sticky="e")
        per_12.grid(row=15,column=1,sticky="w",pady=10)

        per_10_label=Label(st_f2,text=f"10th Percentage:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        per_10=Label(st_f2,text=f" {l[17]}%",bg="#333333",fg="white",justify="left",anchor="w")
        per_10_label.grid(row=16,column=0,sticky="e")
        per_10.grid(row=16,column=1,sticky="w",pady=10)

        nationality_label=Label(st_f2,text=f"Nationality:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        nationality=Label(st_f2,text=f" {l[18]}",bg="#333333",fg="white",justify="left",anchor="w")
        nationality_label.grid(row=17,column=0,sticky="e")
        nationality.grid(row=17,column=1,sticky="w",pady=10)

        gender_label=Label(st_f2,text=f"Gender:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        gender=Label(st_f2,text=f" {l[19]}",bg="#333333",fg="white",justify="left",anchor="w")
        gender_label.grid(row=18,column=0,sticky="e")
        gender.grid(row=18,column=1,sticky="w",pady=10)

        aadhar_label=Label(st_f2,text=f"Aadhar Number:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        aadhar=Label(st_f2,text=f" {l[20]}",bg="#333333",fg="white",justify="left",anchor="w")
        aadhar_label.grid(row=19,column=0,sticky="e")
        aadhar.grid(row=19,column=1,sticky="w",pady=10)

        f_qual_label=Label(st_f2,text=f"Father's Qualification:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_qual=Label(st_f2,text=f" {l[21]}",bg="#333333",fg="white",justify="left",anchor="w")
        f_qual_label.grid(row=20,column=0,sticky="e")
        f_qual.grid(row=20,column=1,sticky="w",pady=10)

        m_qual_label=Label(st_f2,text=f"Mother's Qualification:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_qual=Label(st_f2,text=f" {l[22]}",bg="#333333",fg="white",justify="left",anchor="w")
        m_qual_label.grid(row=21,column=0,sticky="e")
        m_qual.grid(row=21,column=1,sticky="w",pady=10)

        f_occ_label=Label(st_f2,text=f"Father's Occcupation:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_occ=Label(st_f2,text=f" {l[23]}",bg="#333333",fg="white",justify="left",anchor="w")
        f_occ_label.grid(row=22,column=0,sticky="e")
        f_occ.grid(row=22,column=1,sticky="w",pady=10)

        m_occ_label=Label(st_f2,text=f"Mother's Occcupation:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_occ=Label(st_f2,text=f" {l[24]}",bg="#333333",fg="white",justify="left",anchor="w")
        m_occ_label.grid(row=23,column=0,sticky="e")
        m_occ.grid(row=23,column=1,sticky="w",pady=10)

        f_no_label=Label(st_f2,text=f"Father's Mob. No.:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_no=Label(st_f2,text=f" {l[25]}",bg="#333333",fg="white",justify="left",anchor="w")
        f_no_label.grid(row=24,column=0,sticky="e")
        f_no.grid(row=24,column=1,sticky="w",pady=10)

        m_no_label=Label(st_f2,text=f"Mother's Mob. No.:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_no=Label(st_f2,text=f" {l[26]}",bg="#333333",fg="white",justify="left",anchor="w")
        m_no_label.grid(row=25,column=0,sticky="e")
        m_no.grid(row=25,column=1,sticky="w",pady=10)

        alt_no_label=Label(st_f2,text=f"Alternate Mob. No.:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        alt_no=Label(st_f2,text=f" {l[27]}",bg="#333333",fg="white",justify="left",anchor="w")
        alt_no_label.grid(row=26,column=0,sticky="e")
        alt_no.grid(row=26,column=1,sticky="w",pady=10)

        alt_email_label=Label(st_f2,text=f"Alternate Email:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        alt_email=Label(st_f2,text=f" {l[28]}",bg="#333333",fg="white",justify="left",anchor="w")
        alt_email_label.grid(row=27,column=0,sticky="e")
        alt_email.grid(row=27,column=1,sticky="w",pady=10)

        f_email_label=Label(st_f2,text=f"Father's Email:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        f_email=Label(st_f2,text=f" {l[29]}",bg="#333333",fg="white",justify="left",anchor="w")
        f_email_label.grid(row=28,column=0,sticky="e")
        f_email.grid(row=28,column=1,sticky="w",pady=10)

        m_email_label=Label(st_f2,text=f"Mother's Email:",bg="#333333",fg="white",font="Arial 10 bold",justify="right",anchor="e")
        m_email=Label(st_f2,text=f" {l[30]}",bg="#333333",fg="white",justify="left",anchor="w")
        m_email_label.grid(row=29,column=0,sticky="e")
        m_email.grid(row=29,column=1,sticky="w",pady=10)



    def student_login(self,st_root):
        for i in st_root.slaves():
            i.destroy()
        st_root.title("Student's Section")
        l1=Label(st_root,text="\nStudent Login\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
        l1.pack()
        form=Frame(st_root,bg="#333333")
        form.pack()
        mes1=Label(form,text="Student ID: ",bg="#333333",fg="white")
        s_id=Entry(form)
        mes1.grid(row=0,column=0,pady=5)
        s_id.grid(row=0,column=1)
        mes2=Label(form,text="  Password: ",bg="#333333",fg="white")
        passwd=Entry(form,show="●")
        forget_pass_btn=Button(st_root,text="Forgot Password?",cursor="target",command=lambda:self.forget_passwd(st_root))
        show_pass_btn=Button(form,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,passwd))
        mes2.grid(row=1,column=0,pady=5)
        passwd.grid(row=1,column=1)
        show_pass_btn.grid(row=1,column=2,padx=5)
        
        captcha_mes=Label(form,text="Enter Captcha:",bg="#333333",fg="white")
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
        mes=Label(st_root,text=" ",bg="#333333",fg="#ff8b71")
        mes.pack(pady=5)
        try_gen_pass=Button(st_root,text="Generate Password?",cursor="target",command=lambda:self.add_student(st_root))
        try_gen_pass.pack(pady=5)
        st_root.mainloop()

    def add_student(self,st_root):
        for i in st_root.slaves():
            i.destroy()
        st_root.title("Student's Section")
        l1=Label(st_root,text="\nGenerate Password\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
        l1.pack()
        entry_frame=Frame(st_root,bg="#333333")
        entry_frame.pack()
        id_mes=Label(entry_frame,text="Enter Student ID:",bg="#333333",fg="white")
        id_enter=Entry(entry_frame)
        id_mes.grid(row=0,column=0,pady=5)
        id_enter.grid(row=0,column=1)
        st_btn_sp=Label(st_root,text="",bg="#333333",fg="white")
        st_btn_sp.pack()
        id_btn=Button(st_root,text="Check ID",cursor="target",command=lambda:self.check_st_id(st_root,entry_frame,id_btn,id_enter.get(),st_btn_sp,label_space,next_btn))
        id_btn.pack(pady=10)
        label_space=Label(st_root,text="or",bg="#333333",fg="white")
        label_space.pack()
        next_btn=Button(st_root,text="Try Login?",cursor="target",command=lambda:self.student_login(st_root))
        next_btn.pack(pady=10)


    def check_st_id(self,st_root,form_frame,btn,st_ID,mes_box,l_sp,l_btn):
        self.catch_data()
        k=1
        try:
            st_ID=int(st_ID)
            if st_ID in self.id:
                mes_box.config(text="Password is already generated.",fg="#ff8b71")
                return
        except:
            mes_box.config(text="Invalid ID",fg="#ff8b71")
            k=0
        if st_ID in self.present_id:
            l_sp.destroy()
            l_btn.destroy()
            index_of_student=self.present_id.index(st_ID)
            mes_box.config(text="")
            gen_pass=Label(form_frame,text="Enter Password:",bg="#333333",fg="white")
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
                mes_box.config(text="ID not registered.",fg="#ff8b71")
        
    def otp_checker(self,st_root,form_frame,st_email,st_name,btn,st_ID,st_pass):
        form_frame.destroy()
        btn.destroy()
        one_time_password=random.randint(1000,9999)
        try:
            send_otp(st_email,one_time_password,st_name)
        except:
            err_frame=Frame(st_root,bg="#f3fac0")
            mes=Label(err_frame,text="Error!! Check Internet Connection",fg="#ff8b71",bg="#333333")
            mes.pack(pady=5)
            try_btn=Button(err_frame,text="Try Again",cursor="target",command=lambda:self.add_student(st_root))
            try_btn.pack()
            err_frame.pack()
        else:
            otp_form=Frame(st_root,bg="#333333")
            otp_form.pack()
            otp_enter_mes=Label(otp_form,text="Enter OTP:",bg="#333333",fg="white")
            otp_enter_box=Entry(otp_form)
            otp_enter_mes.grid(row=0,column=0,pady=5)
            otp_enter_box.grid(row=0,column=1)
            otp_message=Label(st_root,text="\n\n",bg="#333333",fg="#ff8b71")
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
                heading=Label(st_root,text="\nGenerate Password\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
                heading.pack()
                login_mes=Label(st_root,text="Password Generated Successfully\nClick below to login",bg="#333333",fg="#efcdfb")
                login_mes.pack()
                login_btn=Button(st_root,text="Login",cursor="target",command=lambda:self.student_login(st_root))
                login_btn.pack()
            else:
                message_box.config(text="Invalid OTP")

    def forget_passwd(self,st_root):
        for i in st_root.slaves():
            i.destroy()
        st_root.title("Student's Section")
        l1=Label(st_root,text="\nForget Password\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
        l1.pack()
        form_frame=Frame(st_root,bg="#333333")
        form_frame.pack()
        id_label=Label(form_frame,text="Enter ID: ",bg="#333333",fg="white")
        email_label=Label(form_frame,text="Confirm Email: ",bg="#333333",fg="white")
        id_input=Entry(form_frame,width=30)
        email_entry=Entry(form_frame,width=30)
        id_label.grid(row=0,column=0,pady=5)
        id_input.grid(row=0,column=1)
        email_label.grid(row=1,column=0,pady=5)
        email_entry.grid(row=1,column=1)
        validate_btn=Button(st_root,text="Verify",command=lambda:self.validate_details(st_root,form_frame,id_input,email_entry,mes,validate_btn),cursor="target")
        validate_btn.pack(pady=10)
        mes=Label(st_root,text="",fg="#ff8b71",bg="#333333")
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
                    mes.config(text="Details Verified",fg="#c7fa68")
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
        l1=Label(st_root,text="\nForget Password\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
        l1.pack()
        new_mes=Label(st_root,text="",fg="#ff8b71",bg="#333333")
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
            new_form=Frame(st_root,bg="#333333")
            new_form.pack()
            otp_label=Label(new_form,text="Enter OTP: ",bg="#333333",fg="white")
            otp_entry=Entry(new_form)
            otp_label.grid(row=0,column=0,pady=5)
            otp_entry.grid(row=0,column=1)
            submit_btn=Button(st_root,text="Submit",cursor="target",command=lambda:self.check_forget_otp(st_root,otp,otp_entry.get(),ID,new_mes))
            submit_btn.pack(pady=5)
            new_mes=Label(st_root,text="",bg="#333333",fg="#ff8b71")
            new_mes.pack()

    def check_forget_otp(self,st_root,otp,received_otp,ID,mes):
        otp=str(otp)
        if(otp==received_otp):
            for i in st_root.slaves():
                i.destroy()
            l1=Label(st_root,text="\nForget Password\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
            l1.pack()
            new_fr=Frame(st_root,bg="#333333")
            new_fr.pack()
            new_pass_label=Label(new_fr,text="Enter New Password: ",bg="#333333",fg="white")
            new_pass_entry=Entry(new_fr,show="●")
            show_pass_btn=Button(new_fr,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,new_pass_entry))
            new_pass_label.grid(row=0,column=0,pady=5)
            new_pass_entry.grid(row=0,column=1)
            show_pass_btn.grid(row=0,column=2)
            change_btn=Button(st_root,text="Change Password",cursor="target",command=lambda:self.change_passwd(st_root,new_pass_entry.get(),ID,new_mes))
            change_btn.pack(pady=5)
            new_mes=Label(st_root,text="",bg="#333333",fg="#ff8b71")
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
        l1=Label(st_root,text="\nForget Password\n\n",font="Georgia 20",bg="#333333",fg="#efcdfb")
        l1.pack()
        final_label=Label(st_root,text="Password Reset Successful",fg="green",bg="#333333")
        final_label.pack(pady=5)
        login_btn=Button(st_root,text="Click here to login",cursor="target",command=lambda:self.student_login(st_root))
        login_btn.pack(pady=5)
        




root=Tk()
root.title("Data Manager")
root.state("zoomed")
root.iconbitmap(f"{cwd}\images.ico")
# root.resizable(False,False)
root.configure(bg="#333333")
f1=Frame(root,bg="#333333")
f1.pack()
space1=Label(f1,text=" ",bg="#333333")
space1.pack()
heading=Label(f1,text="Student Data Management",font="Georgia 50",bg="#333333",fg="#efcdfb",pady=70)
heading.pack()
f2=Frame(root,bg="#333333")
f2.pack()
student_obj=Student()
if mydb.is_connected() or (flag):
    login_img=PhotoImage(file=f"{cwd}\~login_button.png")
    student=Button(f2,image=login_img,bg="#333333",activebackground="#333333",border="0",cursor="target",command=lambda:student_obj.student_login(root))
    student.pack()

    space2=Label(f2,text="\n\n",bg="#333333")
    space2.pack()
    gen_pass_img=PhotoImage(file=f"{cwd}\~generate-password_button.png")
    student_pass_generate=Button(f2,image=gen_pass_img,bg="#333333",activebackground="#333333",border="0",cursor="target",command= lambda:student_obj.add_student(root))
    student_pass_generate.pack()
    space3=Label(f2,text="\n\n",bg="#333333")
    space3.pack()

    forget_pass_image=PhotoImage(file=f"{cwd}\~forgot-password_button.png")
    student_forgot_generate=Button(f2,image=forget_pass_image,bg="#333333",activebackground="#333333",border="0",cursor="target",command=lambda:student_obj.forget_passwd(root))
    student_forgot_generate.pack()

else:
    err_message=Label(f1,text="Error!! Not Connected To Internet",bg="#333333",font="Georgia 20",fg="#ff8b71")
    err_message.pack()

root.mainloop()
try:
    server.quit()
    mydb.close()
except:
    pass
