from eml_parser import EmlParser
import pdfkit
import json
import datetime
import os, shutil

def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')

def dups_checker(item_path):
    item_name = os.path.basename(item_path).split('.')[0]
    item_path = os.path.abspath(f'pdf files/{item_name}.pdf')
    i = 1
    while os.path.exists(item_path):
        item_name = item_name + "-" + str(i)
        item_path = item_path.split("\\")
        item_path[-1] = item_name + '.pdf'
        item_path = "\\".join(item_path)
        i+=1
    return item_name

def open_eml_file(file_path):
    with open(file_path, 'rb') as email:
        raw_email= email.read()
    eml_file_path = file_path
    file_name = os.path.basename(eml_file_path)
    print(f"\nProcessing : {file_name}")
    parse_eml(raw_email,eml_file_path)

def parse_eml(raw_email, eml_file_path):
    eml_parser = EmlParser()
    parsed_eml = eml_parser.decode_email_bytes(raw_email)
    parsed_json_eml = json.loads(json.dumps(parsed_eml, indent=4,default=json_serial))
    sender = parsed_json_eml['header']['from']
    for receiver in parsed_json_eml['header']['to']:
        sent_to = receiver
    subject = parsed_json_eml['header'].get('subject')
    date = parsed_json_eml['header']['date']
    attachments = parsed_json_eml['attachment']
    body = parsed_json_eml['body'][0].get('content')

    format_in_html(sender,sent_to,date,subject,attachments,body,eml_file_path)

def format_in_html(sender,sent_to,date,subject,attachments,body,eml_file_path):
    # format message in HTML Format
    html =f'''
    <html>
    <head>
        <title>Email</title>
    </head>
    <body>
        <h2 style="background-color:#f1630b; padding:5px;">From: <span style="text-decoration:underline;">{sender}</span></h2>
        <h2 style="background-color:#f1630b; padding:5px;">To: <span style="text-decoration:underline;"> {sent_to}</span></h2>
        <h2 style="background-color:#f1630b; padding:5px;">Date: {date}</h2>
        <h2 style="background-color:#f1630b; padding:5px;">Subject: {subject}</h2>
        <h2 style="background-color:#f1630b; padding:5px;">Attachements:</h2>
        <ul style="background-color:#AEB8C3;">
    '''

    for attachment in attachments:
        html+=f'<li style="margin:0px; padding:5px;">{attachment.get("filename")}</li>'

    html+=f'''
        </ul>
        <h2 style="background-color:#f1630b; padding:5px;">Message:</h2>
        <p2>{body}</p2>
    </body>
    </html>
    '''
    gen_pdf_file_name = dups_checker(eml_file_path)
    pdfkit.from_string(html,f'{gen_pdf_file_name}.pdf')


def dir_walker(folder_path):
    try:
        for root,dirs,files in os.walk(folder_path):
            for file_name in files:
                if os.path.splitext(file_name)[1] == '.eml':
                    file_path = os.path.join(root, file_name)
                    open_eml_file(file_path)
                else:
                    continue
    except Exception as e:
        print("Error occured. Please try again.")
    

def move_files(folder_path):
    destination_dir = folder_path + '\\' + 'pdf files\\'
    lis = os.listdir(folder_path)
    for item in lis:
        if os.path.isfile(item):
            if item.split('.')[1] == 'pdf':
                shutil.move(item,destination_dir)
            else:
                continue


if __name__ == "__main__":
    if not os.path.isdir("pdf files"):
        os.makedirs("pdf files")
    print("\n\tEML To PDF\n")
    print("1. Single Conversion\n2. Bulk Conversion")
    while True:
        try:
            convert_mode = int(input("\nChoose '1' or '2': "))
            if convert_mode == 1 or 2:
                break
        except ValueError:
            pass
            print("Invalid Input.")
    if convert_mode == 1:
        file_path = input("\nFile Path: ")
        while(os.path.isfile(file_path) == False):
            file_path = input("A directory path was provided instead of a file path. Please enter File Path: ").strip('"')
        open_eml_file(file_path)
        move_from_dir = file_path.split('\\')
    elif convert_mode == 2:
        folder_path = input("\nFolder Path: ").strip('"')
        while(os.path.isfile(folder_path) == True):
            folder_path = input("A file path was provided instead of a folder path. Please enter Folder Path: ").strip('"')
        dir_walker(folder_path)
        move_from_dir = folder_path.split('\\')

    move_from_dir.pop()
    move_from_dir = "\\".join(move_from_dir)
    move_files(move_from_dir)
    print("\nProcess Complete!\n")