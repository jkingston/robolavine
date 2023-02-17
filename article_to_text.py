import html2text
import re


def convert(html):
    lines = []
    found_body = False
    for line in html.splitlines():
        if "<strong>Programming note:" in line or line.startswith("<h2"):
            found_body = True
        if line.startswith("<h2") and "Things happen" in line:
            found_body = False
        if found_body:
            lines.append(line)

    html = '\n'.join(lines)

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.ignore_tables = True
    h.body_width = 0

    text = h.handle(html)

    lines = []
    for line in text.splitlines():
        line = line.lstrip(">#* ")
        line = re.sub("\[[0-9]+\]", "", line)
        lines.append(line)

    text = '\n'.join(lines)

    return text


if __name__ == "__main__":
    title = "The SEC Cracks Down on Crypto"

    with open(f"{title}.html", "r") as f:
        html = f.read()

    text = convert(html)

    with open(f"{title}.txt", "w") as f:
        f.write(text)
