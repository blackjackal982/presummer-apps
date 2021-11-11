import click
import mysql.connector
from mysql.connector import Error
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(toaddr,clg_name,student_data,college_summary,global_summary):
    fromaddr = "ssirisha639@gmail.com"
    msg = MIMEMultipart()
    msg['Subject'] = "COLLEGE REPORT"
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("ssirisha639@gmail.com", "D!ngoo12")

    string = clg_name+"\n"+"name_of_student\t\ttotal_marks\n"
    for row in student_data:
        string+= row[0]+"\t\t"+str(row[1])+"\n"


    string +="college\tno_of_students\tmax_marks\tmin_marks\tavg_marks\n"
    for row in college_summary:
            string+=row[0] + "\t\t" + str(row[1]) + "\t\t" + str(row[2]) + "\t\t" + str(row[3]) + "\t\t" + str(row[4]) + "\n"

    string +="name\t\tclg_name\t\temail_id\t\tmarks\n"
    for row in global_summary:
            string+=row[0] + "\t\t" + str(row[1]) + "\t\t" + str(row[2]) + "\t\t" + str(row[4]) + "\n"

    body = string
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr,toaddr, text)
    server.quit()

@click.command()
@click.argument('clg_name')
def send_report(clg_name):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="dingoo12",database="pca_6")
        mycursor = conn.cursor()

        student_scores ="SELECT marks.name,total_marks from student join marks on student.name=marks.name where student.clg_name='"+clg_name+"';"

        clg_summary = "SELECT clg_name,count(*),max(total_marks),min(total_marks),avg(total_marks) \
        from student join marks on student.name=marks.name group by clg_name;"

        global_summary = "SELECT * from student join marks on student.name=marks.name group by clg_name;"

        mycursor.execute(clg_summary)
        clg_summary = mycursor.fetchall()

        mycursor.execute(global_summary)
        global_summary = mycursor.fetchall()

        mycursor.execute(student_scores)
        student_scores = mycursor.fetchall()

        send_email("blackjackal982@gmail.com",clg_name,student_scores,clg_summary,global_summary)

    except Error as e:
        click.echo(e)
    finally:
        mycursor.close()
        conn.close()

if __name__=='__main__':
    send_report()