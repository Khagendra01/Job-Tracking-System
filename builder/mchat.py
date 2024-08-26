from huggingface_hub import InferenceClient

client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token="",
)

prompt = "Analyze the following email content and categorize it based on job application status. Respond with one of these exact words: 'nothing' if the email is not related to a job application 'rejected' if the application was rejected 'moving forward' if the application is progressing 'applied' if the email is only about submitting a job application. Just return one word, no need to explain, Email content:"
added = ' Hi Khagendra, Thank you for your interest in Dune and taking the time to speak with our team about the Staff Software Engineer, Application position. After discussing with the team, we wanted to let you know that we have decided to move forward with other candidates who we feel are more suited to this particular role at our current stage. Thank you again and all the best for the future. -- Dune Team'
added2 = ' Hello khagendra6, Please click the link below to recover your Steam login credentials: Resume Recovery If you are not trying to recover your Steam login credentials from a computer located in New Jersey, United States, please ignore this email. It is possible that another user entered their login information incorrectly. Cheers, The Steam Team This notification has been sent to the email address associated with your Steam account. This email message was auto-generated. Please do not respond. If you need additional help, please visit Steam Support.'
added3 = ' Hi Khagendra, Thanks again for expressing your interest in the Graduate Software Engineer position at Optiver! We have reviewed your application and are excited to move forward with your candidacy. Below is an overview of our interview process, which typically spans 4 to 8 weeks, depending on availability. Optiver Online Assessment Behavioral Phone Interview with a recruiter Virtual Technical Screen Virtual Technical Interviews Virtual Behavioral Interview Lets get started: The first step in our interview process is the Optiver Online Assessment, which consists of three parts. The entire assessment takes approximately 3.5 hours to complete. You are allowed to take breaks between sections, but once you start a section, you must complete it without pausing. Within 48 hours, you will receive a separate email from the Optiver Assessment Platform (OAP) with detailed instructions and assessment links. Please complete the assessment within the next 15 days to ensure a smooth and efficient progression of your application. Failure to complete the assessment within the recommended timeframe may result in the discontinuation of your application. Due Date: 15 days from today Once you complete the assessment, we will follow up within two weeks to let you know if you qualify for the next round. Please keep the following in mind: If you do not receive a separate email from OAP within an hour, check your spam folder. If it is not there, contact us at recruiting@optiver.us for assistance. The use of AI assistance (ChatGPT, etc.) or online resources (Google, Stack Overflow, etc.) are not allowed for Optivers assessments. This assessment is an approximation of later face-to-face interviews where you will be expected to solve problems in real time. If your assessment is flagged for plagiarism this may result in your application to Optiver being disqualified. Assessments can only be completed once. If you have completed them in the last 8 months for a different role, Optiver location, or with a different email address, your application will be rejected. Before starting your assessment, ensure you have read the directions and are in an optimal environment. We recommend using a laptop or desktop, as using an iPhone or iPad may affect how the assessment platform is displayed on your device. Requests to retake the assessment or any portion of it due to human error or environmental distractions will not be granted. Thanks again and good luck! On Behalf of Optiver US Recruitment'
prompt = prompt + added2


content = ""
for message in client.chat_completion(
	messages=[{"role": "user", "content": prompt}],
	max_tokens=10,
	stream=True,
):
    content = content + message.choices[0].delta.content

content = content.lower()
if 'applied' in content:
    print('applied')

if 'rejected' in content:
    print('rejected')

if 'moving forward' in content:
    print('moving forward')

if 'nothing' in content:
    print('nothing')


