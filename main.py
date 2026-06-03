import flet as ft
import traceback
import os

def main(page: ft.Page):
    try:
        # Kendi uygulamanın kodlarını buraya yaz...
        page.add(ft.Text("Eğer bunu görüyorsan uygulama çalıştı!"))
        
    except Exception as e:
        # Kod patlarsa, hatayı telefonun Download klasörüne txt olarak yazdır
        hata_mesaji = traceback.format_exc()
        
        # Android'de genel Download klasörü yolu budur:
        hata_yolu = "/storage/emulated/0/Download/flet_hata_logu.txt"
        
        with open(hata_yolu, "w") as f:
            f.write(hata_mesaji)

ft.app(target=main)
