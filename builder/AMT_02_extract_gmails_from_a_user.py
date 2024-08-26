# https://youtu.be/K21BSZPFIjQ
"""
Extract selected mails from your gmail account

1. Make sure you enable IMAP in your gmail settings
(Log on to your Gmail account and go to Settings, See All Settings, and select
 Forwarding and POP/IMAP tab. In the "IMAP access" section, select Enable IMAP.)

2. If you have 2-factor authentication, gmail requires you to create an application
specific password that you need to use. 
Go to your Google account settings and click on 'Security'.
Scroll down to App Passwords under 2 step verification.
Select Mail under Select App. and Other under Select Device. (Give a name, e.g., python)
The system gives you a password that you need to use to authenticate from python.

"""

# Importing libraries
import imaplib
import email

from email.utils import parseaddr

from huggingface_hub import InferenceClient



user, password = "khagendrakhatri365@gmail.com", ""

#URL for IMAP connection
imap_url = 'imap.gmail.com'

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Log in using your credentials
my_mail.login(user, password)

# Select the Inbox to fetch messages
my_mail.select('Inbox')

#Define Key and Value for email search
#For other keys (criteria): https://gist.github.com/martinrusev/6121028#file-imap-search
key = 'FROM'
_, data = my_mail.search(None, 'ALL')  #Search for emails with specific key and value

mail_id_list = data[0].split()  #IDs of all emails that we want to fetch 
mail_id_list = mail_id_list[-10:]

msgs = [] # empty list to capture all messages
#Iterate through messages and extract data into the msgs list
for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
    msgs.append(data)


for msg in msgs[::-1]:
    for response_part in msg:
        if type(response_part) is tuple:
            my_msg=email.message_from_bytes((response_part[1]))
            print("_________________________________________")
            print ("subj:", my_msg['subject'])
            print ("from:", my_msg['from'])
            print ("date:", my_msg['date'])
            print ("body:")

                        # Extract name and email from the "from" field
            name, email_address = parseaddr(my_msg['from'])
            
            # Split the name into first and last name
            name_parts = name.split()
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[-1] if len(name_parts) > 1 else ""
            
            print("First Name:", first_name)
            print("Last Name:", last_name)


            for part in my_msg.walk():  
                #print(part.get_content_type())
                if part.get_content_type() == 'text/plain':
                    print (part.get_payload())



def status(mail_txt):

    client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token="",)

    preprompt = "Analyze the following email content and categorize it based on job application status. Respond with one of these exact words: 'nothing' if the email is not related to a job application 'rejected' if the application was rejected 'moving forward' if the application is progressing 'applied' if the email is only about submitting a job application. Just return one word, no need to explain, Email content:"

    prompt = preprompt + mail_txt

    for message in client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        stream=True,
    ):
        content = content + message.choices[0].delta.content

    content = content.lower()

    keywords = ['applied', 'rejected', 'moving forward', 'nothing']

    for keyword in keywords:
        if keyword in content:
            return keyword

            
