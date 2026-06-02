import flet as ft
import datetime
import urllib.request
import json

def main(page: ft.Page):
    # --- MOBİL CİHAZ VE SAYFA AYARLARI ---
    page.title = "Saha Mobil Veri Giriş Sistemi"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_GREY_900

    # --- FIREBASE AYARLARI ---
    PROJECT_ID = "kalibrasyon07-19e1d"
    COLLECTION_NAME = "saha_olcumleri"
    FIREBASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION_NAME}"

    # --- MOBİL UYUMLU GİRİŞ ALANLARI ---
    anahat = ft.TextField(label="Anahat Kollektör", prefix_icon=ft.Icons.ACCOUNT_TREE, expand=True)
    rigol = ft.TextField(label="Rigol Ad", prefix_icon=ft.Icons.LOCATION_ON, expand=True)
    
    ch4 = ft.TextField(label="CH4 (%)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    co2 = ft.TextField(label="CO2 (%)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    o2 = ft.TextField(label="O2 (%)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    h2s = ft.TextField(label="H2S (ppm)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    
    emis = ft.TextField(label="Emiş", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    debi1 = ft.TextField(label="Debi 1", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    debi2 = ft.TextField(label="Debi 2", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    
    vana1 = ft.TextField(label="Vana K. 1 (%)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    vana2 = ft.TextField(label="Vana K. 2 (%)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)

    def bildirim_goster(mesaj, renk):
        page.snack_bar = ft.SnackBar(ft.Text(mesaj, size=15, weight=ft.FontWeight.BOLD), bgcolor=renk)
        page.snack_bar.open = True
        page.update()

    def verileri_gonder(e):
        btn_kaydet.disabled = True
        # GÜNCELLEME: text yerine content kullanıyoruz
        btn_kaydet.content = ft.Text("Mobil Bağlantı Kuruluyor...", size=16) 
        page.update()

        su_an = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def veri_oku(textfield):
            return textfield.value if textfield.value else "0"

        firebase_paketi = {
            "fields": {
                "Tarih": {"stringValue": su_an},
                "Anahat_Kollektor": {"stringValue": anahat.value if anahat.value else "Belirtilmedi"},
                "Rigol_Ad": {"stringValue": rigol.value if rigol.value else "Belirtilmedi"},
                "CH4": {"stringValue": veri_oku(ch4)},
                "CO2": {"stringValue": veri_oku(co2)},
                "O2": {"stringValue": veri_oku(o2)},
                "H2S": {"stringValue": veri_oku(h2s)},
                "Emis": {"stringValue": veri_oku(emis)},
                "Debi_1": {"stringValue": veri_oku(debi1)},
                "Debi_2": {"stringValue": veri_oku(debi2)},
                "Vana_K_1": {"stringValue": veri_oku(vana1)},
                "Vana_K_2": {"stringValue": veri_oku(vana2)}
            }
        }

        try:
            data_bytes = json.dumps(firebase_paketi).encode("utf-8")
            req = urllib.request.Request(
                FIREBASE_URL, 
                data=data_bytes, 
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    bildirim_goster("✅ Veriler Firebase'e Başarıyla Uçuruldu!", ft.Colors.GREEN_700)
                    for alan in [anahat, rigol, ch4, co2, o2, h2s, emis, debi1, debi2, vana1, vana2]:
                        alan.value = ""
                else:
                    bildirim_goster(f"❌ Sunucu Hatası: {response.status}", ft.Colors.RED_700)
                    
        except Exception as ex:
            bildirim_goster(f"❌ Ağ/Bağlantı Hatası: {ex}", ft.Colors.RED_700)

        btn_kaydet.disabled = False
        # GÜNCELLEME: Gönderim bittikten sonra tekrar eski haline dönüyor
        btn_kaydet.content = ft.Text("Sisteme Kaydet", size=16)
        page.update()

    # --- GÜNCELLENEN BUTON ---
    btn_kaydet = ft.ElevatedButton(
        content=ft.Text("Sisteme Kaydet", size=16),  # Hatanın çözüldüğü kısım
        icon=ft.Icons.CLOUD_UPLOAD,
        width=280, 
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600, 
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=verileri_gonder
    )

    mobil_ekran = ft.Column(
        spacing=15,
        controls=[
            ft.Text("MOBİL SAHA PANELİ", size=24, weight=ft.FontWeight.W_900, color=ft.Colors.BLUE_300),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("📍 Konum", color=ft.Colors.WHITE70, size=14, weight=ft.FontWeight.BOLD),
                    ft.Row([anahat]),
                    ft.Row([rigol])
                ]),
                padding=12, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=10
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("☁️ Gaz Değerleri", color=ft.Colors.WHITE70, size=14, weight=ft.FontWeight.BOLD),
                    ft.Row([ch4, co2], spacing=10),
                    ft.Row([o2, h2s], spacing=10)
                ]),
                padding=12, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=10
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("💨 Akış / Emiş", color=ft.Colors.WHITE70, size=14, weight=ft.FontWeight.BOLD),
                    ft.Row([emis]),
                    ft.Row([debi1, debi2], spacing=10)
                ]),
                padding=12, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=10
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("⚙️ Vana Kontrol", color=ft.Colors.WHITE70, size=14, weight=ft.FontWeight.BOLD),
                    ft.Row([vana1, vana2], spacing=10)
                ]),
                padding=12, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=10
            ),

            ft.Row([btn_kaydet], alignment=ft.MainAxisAlignment.CENTER)
        ]
    )

    ana_tasarim_kutusu = ft.Container(
        content=mobil_ekran,
        width=420,
        padding=10
    )

    page.add(ana_tasarim_kutusu)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)