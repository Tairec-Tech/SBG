import traceback
import flet as ft
from forms import abrir_form_personal_registrar

class MockPage:
    def __init__(self):
        self.data = {"usuario_actual": {"institucion_id": 1}}
        self.snack_bar = None
    
    def show_dialog(self, dialog):
        print("DIALOG SHOWN:", dialog.title.value)
    
    def update(self):
        print("PAGE UPDATED")
        
try:
    page = MockPage()
    abrir_form_personal_registrar(page)
except Exception as e:
    traceback.print_exc()
