import os
import cv2
import json
import re
import string
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
    

    lines = lines.upper() #MENGURASI CASE SENSITIF


    #nama
    if 'NAMA' in lines or 'N4MA' in lines or 'AMA' in lines or 'NMA' in lines or 'NAMA.' in lines:
        if 'NAMA' in lines:
            nama_start = lines.index('NAMA') + 4
        elif 'N4MA' in lines:
            nama_start = lines.index('N4MA') + 4
        elif 'AMA' in lines:
            nama_start = lines.index('AMA') + 3
        elif 'NMA' in lines:
            nama_start = lines.index('NMA') + 3
        elif 'NAMA.' in lines:
            nama_start = lines.index('NAMA.') + 6
    
        nama_end = lines.find('\n', nama_start)
        nama = lines[nama_start:nama_end].strip()
        translator = str.maketrans("", "", string.punctuation)
        nama = nama.translate(translator)
        
        nama_lines = nama  # Store the value in a separate variable
        nama_split = nama.split(" ")
        
        nama_file = open("model/nama.txt", 'r')
        nama_data = nama_file.read()
        nama_file.close()

        if len(nama_split) == 1:
            threshold = 91  # Nilai ambang batas untuk kesesuaian
            kata1 = nama_split[0]

            words = nama_data.split('\n')
            
            # Perform closest match for each kata
            kata1_match = process.extractOne(kata1, words)
            kata1_closest_word = kata1_match[0]
            kata1_match_score = kata1_match[1]


            if kata1_match_score >= threshold:
                kata1 = kata1_closest_word
            else:
                kata1 = nama_split[0]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata1)
                nama_file.close()

            # Simpan hasil penggabungan dalam variabel 'hasil'
            nama = kata1

            # Cetak hasil penggabungan
            print(nama)
        elif len(nama_split) > 1:
            threshold = 91  # Nilai ambang batas untuk kesesuaian
            kata1 = nama_split[0]
            kata2 = nama_split[1]

            words = nama_data.split('\n')
            
            # Perform closest match for each kata
            kata1_match = process.extractOne(kata1, words)
            kata1_closest_word = kata1_match[0]
            kata1_match_score = kata1_match[1]

            kata2_match = process.extractOne(kata2, words)
            kata2_closest_word = kata2_match[0]
            kata2_match_score = kata2_match[1]

            if kata1_match_score >= threshold:
                kata1 = kata1_closest_word
            else:
                kata1 = nama_split[0]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata1)
                nama_file.close()

            if kata2_match_score >= threshold:
                print("masuk")
                kata2 = kata2_closest_word
            else:
                kata2 = nama_split[1]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata2)
                nama_file.close()

            # Simpan hasil penggabungan dalam variabel 'hasil'
            nama = kata1+ " " + kata2

            # Cetak hasil penggabungan
            print(nama)
        elif len(nama_split) > 2:
            threshold = 91  # Nilai ambang batas untuk kesesuaian
            kata1 = nama_split[0]
            kata2 = nama_split[1]
            kata3 = nama_split[2]

            words = nama_data.split('\n')
            
            # Perform closest match for each kata
            kata1_match = process.extractOne(kata1, words)
            kata1_closest_word = kata1_match[0]
            kata1_match_score = kata1_match[1]

            kata2_match = process.extractOne(kata2, words)
            kata2_closest_word = kata2_match[0]
            kata2_match_score = kata2_match[1]

            kata3_match = process.extractOne(kata3, words)
            kata3_closest_word = kata3_match[0]
            kata3_match_score = kata3_match[1]

            if kata1_match_score >= threshold:
                kata1 = kata1_closest_word
            else:
                kata1 = nama_split[0]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata1)
                nama_file.close()

            if kata2_match_score >= threshold:
                print("masuk")
                kata2 = kata2_closest_word
            else:
                kata2 = nama_split[1]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata2)
                nama_file.close()

            if kata3_match_score >= threshold:
                kata3 = kata3_closest_word
            else:
                kata3 = nama_split[2]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata3)
                nama_file.close()

            # Simpan hasil penggabungan dalam variabel 'hasil'
            nama = kata1+ " " + kata2+ " " + kata3

            # Cetak hasil penggabungan
            print(nama)
        elif len(nama_split) > 3:
            threshold = 91  # Nilai ambang batas untuk kesesuaian
            kata1 = nama_split[0]
            kata2 = nama_split[1]
            kata3 = nama_split[2]
            kata4 = nama_split[3]

            words = nama_data.split('\n')

            
            # Perform closest match for each kata
            kata1_match = process.extractOne(kata1, words)
            kata1_closest_word = kata1_match[0]
            kata1_match_score = kata1_match[1]

            kata2_match = process.extractOne(kata2, words)
            kata2_closest_word = kata2_match[0]
            kata2_match_score = kata2_match[1]

            kata3_match = process.extractOne(kata3, words)
            kata3_closest_word = kata3_match[0]
            kata3_match_score = kata3_match[1]

            kata4_match = process.extractOne(kata4, words)
            kata4_closest_word = kata4_match[0]
            kata4_match_score = kata4_match[1]

            if kata1_match_score >= threshold:
                kata1 = kata1_closest_word
            else:
                kata1 = nama_split[0]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata1)
                nama_file.close()

            if kata2_match_score >= threshold:
                print("masuk")
                kata2 = kata2_closest_word
            else:
                kata2 = nama_split[1]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata2)
                nama_file.close()

            if kata3_match_score >= threshold:
                kata3 = kata3_closest_word
            else:
                kata3 = nama_split[2]

            if kata4_match_score >= threshold:
                kata4 = kata4_closest_word
            else:
                kata4 = nama_split[3]
                nama_file = open("model/nama.txt", 'a')
                nama_file.write('\n' + kata3)
                nama_file.close()

            # Simpan hasil penggabungan dalam variabel 'hasil'
            nama = kata1+ " " + kata2+ " " + kata3 + " " + kata4

            # Cetak hasil penggabungan
            print(nama)
        else:
            nama = nama

    #alamat
    if 'ALAMAT' in lines or 'AIAMAT' in lines or 'AAMAT' in lines or 'ALAMIT' in lines:
        if 'ALAMAT' in lines:
            alamat_start = lines.index('ALAMAT') + 6
        elif 'AIAMAT' in lines:
            alamat_start = lines.index('AIAMAT') + 6
        elif 'AAMAT' in lines:
            alamat_start = lines.index('AAMAT') + 5
        elif 'ALAMIT' in lines:
            alamat_start = lines.index('ALAMIT') + 6
    
        alamat_end = lines.find('\n', alamat_start)
        alamat = lines[alamat_start:alamat_end].strip()
        alamat_lines = alamat  # Store the value in a separate variable

        # Remove symbols from alamat
        translator = str.maketrans("", "", string.punctuation)
        alamat = alamat.translate(translator)


        alamat_file = open("model/alamat.txt", 'r')
        alamat_data = alamat_file.read()
        alamat_file.close()

        words = alamat_data.split('\n')
        closest_match = process.extractOne(alamat_lines, words)  # Use alamat_lines
        closest_word = closest_match[0]
        match_score = closest_match[1]
        threshold = 91  # Nilai ambang batas untuk kesesuaian
        if match_score >= threshold:
            identity.alamat = closest_word
            print(identity.alamat)
        else:
            identity.alamat = alamat
            alamat_file = open("model/alamat.txt", 'a')
            alamat_file.write('\n' + alamat)
            alamat_file.close()
            print(identity.alamat)

    # kecamatan
    if 'KECAMATAN' in lines or '<ECAMATAN' in lines or '~ECAMATAN' in lines:
        if 'KECAMATAN' in lines:
            kecamatan_start = lines.index('KECAMATAN') + 9
        elif '<ECAMATAN' in lines:
            kecamatan_start = lines.index('<ECAMATAN') + 9
        elif '~ECAMATAN' in lines:
            kecamatan_start = lines.index('~ECAMATAN') + 9
        
    
        kecamatan_end = lines.find('\n', kecamatan_start)
        kecamatan = lines[kecamatan_start:kecamatan_end].strip()
        kecamatan_lines = kecamatan  # Store the value in a separate variable

        kecamatan_file = open("model/list-kecamatan.txt", 'r')
        kecamatan_data = kecamatan_file.read()
        kecamatan_file.close()

        words = kecamatan_data.split('\n')
        closest_match = process.extractOne(kecamatan_lines, words)  # Use kecamatan_lines
        closest_word = closest_match[0]
        match_score = closest_match[1]
        threshold = 90  # Nilai ambang batas untuk kesesuaian
        if match_score >= threshold:
            identity.kecamatan = closest_word
            print(identity.kecamatan)
        else:
            identity.kecamatan = ""
    
 
    # KELURAHAN
    if 'KELOESA' in lines or 'KEL/DESA' in lines or 'KEL/OESA' in lines or 'KELDESA' in lines or 'KEIDESA' in lines or 'XEIDESA' in lines or '~OTDESA' in lines:
        if 'KELOESA' in lines:
            kelurahan_start = lines.index('KELOESA') + 7
        elif 'KEL/DESA' in lines:
            kelurahan_start = lines.index('KEL/DESA') + 8
        elif 'KEL/OESA' in lines:
            kelurahan_start = lines.index('KEL/OESA') + 3
        elif 'KELDESA' in lines:
            print('kesini');
            kelurahan_start = lines.index('KELDESA') + 7
        elif 'KEIDESA' in lines:
            kelurahan_start = lines.index('KEIDESA') + 7
        elif 'XEIDESA' in lines:
            kelurahan_start = lines.index('XEIDESA') + 7
        elif '~OTDESA' in lines:
            kelurahan_start = lines.index('~OTDESA') + 7

            
    
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
        print(closest_word)
        threshold = 90  # Nilai ambang batas untuk kesesuaian
        if match_score >= threshold:
            identity.kelurahan = closest_word
        else:
            identity.kelurahan = ""
    
    # RT & RW
    if 'RTRW' in lines or 'RTW' in lines or 'RT/RW' in lines or 'RW' in lines or 'HIRW' in lines:
        if 'RTRW' in lines:
            rtrw_start = lines.index('RTRW') + 4
        elif 'RTW' in lines:
            rtrw_start = lines.index('RTW') + 3
        elif 'RT/RW' in lines:
            rtrw_start = lines.index('RT/RW') + 5
        elif 'RW' in lines:
            rtrw_start = lines.index('RW') + 2
        elif 'HIRW' in lines:
            rtrw_start = lines.index('HIRW') + 2
        
        rtrw_end = lines.find('\n', rtrw_start)
        rtrw = lines[rtrw_start:rtrw_end].strip()
        lines = rtrw   
        rtrw_file = open("model/rtrw.txt", 'r')
        rtrw_data = rtrw_file.read()
        rtrw_file.close()

        words = rtrw_data.split('\n')
        closest_match = process.extractOne(lines, words)
        closest_word = closest_match[0]
        match_score = closest_match[1]
        threshold = 60  # Nilai ambang batas untuk kesesuaian
        if match_score >= threshold:
            identity.rtrw = closest_word
            print(identity.rtrw)
        else:
            identity.rtrw = ""


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
