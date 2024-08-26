from celery import shared_task
from .models import Job
import imaplib
import email
import re
from email.utils import parseaddr
from huggingface_hub import InferenceClient
from django.contrib.auth import get_user_model


@shared_task(bind=True)
def fetch_job_updates(self, username, password):


    def getMessage(email_address, password, last_ind):
        try:
            # Connect to Gmail's IMAP server
            imap_server = "imap.gmail.com"
            imap_port = 993

            # Create an IMAP4 client encrypted with SSL
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)

            # Login to the server
            mail.login(email_address, password)

            # Select the mailbox you want to access (in this case, "INBOX")
            mail.select("INBOX")

            _, data = mail.search(None, '(X-GM-RAW "category:primary")')

            mail_id_list = data[0].split()  #IDs of all emails that we want to fetch 
            if last_ind:
                mail_id_list = [byte for byte in mail_id_list if int(byte) > last_ind]
            else:
                mail_id_list = mail_id_list[-10:]

            ink = int(mail_id_list[-1])

            msgs = [] # empty list to capture all messages
            #Iterate through messages and extract data into the msgs list
            for num in mail_id_list:
                typ, data = mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
                msgs.append(data)
            # Search for the specific message using its ID

            cache = []

            for msg_data in msgs:

                data=""
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        email_body = response_part[1]
                        email_message = email.message_from_bytes(email_body)

                        name, email_address = parseaddr(email_message['from'])
                        subject = email_message['Subject']
                        date = email_message['date']

                        # Find full message body
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    data = data + part.get_payload(decode=True).decode()

                        # Remove new lines and carriage returns
                        text = data.replace('\r', '').replace('\n', ' ')

                        # Remove email header information
                        plain_text = re.sub(r'-{10,}.*?-{10,}', '', text, flags=re.DOTALL)

                        # Remove extra spaces
                        data = re.sub(r'\s+', ' ', plain_text).strip()

                        cache.append((name, email_address, date, subject, data))
            
            
            # Close the connection
            mail.close()
            mail.logout()
            return cache, ink
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_status(mail_txt, indek):

            client = InferenceClient(
            "mistralai/Mistral-7B-Instruct-v0.3",
            token="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",)

            preprompt1 = "Analyze the following email content and categorize it. Respond with one of these exact words: 'rejected' if the application was rejected 'moving forward' if the application is about applying a job 'applied'. Also return the job title. The sample format is look like 'applied' , 'software engineering intern'. If there is no job title return 'applied' , 'None'. No more than these two words, no need to explain why. Email content:"
            preprompt2 = "Analyze the following email text and determine if it's a response to a job application. Reply 'yes', if it is related to job application process, else 'no'. Reply 'no' also if this is about job alert."
            if indek == 1:
                prompt = preprompt2 + mail_txt
            else:
                prompt = preprompt1 + mail_txt

            content = ""

            for message in client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                stream=True,
            ):
                content = content + message.choices[0].delta.content

            return content
            
    def fill_status(data):
            status = []
            for each_data in data:
                if not ('job alert' in each_data[4].lower() or 'job alerts' in each_data[4].lower() or 'job' in each_data[0].lower()):
                    pmt = each_data[0] + " " + each_data[3] + " " + each_data[4]
                    isJob = get_status(pmt, 1)
                    if not 'no' in isJob.lower():
                        content = get_status(each_data[4],2)
                        content = content.lower()
                        if not 'none' in content:
                            keywords = ['applied', 'rejected', 'moving forward']
                            for keyword in keywords:
                                if keyword in content:
                                    status.append((each_data[0], content.split(", ", 1)))
            return status

    User = get_user_model()
    user = User.objects.filter(username=username).first()

    data, ink = getMessage(username, password, user.mail_id)
    status = fill_status(data)

    user.mail_id = ink  # Replace 'property_name' with the actual property you want to edit
    user.save()

    print(status)

    for company, status in status:
        Job.objects.create(
        title = status[1],
        status = status[0],
        company = company,
        author = user)
     
    return