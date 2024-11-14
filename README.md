# Title: Markdownify

## Summary:
Markdownify is a Python tool that converts Markdown files into HTML, supporting basic Markdown syntax like headers, bold, italics, lists, and links. This project aims to provide an extensible codebase for handling Markdown-to-HTML conversion.

## Objective:
The primary objective is to create a modular Markdown parser that can convert the following Markdown syntax into HTML:
1. Headers (`#` to `######`)
2. Bold and Italics (`**bold**`, `*italic*` or `_italic_`)
3. Unordered and Ordered Lists
4. Links (`[text](url)`)
5. Paragraphs

The program should read a `.md` file as input and generate a `.html` file as output.

## Key Features:
- Support for basic Markdown syntax
- Easy-to-expand, modular functions for each Markdown element
- File input/output handling for `.md` and `.html` files

This is a **bold** test.

## Installation and Setup
1. Clone the repository: `git clone https://github.com/tycrowe/internetify-my-md.git`
2. Navigate into the directory: `cd internetify-my-md`
3. Run the script: `python main.py`

## Usage
Provide an input Markdown file and specify an output HTML file. For example:
```bash
python main.py
```

## Testing
To test this tool, create a sample Markdown file with each supported syntax and check the resulting HTML output for accuracy.

## License
This project is licensed under the MIT License. See the LICENSE file for details.