import os
from typing import List


class DesktopEntryBuilder:
    header: str = "[Desktop Entry]"
    

    def WithName(self, name: str) -> "DesktopEntryBuilder":
        if name is None or name == '':
            raise Exception("Empty name")

        self.Name : str = name + '\n'
        
        return self
    
    def WithVersion(self, version: str) -> "DesktopEntryBuilder":
        if version is None or version == '':
            raise Exception("Empty version")

        self.Version = version

        return self

    def OfType(self, _type: str) -> "DesktopEntryBuilder":
        if _type is None or _type == '':
            raise Exception("Empty Type")
        
        self.Type = _type

        return self

    def WithComment(self, comment: str) -> "DesktopEntryBuilder":
        if comment is None or comment == '':
            raise Exception("Empty comment")
        
        self.Comment = comment
        return self
    
    def InThisPath(self, path: str)  -> "DesktopEntryBuilder":
        if path is None or path == '':
            raise Exception("Empty Path")
        
        self.Path = path
        return self

    def ExecuteThis(self, _exec: str, *args) -> "DesktopEntryBuilder":
        if _exec is None or _exec == '':
            raise Exception("Empty Executable")
        
        self.Executable = _exec
        self.Args = args
        return self

    def UseThisIcon(self, icon_path: str) -> "DesktopEntryBuilder":
        if icon_path is None or icon_path == '':
            raise Exception("Empty icon")

        self.Icon = icon_path
        return self

    def NeedsTerminal(self, use_terminal: bool) -> "DesktopEntryBuilder":
        self.UseTerminal = use_terminal

        return self
    
    def OfTheseCategories(self, categories: List[str], args) -> "DesktopEntryBuilder":
        if categories is None:
            raise Exception("Empty Categories")

        self.Categories = categories + [arg for arg in args if type(arg) is str]
        return self

    def Build(self) -> List[str]:
        entry = [self.header]

        if hasattr(self, 'Name'):
            entry.append(f"Name={self.Name.strip()}")
        if hasattr(self, 'Version'):
            entry.append(f"Version={self.Version}")
        if hasattr(self, 'Type'):
            entry.append(f"Type={self.Type}")
        if hasattr(self, 'Comment'):
            entry.append(f"Comment={self.Comment}")
        if hasattr(self, 'Path'):
            entry.append(f"Path={self.Path}")
        if hasattr(self, 'Executable'):
            exec_line = self.Executable
            if hasattr(self, 'Args') and self.Args:
                exec_line += ' ' + ' '.join(self.Args)
            entry.append(f"Exec={exec_line}")
        if hasattr(self, 'Icon'):
            entry.append(f"Icon={self.Icon}")
        if hasattr(self, 'UseTerminal'):
            entry.append(f"Terminal={'true' if self.UseTerminal else 'false'}")
        else:
            entry.append("Terminal=false")
        if hasattr(self, 'Categories'):
            entry.append(f"Categories={';'.join(self.Categories)};")

        return entry

    def __str__(self) -> str:
        return "\n".join(self.Build())  
    
    @staticmethod
    def WriteToFile(entry: List[str]) -> None:
        # Try to find the "Name=" line safely
        name_line = next((line for line in entry if line.startswith("Name=")), None)
        if not name_line:
            raise ValueError("Desktop entry is missing 'Name=' field.")
        
        file_name = name_line.split('=', 1)[1].strip()
        file_path = os.path.expanduser(f"~/.local/share/applications/{file_name}.desktop")
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as file:
            file.write("\n".join(entry) + "\n")

        # Optionally make it executable
        os.chmod(file_path, 0o755)

        