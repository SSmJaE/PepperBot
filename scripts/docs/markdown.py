from typing import List


class Markdown:
    def __init__(self, before: str = "", after: str = ""):
        self.before = before
        self.after = after

        self.content = ""

    def render(self):
        return self.before + self.content + self.after

    def title(self, title: str, level: int = 1):
        self.content += f"{'#' * level} {title}\n\n"
        return self

    def text(self, text: str):
        self.content += f"{text}\n\n"
        return self

    def table(self, rows: List[List[str]]):
        string = ""

        for index, row in enumerate(rows):
            if index == 0:
                string += f"|{'|'.join(row)}|\n"
                string += f"|{'|'.join(':---:' for _ in row)}|\n"

            else:
                string += f"|{'|'.join(row)}|\n"

        self.content += f"{string}\n"

        return self

    def code(self, code: str, language: str = ""):
        self.content += f"```{language}\n{code}\n```\n\n"
        return self

    def to_file(self, file_path: str):
        if not file_path.endswith(".md"):
            file_path += ".md"

        with open(file_path, "w", encoding="utf8") as f:
            f.write(self.content)
