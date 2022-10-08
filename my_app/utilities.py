import smtplib 
from email.message import EmailMessage

def read_file(path):
    with open(path, encoding="utf-8") as _file:
        return _file.read()


def send_email(subject, user, id, type):
    try:
        email_subject = subject 
        sender_email_address = "xxxxxx@uninorte.edu.co" 
        receiver_email_address = user.email 
        email_smtp = "smtp-mail.outlook.com" 
        email_password = "xxxxxxxxxxxx" 

        # Crear un objeto de mensaje de correo electrónico 
        message = EmailMessage() 

        # Configurar encabezados de correo electrónico 
        message['Subject'] = email_subject 
        message['From'] = sender_email_address 
        message['To'] = receiver_email_address 

        if type == 'recover_password':
            file_content = read_file("my_app/templates/notification_email_password.html")
            file_content = file_content.replace('@url', "http://127.0.0.1:5000/auth/reset_password?userId="+ id)
        else:
            file_content = read_file("my_app/templates/notification_email.html")
            file_content = file_content.replace('@url', "http://127.0.0.1:5000/auth/activate_account?userId="+ id)
        file_content = file_content.replace('@user_name', user.user_name)
        

        # Establecer el texto del cuerpo del correo electrónico
        message.set_content(file_content, subtype='html')

        # Establecer servidor y puerto smtp
        server = smtplib.SMTP(email_smtp, '587') 

        # Identifique este cliente en el servidor SMTP 
        server.ehlo() 

        # Asegure la conexión SMTP
        server.starttls() 

        # Iniciar sesión en la cuenta de correo electrónico
        server.login(sender_email_address, email_password) 

        # Enviar correo electrónico 
        server.send_message(message) 

        # Cerrar conexión con el servidor
        server.quit()
    except:
        print('Error al enviar correo de activacion')