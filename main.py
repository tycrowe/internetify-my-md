import re


class Section:
    def __init__(self, header_text, section_text):
        self.header_text = header_text.strip()
        self.section_text = section_text

    def parse_header_to_html(self):
        size = self.header_text[0:6].count('#')
        return f"<h{size}>{self.header_text[size:]}</h{size}>"

    def parse_lists_to_html(self, ordered=True):
        if ordered:
            list_items = re.findall(r"(\d.)", self.section_text, re.M)
            list_item_indexes = [(match.start(0), match.end(0)) for match in
                                 re.finditer(r"\d\.(.*)", self.section_text, re.M)]
            list_item_text = re.findall(r"\d\.(.*)", self.section_text)
        else:
            list_items = re.findall(r"(-\s)", self.section_text, re.M)
            list_item_indexes = [(match.start(0), match.end(0)) for match in
                                 re.finditer(r"-\s(.*)", self.section_text, re.M)]
            list_item_text = re.findall(r"-\s(.*)", self.section_text)

        if len(list_items) > 2:
            list_html = "<ol>" if ordered else "<ul>"
            for match in list_item_text:
                list_html = f"{list_html}\n<li>{match}</li>"
            list_html = list_html + ("</ol><br>\n" if ordered else "</ul><br>\n")

            # Replace all the list content with
            first_index = list_item_indexes[0][0]
            last_index = list_item_indexes[len(list_item_indexes) - 1][1]
            self.section_text = self.section_text[:first_index] + list_html + self.section_text[last_index + 1:]
            return True

        return None


    def parse_bolds(self):
        bold_matches = re.finditer(r"(?<!`)\*\*(\w+)\*\*", self.section_text, re.M)
        for match in bold_matches:
            self.section_text = self.section_text[:match.start(0)] + f"<b>{match.group(1)}</b> " + self.section_text[match.end(0) + 1:]

    def parse_underlines(self):
        bold_matches = re.finditer(r"(?<!`)_(\w+)_", self.section_text, re.M)
        for match in bold_matches:
            self.section_text = self.section_text[:match.start(0)] + f"<u>{match.group(1)}</u> " + self.section_text[match.end(0) + 1:]

    def parse_italics(self):
        bold_matches = re.finditer(r"(?<!`)\*(\w+)\*", self.section_text, re.M)
        for match in bold_matches:
            self.section_text = self.section_text[:match.start(0)] + f"<i>{match.group(1)}</i> " + self.section_text[match.end(0) + 1:]

    def to_html(self):
        while True:
            if not self.parse_lists_to_html():
                break

        while True:
            if not self.parse_lists_to_html(ordered=False):
                break

        self.parse_bolds()
        self.parse_italics()
        self.parse_underlines()

        return f"""
        <section>
            {self.parse_header_to_html()}
            <br>
            <p>
                {self.section_text}
            </p>
        </section>
        """

    def __str__(self):
        return f"\nHeader text:\n\n{self.header_tag}\nSection text:\n\n{self.section_text}"


def get_sections(markdown_text) -> list[Section]:
    """
    Sections are blocks that begin with a header of '#'s, ranging from # to ######.
    We want to process the entire markdown, and return a "htmlized" section for each header block.
    :return: A list of [<div><h#></h#><p>{section_text}</p></div>]
    """
    sections = []

    header_tags = re.finditer("^(#{1,6}.+)$", markdown_text, re.M)
    # Fetch the index of each header tag
    header_tags_indexes = [(match.start(0), match.end(0)) for match in header_tags]
    # Get all the text between each section
    for i, index_pair in enumerate(header_tags_indexes):
        if i + 1 < len(header_tags_indexes):
            text_of_section = markdown_text[index_pair[1]:header_tags_indexes[i + 1][0]]
        else:
            text_of_section = markdown_text[index_pair[1]:]
        sections.append(Section(markdown_text[index_pair[0]:index_pair[1]], text_of_section))

    return sections


def convert_md_to_html(input_file_path, title) -> str:
    html_text = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
"""

    with open(input_file_path, 'r') as markdown_file:
        markdown_text = markdown_file.read()
        sections = get_sections(markdown_text)

        # Now that each is broken up by section, we can process the text of each section, replacing the markdown with
        #   html a bit easier.
        for section in sections:
            html_text = f"{html_text}{section.to_html()}"

    return html_text + "</body></html>"

def get_file_path(prompt, max_attempts=3, default="", forced_suffix="") -> str:
    file_path = ""
    attempts = 0
    while len(file_path) == 0:
        file_path = input(f"{prompt}: ").strip()
        attempts += 1

        if attempts >= max_attempts:
            file_path = f"{default}"
            break

    if forced_suffix not in file_path:
        file_path = f"{file_path}.{forced_suffix}"

    return file_path


if __name__ == '__main__':
    input_file = get_file_path(
        "Enter the filesystem path to the markdown file",
        max_attempts=1,
        default="./README",
        forced_suffix="md"
    )

    output_file = get_file_path(
        "Enter the filesystem path for outputting the html",
        max_attempts=1,
        default="./readme-to",
        forced_suffix="html"
    )

    print(f"Converting {input_file} to {output_file}.")

    converted_text = convert_md_to_html(input_file, "Internetified!")

    with open(output_file, "w") as out:
        out.write(converted_text)