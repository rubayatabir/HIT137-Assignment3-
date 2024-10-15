import tkinter as tk
from tkinter import ttk
from googletrans import Translator

# Base class for the app demonstrating encapsulation and method overriding
class BaseApp:
    def __init__(self, root):
        self.root = root  # Encapsulation: the root is stored as a private instance variable
        self.root.title("Language Translator")
        self.root.geometry("400x300")
    
    # Method meant to be overridden in child classes (Method overriding)
    def create_layout(self):
        pass

# TranslatorApp demonstrates multiple inheritance by inheriting from BaseApp and tk.Tk
class TranslatorApp(BaseApp, tk.Tk):
    def __init__(self, root):
        BaseApp.__init__(self, root)  # Inheriting attributes and methods from BaseApp
        self.translator = Translator()  # Encapsulation: translator instance is private to the class
        self.create_layout()  # Method overriding: using child class's layout method

    # Method overriding: Redefining the base method to create the UI layout
    def create_layout(self):
        # Creating UI elements for input and output
        self.label_input = tk.Label(self.root, text="Enter Text")
        self.label_input.pack(pady=10)

        self.text_input = tk.Entry(self.root, width=50)
        self.text_input.pack()

        self.label_output = tk.Label(self.root, text="Translated Text")
        self.label_output.pack(pady=10)

        self.text_output = tk.Entry(self.root, width=50)
        self.text_output.pack()

        # Button to trigger the translation
        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate_text)
        self.translate_button.pack(pady=10)
        
        # Dropdown menu for language selection
        self.language_var = tk.StringVar()  # Encapsulation: the selected language is stored privately
        self.language_dropdown = ttk.Combobox(self.root, textvariable=self.language_var)
        self.language_dropdown['values'] = ('fr', 'es', 'de', 'zh-cn')  # List of supported languages
        self.language_dropdown.set('Select language')
        self.language_dropdown.pack()

    # Method for translating text entered by the user (Method overriding is possible here)
    def translate_text(self):
        input_text = self.text_input.get()  # Getting input text
        target_language = self.language_var.get()  # Getting selected language
        
        if input_text and target_language != 'Select language':
            translated = self.translator.translate(input_text, dest=target_language)
            self.text_output.delete(0, tk.END)  # Clearing the output field
            self.text_output.insert(0, translated.text)  # Showing translated text
        else:
            self.text_output.delete(0, tk.END)
            self.text_output.insert(0, "Please enter text and select a language")

# Decorator function to log actions, demonstrating multiple decorators (a simple example)
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"Translating text using the {func.__name__} method")  # Logging action
        return func(*args, **kwargs)  # Calling the original method
    return wrapper

# AdvancedTranslatorApp inherits from TranslatorApp (Inheritance) and uses polymorphism
class AdvancedTranslatorApp(TranslatorApp):
    @log_action  # Applying a decorator to log the translate action (Multiple decorators)
    def translate_text(self):
        # Method overriding: Changing behavior of translate_text with logging
        super().translate_text()  # Calling the parent class's translate_text method

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedTranslatorApp(root)  # Creating an instance of the app
    root.mainloop()  # Running the main event loop
