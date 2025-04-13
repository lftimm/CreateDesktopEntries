import customtkinter as CTk
import tkinter.filedialog as fd
from desktop_entry_builder import DesktopEntryBuilder


class MainWindow(CTk.CTk):
    TITLE = "Desktop Entry Builder"
    GEOMETRY = "500x600"

    def __init__(self):
        super().__init__()
        self.setup()

        # Inputs
        self.entries = {}

        form_fields = [
            ("Name", "App name"),
            ("Version", "1.0"),
            ("Type", "Application"),
            ("Comment", "Description"),
            ("Exec", "/usr/bin/app"),
            ("Icon", "icon.png"),
            ("Path", "/usr/bin"),
            ("Categories", "Utility;Development"),
        ]

        for i, (key, placeholder) in enumerate(form_fields):
            label = CTk.CTkLabel(self, text=key)
            label.grid(row=i, column=0, sticky="e", padx=10, pady=5)

            entry = CTk.CTkEntry(self, placeholder_text=placeholder)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

            self.entries[key] = entry

        # Terminal Checkbox
        self.use_terminal = CTk.BooleanVar(value=False)
        terminal_checkbox = CTk.CTkCheckBox(self, text="Run in Terminal", variable=self.use_terminal)
        terminal_checkbox.grid(row=len(form_fields), column=0, columnspan=2, pady=10)

        # File picker button
        file_button = CTk.CTkButton(self, text="Pick Executable", command=self.pick_exec_file)
        file_button.grid(row=len(form_fields) + 1, column=0, columnspan=2, pady=5)

        # Submit button
        build_button = CTk.CTkButton(self, text="Build .desktop Entry", command=self.build_entry)
        build_button.grid(row=len(form_fields) + 2, column=0, columnspan=2, pady=10)

        # Output box
        self.output_box = CTk.CTkTextbox(self, height=100, wrap="none")
        self.output_box.grid(row=len(form_fields) + 3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.output_box.configure(state="disabled")

        self.grid_columnconfigure(1, weight=1)
        self.mainloop()

    def setup(self):
        self.title(MainWindow.TITLE)
        self.geometry(MainWindow.GEOMETRY)
        CTk.set_appearance_mode("system")
        CTk.set_default_color_theme("blue")

    def pick_exec_file(self):
        file_path = fd.askopenfilename(title="Select Executable")
        if file_path:
            self.entries["Exec"].delete(0, "end")
            self.entries["Exec"].insert(0, file_path)

    def build_entry(self):
        try:
            builder = DesktopEntryBuilder() \
                .WithName(self.entries["Name"].get()) \
                .WithVersion(self.entries["Version"].get()) \
                .OfType(self.entries["Type"].get()) \
                .WithComment(self.entries["Comment"].get()) \
                .InThisPath(self.entries["Path"].get()) \
                .ExecuteThis(self.entries["Exec"].get()) \
                .UseThisIcon(self.entries["Icon"].get()) \
                .NeedsTerminal(self.use_terminal.get()) \
                .OfTheseCategories(self.entries["Categories"].get().split(";"), [])

            result = builder.Build()
            DesktopEntryBuilder.WriteToFile(result)

            self.output_box.configure(state="normal")
            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", "\n".join(result))
            self.output_box.configure(state="disabled")

        except Exception as e:
            self.output_box.configure(state="normal")
            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", f"Error: {str(e)}")
            self.output_box.configure(state="disabled")


if __name__ == '__main__':
    app = MainWindow()