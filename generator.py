#! /usr/bin/env python
import argparse
from datetime import datetime
import json
import os
import shutil
import webbrowser

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell

INPUT_JSON = "resume.json"
TEMPLATE_FILE = "template.html"
CSS_FILE = "style.css"
OUTPUT_HTML = "index.html"


def simpledate(value):
    """Formats dates as 'Month YYYY'"""
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return parsed.strftime("%B %Y")


def generate():
    with open(INPUT_JSON, "r") as j:
        loaded = json.load(j)

    with open(CSS_FILE, "r") as c:
        css = c.read()

    env = Environment(loader=FileSystemLoader("."))
    env.filters["simpledate"] = simpledate
    env.globals['now'] = datetime.utcnow
    template = env.get_template("template.html")

    compiled = template.render({
        "css": css,
        "resume": loaded
    })

    with open(OUTPUT_HTML, "w") as oh:
        oh.write(compiled)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()

    if args.watch:
        server = Server()
        server.watch(INPUT_JSON, generate)
        server.watch(TEMPLATE_FILE, generate)
        server.watch("style.css", generate)
        webbrowser.open_new_tab("http://localhost:5500/")
        server.serve(root='index.html', live_css=False)
    else:
        generate()
