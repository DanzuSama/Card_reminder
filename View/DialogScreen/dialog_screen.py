from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.properties import NumericProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class MyDialog(ModalView):
    timer = NumericProperty(10)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def on_dismiss(self):
        self.stop_timer()

    def update_timer(self, dt):
        self.timer -= 1
        self.dialog.buttons[0].text = 'Close ({})'.format(self.timer)
        if self.timer == 0:
            self.dialog.dismiss()
            Clock.unschedule(self.update_timer)

    def show(self, title, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text='Close ({})'.format(self.timer),
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
            Clock.schedule_interval(self.update_timer, 1)
        self.dialog.open()

