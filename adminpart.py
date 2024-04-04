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

cwd=os.getcwd()+"\icons_minor_project"

mydb=sqltor.connect(host="localhost",user="root",password="root",database="test")

key="AXYZ-33#4-231B"

pwd_f=False


def send_st_otp(recipient,ID,name):
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
        st_pwd_cat_l.grid(row=14,column=0,sticky=E)
        st_pwd_cat_en.grid(row=14,column=1,pady=5)
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


def on_click(event):
    global key_entry
    key_entry.delete(0,END)


class Admin:
    
    def otp_section(self,a_root,KEY,mes_lab):
        global key
        KEY=KEY.lstrip()
        if (KEY==""):
            mes_lab.config(text="Enter Key!!")
            return
        elif(KEY!=key):
            mes_lab.config(text="Wrong Key!!")
            return
        c=0
        for i in a_root.slaves():
            if(c==0):
                c+=1
                continue
            i.destroy()
        try:
            OTP=send_otp()
        except:
            n_m=Label(a_root,text="No Internet",fg="red",bg="#eaddfe")
            n_m.pack(pady=10)
            q_btn=Button(a_root,text="Quit",command=a_root.destroy,cursor="target")
            q_btn.pack()
        else:
            f=Frame(a_root,bg="#eaddfe")
            f.pack()
            otp_Label=Label(f,text="Enter OTP: ",bg="#eaddfe")
            otp_entry=Entry(f)
            otp_Label.grid(row=0,column=0)
            otp_entry.grid(row=0,column=1,pady=5)
            sub_btn=Button(a_root,text="Submit",cursor="target",command=lambda:self.otp_checker(a_root,otp_entry.get(),OTP,mes))
            sub_btn.pack(pady=10)
            mes=Label(a_root,text="",fg="red",background="#eaddfe")
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
        a_fn_head=Label(a_root,text="\nADMIN FUNCTIONS",bg="#eaddfe",fg="#7d4500",font="Arial 25 bold")
        a_fn_head.pack()
        add_st_btn=Button(a_root,text="Add Student",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_student(a_root))
        add_st_btn.pack(pady=20)
        modify_st_btn=Button(a_root,text="Modify Student Information",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.modify_data(a_root))
        modify_st_btn.pack(pady=20)
        delete_st_btn=Button(a_root,text="Delete Student",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.delete_student(a_root))
        delete_st_btn.pack(pady=20)
        upload_res=Button(a_root,text="Upload Result",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_result(a_root))
        upload_res.pack(pady=20)
        attendance=Button(a_root,text="Upload Attendance",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.upload_attendance(a_root))
        attendance.pack(pady=20)
    
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
        heading_s=Label(a_root,text="Add New Student",font="Arial 20 bold",bg="#eaddfe",fg="#7d4500")
        heading_s.pack(pady=20)
        false_frame=Frame(a_root)
        false_frame.pack(expand=Y)
        f1=Frame(a_root,bg="#eaddfe")
        f1.place(x=300,y=80)
        f2=Frame(a_root,bg="#eaddfe")
        f2.place(x=700,y=80)
        name_label=Label(f1,text="*Enter Name: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        name_label.grid(row=0,column=0,sticky=E)
        name_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        name_entry.grid(row=0,column=1,pady=5)
        course_label=Label(f1,text="*Select Course: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        course_selector=ttk.Combobox(f1,state="readonly",values=["B.C.A.","B.Sc. I.T.","B.A.","B.Com.","B.Sc. F.S.T","D. Pharma","M.A."],width=20)
        course_label.grid(row=1,column=0,sticky=E)
        course_selector.grid(row=1,column=1,pady=5)
        f_name_l=Label(f1,text="*Father's name: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        f_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_name_l.grid(row=2,column=0,sticky=E)
        f_name_en.grid(row=2,column=1,pady=5)
        m_name_l=Label(f1,text="*Mother's name: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        m_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_name_l.grid(row=3,column=0,sticky=E)
        m_name_en.grid(row=3,column=1,pady=5)
        g_name_l=Label(f1,text="*Guardian's name: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        g_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        g_name_l.grid(row=4,column=0,sticky=E)
        g_name_en.grid(row=4,column=1,pady=5)
        st_ID_l=Label(f1,text="*Enter ID: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_ID_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_ID_l.grid(row=5,column=0,sticky=E)
        st_ID_en.grid(row=5,column=1,pady=5)
        st_enroll_l=Label(f1,text="*Enrollment No.: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_enroll_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_enroll_l.grid(row=6,column=0,sticky=E)
        st_enroll_en.grid(row=6,column=1,pady=5)
        st_mob_l=Label(f1,text="*Enter Mob. No.: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_mob_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_mob_l.grid(row=7,column=0,sticky=E)
        st_mob_en.grid(row=7,column=1,pady=5)
        st_email_l=Label(f1,text="*Enter Email: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_email_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_email_l.grid(row=8,column=0,sticky=E)
        st_email_en.grid(row=8,column=1,pady=5)
        st_dob_l=Label(f1,text="*D.O.B.: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_dob_en=DateEntry(f1,selectmode='day',date_pattern='dd-MM-yyyy',width=20,mindate=date(1965,1,1),maxdate=date(2006,12,31))
        st_dob_l.grid(row=9,column=0,sticky=E)
        st_dob_en.grid(row=9,column=1,pady=5)
        st_12_l=Label(f1,text="*12th Passing Year: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_12_en=ttk.Combobox(f1,state="readonly",values=year12,width=20)
        st_12_l.grid(row=10,column=0,sticky=E)
        st_12_en.grid(row=10,column=1,pady=5)
        st_10_l=Label(f1,text="*10th Passing Year: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_10_en=ttk.Combobox(f1,state="readonly",values=year10,width=20)
        st_10_l.grid(row=11,column=0,sticky=E)
        st_10_en.grid(row=11,column=1,pady=5)
        st_b_group_l=Label(f1,text="*Enter Blood Group: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_b_group_en=ttk.Combobox(f1,state="readonly",values=["A+","A-","AB+","AB-","B+","B-","O+","O-"],width=20)
        st_b_group_l.grid(row=12,column=0,sticky=E)
        st_b_group_en.grid(row=12,column=1,pady=5)
        st_pwd_l=Label(f1,text="*PwD: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_pwd_en=ttk.Combobox(f1,state="readonly",values=["Yes","No"],width=20)
        st_pwd_l.grid(row=13,column=0,sticky=E)
        st_pwd_en.grid(row=13,column=1,pady=5)
        st_pwd_cat_l=Label(f1,text="Enter Disability : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_pwd_cat_en=Text(f1,width=17,height=2,highlightbackground="grey",highlightthickness=1,bd=0)
        st_address_l=Label(f1,text="*Address : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        st_address_en=Text(f1,width=17,height=4,font="Calibri",highlightbackground="grey",highlightthickness=1,bd=0)
        st_address_l.grid(row=15,column=0,sticky=E)
        st_address_en.grid(row=15,column=1)

        marks_12=Label(f2,text="*Enter 12th Percentage : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        marks_12_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        marks_12.grid(row=0,column=0,sticky=E)
        marks_12_en.grid(row=0,column=1,pady=5)
        l_per=Label(f2,text="%",bg="#eaddfe",font="Arial 10 bold")
        l_per.grid(row=0,column=2)

        marks_10=Label(f2,text="*Enter 10th Percentage : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        marks_10_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        marks_10.grid(row=1,column=0,sticky=E)
        marks_10_en.grid(row=1,column=1,pady=5)
        l_per2=Label(f2,text="%",bg="#eaddfe",font="Arial 10 bold")
        l_per2.grid(row=1,column=2)

        nationality=Label(f2,text="*Nationality : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        nationality_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        nationality.grid(row=2,column=0,sticky=E)
        nationality_en.grid(row=2,column=1,pady=5)

        aadhar=Label(f2,text="Enter Aadhar Number : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        aadhar_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        aadhar.grid(row=3,column=0,sticky=E)
        aadhar_en.grid(row=3,column=1,pady=5)

        gender_l=Label(f2,text="*Gender: ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        gender_en=ttk.Combobox(f2,state="readonly",values=["Male","Female","Others"],width=20)
        gender_l.grid(row=4,column=0,sticky=E)
        gender_en.grid(row=4,column=1,pady=5)

        f_qualification=Label(f2,text="Enter Father's Qualification : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        f_qualification_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_qualification.grid(row=5,column=0,sticky=E)
        f_qualification_en.grid(row=5,column=1,pady=5)

        m_qualification=Label(f2,text="Enter Mother's Qualification : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        m_qualification_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_qualification.grid(row=6,column=0,sticky=E)
        m_qualification_en.grid(row=6,column=1,pady=5)

        f_occupation=Label(f2,text="Enter Father's Occupation : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        f_occupation_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_occupation.grid(row=7,column=0,sticky=E)
        f_occupation_en.grid(row=7,column=1,pady=5)

        m_occupation=Label(f2,text="Enter Mother's Occupation : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        m_occupation_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_occupation.grid(row=8,column=0,sticky=E)
        m_occupation_en.grid(row=8,column=1,pady=5)

        f_mob=Label(f2,text="Father's Mobile Number : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        f_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_mob.grid(row=9,column=0,sticky=E)
        f_mob_en.grid(row=9,column=1,pady=5)

        m_mob=Label(f2,text="Mother's Mobile Number : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        m_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_mob.grid(row=10,column=0,sticky=E)
        m_mob_en.grid(row=10,column=1,pady=5)
        
        alt_mob=Label(f2,text="Alternate Mobile Number : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        alt_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        alt_mob.grid(row=11,column=0,sticky=E)
        alt_mob_en.grid(row=11,column=1,pady=5)

        alt_email=Label(f2,text="Alternate Email : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        alt_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        alt_email.grid(row=12,column=0,sticky=E)
        alt_email_en.grid(row=12,column=1,pady=5)

        f_email=Label(f2,text="Father's Email : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        f_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        f_email.grid(row=13,column=0,sticky=E)
        f_email_en.grid(row=13,column=1,pady=5)

        m_email=Label(f2,text="Mother's Email : ",bg="#eaddfe",font="Arial 10 bold",justify="right",anchor="e")
        m_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        m_email.grid(row=14,column=0,sticky=E)
        m_email_en.grid(row=14,column=1,pady=5)

        label_astrick=Label(f2,text="* to be filled neccesserily",font="Arial 10 italic")
        label_astrick.grid(row=15,column=0,columnspan=2,pady=20)

        data=[name_entry,course_selector,f_name_en,m_name_en,g_name_en,st_ID_en,st_enroll_en,st_mob_en,st_email_en,st_dob_en,st_12_en,st_10_en,st_b_group_en,st_address_en,marks_12_en,marks_10_en,nationality_en,gender_en]

        data2=[aadhar_en,f_qualification_en,m_qualification_en,f_occupation_en,m_occupation_en,f_mob_en,m_mob_en,alt_mob_en,alt_email_en,f_email_en,m_email_en]

        st_submit_btn=Button(a_root,text="Submit",cursor="target",command=lambda:self.get_st_data(a_root,data,data2,st_pwd_en,st_pwd_cat_en,mes))
        st_submit_btn.pack()

        mes=Label(a_root,text="",bg="#eaddfe")
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
        l.insert(14,st_pwd_en.get())
        l.insert(15,pwd)
        for i in data2:
            x=i.get()
            if(x==""):
                x=None
            l.append(x)
        try:
            id=int(l[5])
              #16,17,20,25,26,27,
            mob=int(l[7])
            if(l[20]!=None):
                adhar=int(l[20])
            if(l[25]!=None):
                F_no=int(l[25])
                if(len(str(F_no)) != 10):
                    mes.config(text="Invalid Father's Mobile Number",fg="red")
                    return
            if(l[26]!=None):
                M_no=int(l[26])
                if(len(str(M_no)) != 10):
                    mes.config(text="Invalid Mohter's Mobile Number",fg="red")
                    return
            if(l[27]!=None):
                alt_no=int(l[27])
                if(len(str(alt_no)) != 10):
                    mes.config(text="Invalid Alternate Mobile Number",fg="red")
                    return
        except:
            mes.config(text="Invalid Entry!!",fg="red")
        if(len(str(mob)) != 10):
             mes.config(text="Invalid Mobile Number",fg="red")
             return
        dob=l[9][6:]+'-'+l[9][3:5]+'-'+l[9][0:2]
        l[9]=dob
        
        l=tuple(l)



        global mydb
        cursor=mydb.cursor()
        cursor.execute("select st_ID from student_details")
        i=cursor.fetchall()
        j=(int(l[5]),)
        if(j in i):
            mes.config(text="ID already present",fg="red")
            return
        query="insert into student_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,l)

        query="insert into student_gen values(%s,%s,%s)";
        val=(id,l[0],l[8])
        cursor.execute(query,val)

        try:
            send_st_otp(l[8],id,l[0])
        except Exception as e:
            print(e)
            mes.config(text="No internet!!",fg="red")
            return
        
        mes.config(text="Data set",fg="green")
        mydb.commit()


    def modify_data(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Modify Student Record",font="Arial 20 bold",bg="#eaddfe",fg="#7d4500")
        head_l.pack(pady=10)

        f1=Frame(a_root,bg="#eaddfe")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="#eaddfe")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)

        sub_bt=Button(f1,text="Submit",cursor="target")
        sub_bt.grid(row=1,column=0,columnspan=2)

        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack(pady=40)


    def delete_student(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Delete Student Record",font="Arial 20 bold",bg="#eaddfe",fg="#7d4500")
        head_l.pack(pady=10)
        del_f=Frame(a_root,bg="#eaddfe")
        del_f.pack()
        
        st_id=Label(del_f,text="Enter Student ID: ",font="Arial 10 bold",justify="right",anchor="e",bg="#eaddfe")
        st_id.grid(row=0,column=0,sticky=E)

        st_id_en=Entry(del_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
        st_id_en.grid(row=0,column=1,pady=80)

        mes_box=Label(del_f,text="",bg="#eaddfe")
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
        head_l=Label(a_root,text="Upload Student Result",font="Arial 20 bold",bg="#eaddfe",fg="#7d4500")
        head_l.pack(pady=10)

        f1=Frame(a_root,bg="#eaddfe")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="#eaddfe")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)

        sub_bt=Button(f1,text="Submit",cursor="target")
        sub_bt.grid(row=1,column=0,columnspan=2)

        back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
        back_btn.pack(pady=40)

    def upload_attendance(self,a_root):
        for i in a_root.slaves():
            i.destroy()
        head_l=Label(a_root,text="Upload Student Attendance",font="Arial 20 bold",bg="#eaddfe",fg="#7d4500")
        head_l.pack(pady=10)

        f1=Frame(a_root,bg="#eaddfe")
        f1.pack()

        id_label=Label(f1,text="Enter Student ID: ",font="Arial 10 bold",bg="#eaddfe")
        id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
        id_label.grid(row=0,column=0)
        id_entry.grid(row=0,column=1,pady=80)
        mes=Label(f1,text="",fg="red",bg="#eaddfe")
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
        h1=Label(a_root,text=f"Upload Attendance of {s_name}",font="Arial 20 bold",bg="#eaddfe",fg="#7d4500")
        h1.pack(pady=10)
        




adm=Admin()

root=Tk()
root.title("Admin")
root.state("zoomed")
root.configure(bg="#eaddfe")
root.iconbitmap(f"{cwd}\images.ico")

heading=Label(root,text="\nADMIN LOGIN\n",font="Arial 50 bold",bg="#eaddfe",fg="#7d4500")
heading.pack()
if(True):
    key_entry=Entry(root,width=30,font=100)
    key_entry.insert(0,"Enter Key Here...")
    key_entry.bind("<FocusIn>",on_click)
    key_entry.pack(pady=20)
    # submit_btn=Button(root,text="Submit",cursor="target",command=lambda:adm.otp_section(root,key_entry.get(),m_label))
    submit_btn=Button(root,text="Submit",cursor="target",command=lambda:adm.adm_functions(root))

    submit_btn.pack(pady=5)
    m_label=Label(root,text="",fg="red",bg="#eaddfe")
    m_label.pack()
else:
    err_mess=Label(root,text="No Internet",font="Georgia 30",bg="#eaddfe",fg="red")
    err_mess.pack()

root.mainloop()

try:
    mydb.close()
    server.quit()
except:
    pass