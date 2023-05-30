from eml_parser import EmlParser
import pdfkit
import json
import datetime
import os, shutil

def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')

def dups_checker(item_name):
    script_path = os.path.dirname(os.path.abspath(__file__))
    item_name = os.path.splitext(item_name)[0]
    item_path = script_path + '\\pdf files\\'+ item_name + '.pdf'
    i = 1
    while os.path.exists(item_path):
        item_name = item_name + "-" + str(i)
        item_path = script_path + '\\pdf files\\'+ item_name + '.pdf'
        i+=1
    return item_name

def open_eml_file(file_path):
    with open(file_path, 'rb') as email:
        raw_email= email.read()
    eml_file = os.path.basename(file_path)
    print(f"\nProcessing : {eml_file}")
    indi_html = parse_eml(raw_email,eml_file)
    return indi_html

def parse_eml(raw_email,eml_file):
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
    indi_html = format_in_html(sender,sent_to,subject,date,attachments,body,eml_file)
    return indi_html
    
def format_in_html(sender,sent_to,subject,date,attachments,body,eml_file):
    # format message in HTML Format
    indi_html =f'''
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
        indi_html+=f'<li style="margin:0px; padding:5px;">{attachment.get("filename")}</li>'
    indi_html+=f'''
        </ul>
        <h2 style="background-color:#f1630b; padding:5px;">Message:</h2>
        <p2>{body}</p2>
    </body>
    </html>
    '''
    gen_pdf_file_name = dups_checker(eml_file)
    pdfkit.from_string(indi_html,f'{gen_pdf_file_name}.pdf')
    eml_file_name = os.path.splitext(eml_file)[0]
    if gen_pdf_file_name != eml_file_name:
        print(f"\n\tRenamed - '{eml_file_name}' as '{gen_pdf_file_name}'")
    return indi_html

def page_break_hmtl():
    page_break = '''<div style="page-break-before:always;"></div>'''
    return page_break

def dir_walker(folder_path):
    combined_html = ''
    combined_file_name = 'combined_conversion'
    eml_count = 0
    try:
        for root,dirs,files in os.walk(folder_path):
            for file_name in files:
                if os.path.splitext(file_name)[1] == '.eml':
                    eml_count +=1
                    file_path = os.path.join(root, file_name)
                    indi_html = open_eml_file(file_path)
                    if eml_count !=1:
                        combined_html += page_break_hmtl()
                    combined_html += indi_html
                else:
                    continue
        gen_output_file = dups_checker(combined_file_name)
        print(f"\nProcessing : {gen_output_file}")
        pdfkit.from_string(combined_html, f'{gen_output_file}.pdf')
    except Exception as e:
        print(f"Error occured. Please try again. - {e}")
    
def move_files():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    destination_dir = folder_path + "\\pdf files\\"
    lis = os.listdir(folder_path)
    try:
        for item in lis:
            if os.path.isfile(item):
                if os.path.splitext(item)[1] == '.pdf':
                    shutil.move(item,destination_dir)
                else:
                    continue
        print(f"\nMove Successful! Files moved to '{destination_dir}'")
    except Exception as e:
        print(f"Error - {e}")

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
    move_files()
    print("\nProcess Complete!!\n")