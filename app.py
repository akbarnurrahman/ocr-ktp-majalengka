import os
import cv2
import json
import re
import datetime
import math
import asyncio
import pytesseract
import numpy as np
import urllib.request as rq
import Levenshtein
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from sanic import Sanic
from sanic.response import json
from functools import wraps, partial
from sanic_cors import CORS, cross_origin
import Levenshtein
class Identity(object):
    def __init__(self):
        self.provinsi = ""
        self.kelurahan = ""
        self.rtrw = ""
    
    def extract_ktp(lines):
        print('ok')

  

def month_to_number(arg):
    switcher = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03",
        "APR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12"
    }
    return switcher.get(arg, "Invalid month")



def parse_ktp(lines):
    res = []
    dates = []

    identity = Identity()
    lines = lines.replace("\n\n\n\n\n", "\n").replace("\n\n\n\n", "\n").replace("\n\n\n", "\n").replace("\n\n", "\n")
    print(lines)
   
    if 'KelOesa' in lines or 'Kel/Desa' in lines or 'Kel/Oesa' in lines or 'KelDesa' in lines:
        if 'KelOesa' in lines:
            kelurahan_start = lines.index('KelOesa') + 7
        elif 'Kel/Desa' in lines:
            kelurahan_start = lines.index('Kel/Desa') + 8
        elif 'Kel/Oesa' in lines:
            kelurahan_start = lines.index('Kel') + 3
        elif 'KelDesa' in lines:
            kelurahan_start = lines.index('KelDesa') + 7
    
        kelurahan_end = lines.find('\n', kelurahan_start)
        kelurahan = lines[kelurahan_start:kelurahan_end].strip()
        kelurahan_lines = kelurahan  # Store the value in a separate variable
        kelurahan_file = open("model/desa.txt", 'r')
        kelurahan_data = kelurahan_file.read()
        kelurahan_file.close()

        words = kelurahan_data.split('\n')
        closest_match = process.extractOne(kelurahan_lines, words)  # Use kelurahan_lines
        closest_word = closest_match[0]
        match_score = closest_match[1]
        threshold = 80  # Nilai ambang batas untuk kesesuaian
        if match_score >= threshold:
            identity.kelurahan = closest_word
            print(identity.kelurahan)
        else:
            identity.kelurahan = ""
    
    if 'RTRW' in lines or 'RTW' in lines or 'RT/RW' in lines or 'RW' in lines:
        if 'RTRW' in lines:
            rtrw_start = lines.index('RTRW') + 4
        elif 'RTW' in lines:
            rtrw_start = lines.index('RTW') + 3
        elif 'RT/RW' in lines:
            rtrw_start = lines.index('Kel') + 5
        elif 'RW' in lines:
            rtrw_start = lines.index('RW') + 2
        
        rtrw_end = lines.find('\n', rtrw_start)
        rtrw = lines[rtrw_start:rtrw_end].strip()
        lines = rtrw   
        provinsis_file = open("model/rtrw.txt", 'r')
        provinsis_data = provinsis_file.read()
        provinsis_file.close()

        words = provinsis_data.split('\n')
        closest_match = process.extractOne(lines, words)
        closest_word = closest_match[0]
        match_score = closest_match[1]
        threshold = 80  # Nilai ambang batas untuk kesesuaian
        if match_score >= threshold:
            identity.provinsi = closest_word
            print(identity.provinsi)
        else:
            identity.provinsi = ""


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


def to_json(object):
    return object.__dict__


def validateInvalidCharacter(text):
    if re.search('\n|:|/|NIK|Alamat|Agama|Provinsi|-', text, flags=re.IGNORECASE):
        return ""
    return text


def validateCity(text):
    if re.search(r'[0-9]', text):
        return ""
    return text


def validateResponse(response):
    response.nama = validateInvalidCharacter(response.nama)
    response.kota = validateCity(response.kota)
    return response


@async_wrap
def detect_text(path):
    result = Identity()
    try:
        img = cv2.imread(path)
        height, width = img.shape[:2]
        img = cv2.resize(img, (1024, int((height * 1024) / width)))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
        lines = pytesseract.image_to_string((threshed), lang="ind")
        if re.search("paspor|passport", lines, flags=re.IGNORECASE):
            result = parse_passport(lines)
        elif re.search("kepolisian|surat izin mengemudi|surat izin", lines, flags=re.IGNORECASE):
            result = parse_sim(lines)
        elif re.search("provinsi daerah|nik|provinsi|", lines, flags=re.IGNORECASE):
            result = parse_ktp(lines)
       
    except:
        return to_json(result)


@async_wrap
def detect_text_url(url):
    result = Identity()
    try:
        resp = rq.urlopen(url)
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        height, width = img.shape[:2]
        img = cv2.resize(img, (1024, int((height * 1024) / width)))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
        lines = pytesseract.image_to_string((threshed), lang="ind")
        if re.search("paspor|passport", lines, flags=re.IGNORECASE):
            result = parse_passport(lines)
        elif re.search("kepolisian|surat izin mengemudi|surat izin", lines, flags=re.IGNORECASE):
            result = parse_sim(lines)
        elif re.search("provinsi daerah|nik|provinsi|", lines, flags=re.IGNORECASE):
            result = parse_ktp(lines)
        return to_json(result)
    except:
        return to_json(result)


app = Sanic("ocr")

@app.route("/scan", methods=['POST'])
async def scan(request):
    if request.json is not None:
        values = request.json
        if "path" in values:
            path = values['path']
            data = await detect_text(path)
            return json(data)
    return json({"error": "path is required."})




def run():
    app.run(host="0.0.0.0", port=5000, access_log=True,
            debug=True, workers=4)


if __name__ == "__main__":
    run()
