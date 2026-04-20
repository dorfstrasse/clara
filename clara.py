# My name is CLARA, stands for Cash Logging And Reporting Assistant

import imaplib
import email
from email.header import decode_header
import re
import json
import os
import schedule
import time
import logging
from datetime import datetime
from typing import Optional
 
import gspread
from google.oauth2.service_account import Credentials


CONFIG = {
    "email_address": "eins5tud1um1n153ltwald@gmail.com",
    "email_code": "ruhkmmrtubkkmcpl",
    "gsheet_credentials_file": "credentials.json",
    "spreadsheet_id": "1Jxir66vMsTUVte7ZBBcvrIdXzCnxQHS4CXfdnewgE-k",
    "sheet_name": "CLARA",
    "interval_minutes": 60,
    "processed_ids_file": "processed_ids.json",
}

COLUMNS = ["Tanggal", "Nominal", "Dompet", "Kategori", "Keterangan", "Status"]

#==========================================================================================
#                                       FILE LOGGING
#==========================================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("clara.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("CLARA")
#==========================================================================================

imap_url = 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(CONFIG["email_address"], CONFIG["email_code"])
mail.select('inbox')
_, search_data = mail.search(None, 'UNSEEN')

status, messages = mail.search(None, '(FROM "receipts@blubybcadigital.id")')
email_ids = messages[0].split()

for eid in email_ids[-5:]:
    status, msg_data = mail.fetch(eid, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            
            subject = msg["subject"]
            print("Subject:", subject)
            
            # Ambil body
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print("Body:", body)
            else:
                body = msg.get_payload(decode=True).decode()
                print("Body:", body)