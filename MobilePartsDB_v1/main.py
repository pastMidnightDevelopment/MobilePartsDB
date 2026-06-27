"""
File: main.py
Version: 0.1.0
Purpose: Main Kivy app for MobilePartsDB.
"""

# IMPORTS
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from database import initialize_database, create_entry, get_all_entries

# CONSTANTS
SCREEN_HOME = "home"
SCREEN_NEW_ENTRY = "new_entry"
SCREEN_ENTRIES = "entries"

# FUNCTIONS
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        title = Label(text="MobilePartsDB", font_size=32)

        new_button = Button(text="New Entry", font_size=24)
        new_button.bind(on_press=self.go_to_new_entry)

        entries_button = Button(text="View Entries", font_size=24)
        entries_button.bind(on_press=self.go_to_entries)

        layout.add_widget(title)
        layout.add_widget(new_button)
        layout.add_widget(entries_button)

        self.add_widget(layout)

    def go_to_new_entry(self, instance):
        self.manager.current = SCREEN_NEW_ENTRY

    def go_to_entries(self, instance):
        self.manager.get_screen(SCREEN_ENTRIES).refresh_entries()
        self.manager.current = SCREEN_ENTRIES


class NewEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        title = Label(text="New Knowledge Card", font_size=28)

        camera_placeholder = Label(
            text="[Camera will go here in Session 2]",
            font_size=20
        )

        self.name_input = TextInput(
            hint_text="Quick name, example: MAC valve",
            multiline=False,
            font_size=22,
            size_hint_y=None,
            height=60
        )

        save_button = Button(text="Add Entry", font_size=24)
        save_button.bind(on_press=self.save_entry)

        back_button = Button(text="Back", font_size=24)
        back_button.bind(on_press=self.go_home)

        layout.add_widget(title)
        layout.add_widget(camera_placeholder)
        layout.add_widget(self.name_input)
        layout.add_widget(save_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def save_entry(self, instance):
        create_entry(self.name_input.text)
        self.name_input.text = ""
        self.manager.get_screen(SCREEN_ENTRIES).refresh_entries()
        self.manager.current = SCREEN_ENTRIES

    def go_home(self, instance):
        self.manager.current = SCREEN_HOME


class EntriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.title = Label(text="Saved Entries", font_size=28)

        self.entries_box = BoxLayout(orientation="vertical", spacing=5)

        back_button = Button(text="Back", font_size=24)
        back_button.bind(on_press=self.go_home)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.entries_box)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def refresh_entries(self):
        self.entries_box.clear_widgets()

        entries = get_all_entries()

        if len(entries) == 0:
            self.entries_box.add_widget(Label(text="No entries yet.", font_size=22))
            return

        for entry_id, created_at, quick_name, status in entries:
            entry_text = f"{entry_id}: {quick_name} | {status} | {created_at}"
            self.entries_box.add_widget(Label(text=entry_text, font_size=18))

    def go_home(self, instance):
        self.manager.current = SCREEN_HOME


# MAIN
class MobilePartsDBApp(App):
    def build(self):
        initialize_database()

        screen_manager = ScreenManager()

        screen_manager.add_widget(HomeScreen(name=SCREEN_HOME))
        screen_manager.add_widget(NewEntryScreen(name=SCREEN_NEW_ENTRY))
        screen_manager.add_widget(EntriesScreen(name=SCREEN_ENTRIES))

        return screen_manager


# PROGRAM START
if __name__ == "__main__":
    MobilePartsDBApp().run()