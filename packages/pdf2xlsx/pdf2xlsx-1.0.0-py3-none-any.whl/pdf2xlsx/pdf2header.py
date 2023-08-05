import os
import shutil
import re
from collections import namedtuple
from PyPDF2 import PdfFileReader

FILENAME = '6510849534_info@isneaker.eu.pdf'

Invoice = namedtuple('Invoice', ['sorszam', 'kelt', 'fizetesihatar', 'vegosszeg'])

SORSZAM_PATTERN = '[ ]*Számla sorszáma:([0-9]+)'
SORSZAMPROG = re.compile(SORSZAM_PATTERN)

KELT_PATTERN = '[ ]*Számla kelte:[([0-9]{4}\.[0-9]{2}\.[0-9]{2}|[0-9]{2}\.[0-9]{2}\.[0-9]{4}])'
KELTPROG = re.compile(KELT_PATTERN)

FIZETESI_PATTERN = '[ ]*FIZETÉSI HATÁRIDÕ:([0-9]{4}\.[0-9]{2}\.[0-9]{2})[ ]+([0-9]+\.?[0-9]*\.?[0-9]*)'
FIZETESIPROG = re.compile(FIZETESI_PATTERN)


def get_invoice():
    sorszam = False
    kelt = False
    fizetesihatar = False
    vegosszeg = False
    line = ""
    while True:
        if not sorszam:
            mo = SORSZAMPROG.match(line)
            if mo:
                sorszam = int(mo.group(1))
                line = yield sorszam
        elif not kelt:
            mo = KELTPROG.match(line)
            if mo:
                kelt = mo.group(1)
                line = yield kelt
        else:
            mo = FIZETESIPROG.match(line)
            if mo:
                fizetesihatar = mo.group(1)
                vegosszeg = int(mo.group(2).replace('.',''))
                tmp_invo = Invoice(sorszam, kelt, fizetesihatar, vegosszeg)
                while True:
                    line = yield tmp_invo
        line = yield None
                
                

def parse_file():
    with open(FILENAME, 'rb') as fd:
        tmp_input = PdfFileReader(fd)
        tmp_lines = tmp_input.getPage(0).extractText().split('\n')
        invoice_getter = get_invoice()
        invo = next(invoice_getter)
        for line in tmp_lines:
            invo = invoice_getter.send(line)

        invoice_getter.close()
        return invo                    



#invo = get_invoice()
invo = parse_file()
print(invo)
