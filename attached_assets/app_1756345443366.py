import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = ""
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def fifty(text):
    response = model.generate_content(
        "#for the following text generate the proper and efficient summary of data and the summary should be 50% of the total words and format it .Do not "
        "include * in the output\n" + text)
    return response.text

def twentyfive(text):
    response = model.generate_content(
        "#for the following text generate the proper and efficient summary of data and the summary should be 25% of the total words and format it .Do not "
        "include * in the output\n" + text) 
    return response.text

def seventyfive(text):
    response = model.generate_content(
        "#for the following text generate the proper and efficient summary of data and the summary should be 75% of the total words and format it .Do not "
        "include * in the output\n" + text)
    return response.text

def generateSummary(text):
    response = model.generate_content("#for the folowing text generate the proper and efficient summary of data as follows and format it do not include * in the output\n"+text)
    return response.text

def generateSummaryJSON(data_list):
    os.environ['GOOGLE_API_KEY'] = "" 
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')
    summaries = []

    for data in data_list:
        thread_id = data.get("thread_id", "")
        body_texts = data.get("body", "")

        if thread_id and body_texts:
            combined_text = " ".join(body_texts)
            summary = model.generate_content("#summerzie the below mail to 60 words and keep important details and remove all the next line characters and asterisk\n"+combined_text)
            if summary!=None:
                summaries.append({"thread_id": thread_id, "body": summary.text})

    return summaries
