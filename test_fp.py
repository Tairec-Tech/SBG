import flet as ft

def main(page: ft.Page):
    def on_file(e): pass
    fp = ft.FilePicker()
    fp.on_result = on_file
    page.overlay.append(fp)
    page.update()
    page.add(ft.Text("Testing FilePicker"))

ft.app(target=main)
