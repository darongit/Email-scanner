import os
import re
from string import ascii_lowercase


def paths():
    if os.name != "nt": return ["/",]
    drives = []
    for letter in ascii_lowercase:
        tmp = f"{letter}:/"
        if os.path.isdir(tmp):
            drives.append(tmp)
    return drives


email_pattern = re.compile(r"[a-zA-Z0-9_\.-]+@[a-zA-Z0-9_\-\.]+\.[a-z]+")

already_printed_emails = []
to_avoid = ("png", "json", "jpg", "ini")

for path in paths():
    for dir_name, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(dir_name, file)
            if file.split(".")[-1] in ("json", "txt", "ini"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                        for match in re.finditer(email_pattern, text):
                            start, stop = match.span()
                            email = text[start:stop]
                            if not email in already_printed_emails and email.rsplit(".")[-1] not in to_avoid:
                                already_printed_emails.append(email)
                                print(f"{email}\n\t{file_path}\n")
                except UnicodeError as e:
                    # just get another file
                    continue
                except FileNotFoundError as e:
                    # probably python don't have permission to this file
                    continue
                except NotADirectoryError as e:
                    # probably python don't have permission to this direction
                    continue
                except Exception as e:
                    print(e)
                    # pause to see what's happen
                    input("Any key to continue searching...")