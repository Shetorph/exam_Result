import requests
import time
from bs4 import BeautifulSoup

#OBS DPU Öğrencileri için yapılmıştır.

print("Cookie'yi giriniz.")
cookieValue = str(input())
dersler = []
i=0
kacSaniyedeBir = 1800 #Tavsiye edilen süre. Saniye cinsinden yazınız.

while(i<=28):
    
    dersler.clear()
    headers = {
        "accept": "*/*",
        "cookie": cookieValue,
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://obs.dpu.edu.tr",
        "referer": "https://obs.dpu.edu.tr/oibs/std/index.aspx?curOp=0"
    }


    URl = "https://obs.dpu.edu.tr/oibs/std/not_listesi_op.aspx"
    response = requests.get(URl, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.select("#grd_not_listesi tr")[1:]
    
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 7:
            ders_adi = cells[2].text.strip()

            # Vize notunu al
            vize_element = cells[4].find("span", string=lambda x: "Vize" in x if x else False)
            vize = None
            if vize_element:
                vize = vize_element.text.split(":")[-1].strip()

            # Ort, Not ve Durum değerlerini al
            ort = cells[5].text.strip()
            not_degeri = cells[6].text.strip()
            durum = cells[7].text.strip()

            dersler.append({
                "ders": ders_adi,
                "vize": vize,
                "ort": ort,
                "not": not_degeri,
                "durum": durum
            })

    # Sonuçları yazdır
    print("↓" * 75)
    for ders in dersler:
        print(f"Ders : {ders['ders']}")
        print("-" * 25)
        print(f"Vize: {ders['vize']}, Ort: {ders['ort']}, Not: {ders['not']}, Durum: {ders['durum']}\n")
    print("↑" * 75)
    time.sleep(kacSaniyedeBir)
    i+=1