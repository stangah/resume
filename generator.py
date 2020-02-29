#! /usr/bin/env python
import argparse
from datetime import datetime
import json
import os
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

INPUT_JSON = "resume.json"
TEMPLATE_FILE = "template.html"
CSS_FILE = "style.css"
OUTPUT_HTML = "index.html"


def simpledate(value):
    """Formats dates as 'Month YYYY'"""
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return parsed.strftime("%B %Y")


if __name__ == "__main__":
    with open(INPUT_JSON, "r") as j:
        loaded = json.load(j)

    with open(CSS_FILE, "r") as c:
        css = c.read()

    env = Environment(loader=FileSystemLoader("."))
    env.filters["simpledate"] = simpledate
    template = env.get_template("template.html")

    compiled = template.render({
        "css": css,
        "resume": loaded
    })

    with open(OUTPUT_HTML, "w") as oh:
        oh.write(compiled)
