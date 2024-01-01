from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from privateq.config import FILE_DIR
from typing import Dict, List

import os

def path_to_uri(path: str, scheme: str="https://", domain: str=os.environ.get("DOC_DOMAIN")) -> str:
    """Convert a path to a URI."""
    return scheme + domain + str(path).split(domain)[-1]

def extract_txt_from_sec(sec: 'BeautifulSoup') -> str:
    """Extract text from a section of a BeautifulSoup object."""
    txts = []
    for child in sec.children:
        if isinstance(child, NavigableString) and child.strip():
            txts.append(child.strip())
        elif child.name == "section":
            continue
        else:
            txts.append(child.get_text().strip())
    return "\n".join(txts)

def extract_sections(record: Dict[str, str]) -> List[str]:
    """Extract sections from a record."""
    with open(record["path"], "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
    sections = soup.find_all("section")
    section_list = []
    for section in sections:
        section_id = section.get("id")
        section_text = extract_txt_from_sec(section)
        if section_id:
            uri = path_to_uri(path=record["path"])
            section_list.append({"source": f"{uri}#{section_id}", "text": section_text})
    return section_list

def fetch_text(uri):
    url, anchor = uri.split("#") if "#" in uri else (uri, None)
    file_path = Path(FILE_DIR, url.split("https://")[-1])
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    if anchor:
        target_element = soup.find(id=anchor)
        if target_element:
            text = target_element.get_text()
        else:
            return fetch_text(uri=url)
    else:
        text = soup.get_text()
    return text