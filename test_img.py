import flet as ft
try:
    img = ft.Image(src="data:image/png;base64,abc", width=32)
    print("src with data URI works!")
except Exception as e:
    print("error:", e)
