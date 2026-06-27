"""
File: main.py
Version: 0.4.0
Purpose: Cross-platform Kivy UI prototype for MobilePartsDB.
"""

# IMPORTS
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from app.backend.database import (
    initialize_database,
    create_entry,
    add_attachment_to_entry,
    get_all_entries,
    get_attachments_for_entry,
    FILE_TYPE_IMAGE,
)


# CONSTANTS
SCREEN_HOME = "home"
SCREEN_NEW_ENTRY = "new_entry"
SCREEN_ENTRIES = "entries"


# FUNCTIONS
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        layout.add_widget(Label(text="MobilePartsDB", font_size=32))

        new_button = Button(text="New Entry", font_size=24)
        new_button.bind(on_press=self.go_to_new_entry)

        entries_button = Button(text="View Entries", font_size=24)
        entries_button.bind(on_press=self.go_to_entries)

        layout.add_widget(new_button)
        layout.add_widget(entries_button)

        self.add_widget(layout)

    def go_to_new_entry(self, instance):
        self.manager.get_screen(SCREEN_NEW_ENTRY).reset_screen()
        self.manager.current = SCREEN_NEW_ENTRY

    def go_to_entries(self, instance):
        self.manager.get_screen(SCREEN_ENTRIES).refresh_entries()
        self.manager.current = SCREEN_ENTRIES


class NewEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_files = []

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        layout.add_widget(Label(text="New Knowledge Card", font_size=26))

        self.file_chooser = FileChooserListView()
        layout.add_widget(self.file_chooser)

        add_file_button = Button(text="Add Selected Attachment", font_size=20, size_hint_y=None, height=60)
        add_file_button.bind(on_press=self.add_selected_file)

        self.selected_label = Label(text="Selected attachments: 0", font_size=18, size_hint_y=None, height=40)

        self.name_input = TextInput(
            hint_text="Quick name, example: 4 inch carrier",
            multiline=False,
            font_size=20,
            size_hint_y=None,
            height=55,
        )

        save_button = Button(text="Save Entry", font_size=22, size_hint_y=None, height=60)
        save_button.bind(on_press=self.save_entry)

        back_button = Button(text="Back", font_size=22, size_hint_y=None, height=60)
        back_button.bind(on_press=self.go_home)

        layout.add_widget(add_file_button)
        layout.add_widget(self.selected_label)
        layout.add_widget(self.name_input)
        layout.add_widget(save_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def reset_screen(self):
        self.selected_files = []
        self.selected_label.text = "Selected attachments: 0"
        self.name_input.text = ""

    def add_selected_file(self, instance):
        selected = self.file_chooser.selection

        if len(selected) == 0:
            return

        selected_file = selected[0]

        if selected_file not in self.selected_files:
            self.selected_files.append(selected_file)

        self.selected_label.text = f"Selected attachments: {len(self.selected_files)}"

    def save_entry(self, instance):
        entry_id = create_entry(self.name_input.text)

        for file_path in self.selected_files:
            add_attachment_to_entry(entry_id, file_path, FILE_TYPE_IMAGE)

        self.reset_screen()
        self.manager.get_screen(SCREEN_ENTRIES).refresh_entries()
        self.manager.current = SCREEN_ENTRIES

    def go_home(self, instance):
        self.manager.current = SCREEN_HOME


class EntriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.layout.add_widget(Label(text="Saved Entries", font_size=28))

        self.entries_box = BoxLayout(orientation="vertical", spacing=5)

        back_button = Button(text="Back", font_size=22, size_hint_y=None, height=60)
        back_button.bind(on_press=self.go_home)

        self.layout.add_widget(self.entries_box)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def refresh_entries(self):
        self.entries_box.clear_widgets()

        entries = get_all_entries()

        if len(entries) == 0:
            self.entries_box.add_widget(Label(text="No entries yet.", font_size=20))
            return

        for entry_id, created_at, quick_name, status in entries:
            attachments = get_attachments_for_entry(entry_id)
            entry_text = (
                f"{entry_id}: {quick_name}\n"
                f"Status: {status}\n"
                f"Attachments: {len(attachments)}\n"
                f"Created: {created_at}"
            )

            self.entries_box.add_widget(Label(text=entry_text, font_size=16))

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