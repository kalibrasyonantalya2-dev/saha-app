import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        ft.Text("TEST BAŞARILI! BEYAZ EKRANI GEÇTİK!", size=25, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD)
    )

ft.app(target=main)

