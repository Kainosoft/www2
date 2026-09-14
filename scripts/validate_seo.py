from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from PIL import Image

root = Path(__file__).resolve().parents[1]
pages = {
    "index.html": "https://www.kainosoft.com/",
    "index-es.html": "https://www.kainosoft.com/index-es.html",
    "index-light.html": "https://www.kainosoft.com/",
    "index-light-es.html": "https://www.kainosoft.com/index-es.html",
}

class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta = []; self.links = []; self.scripts = []; self._json_ld = False
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "meta": self.meta.append(data)
        if tag == "link": self.links.append(data)
        if tag == "script" and data.get("type") == "application/ld+json": self._json_ld = True
    def handle_endtag(self, tag):
        if tag == "script": self._json_ld = False
    def handle_data(self, data):
        if self._json_ld: self.scripts.append(data)

for filename, expected_canonical in pages.items():
    parser = HeadParser(); parser.feed((root / filename).read_text())
    canonicals = [link["href"] for link in parser.links if link.get("rel") == "canonical"]
    assert canonicals == [expected_canonical], f"{filename}: canonical {canonicals}"
    alternates = {(link.get("hreflang"), link.get("href")) for link in parser.links if link.get("rel") == "alternate"}
    assert {"en", "es", "x-default"} == {lang for lang, _ in alternates}, f"{filename}: hreflang"
    properties = {meta.get("property"): meta.get("content") for meta in parser.meta if meta.get("property")}
    names = {meta.get("name"): meta.get("content") for meta in parser.meta if meta.get("name")}
    for name in ("og:type", "og:site_name", "og:title", "og:description", "og:url", "og:image", "og:image:width", "og:image:height", "og:image:alt"):
        assert properties.get(name), f"{filename}: missing {name}"
    for name in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
        assert names.get(name), f"{filename}: missing {name}"
    assert properties["og:url"] == expected_canonical, f"{filename}: og:url"
    assert len(parser.scripts) == 1
    schema = json.loads(parser.scripts[0])
    assert {node["@type"] for node in schema["@graph"]} == {"Organization", "WebSite"}

image = Image.open(root / "images/og/kainosoft-og.png")
assert image.size == (1200, 630) and image.format == "PNG"
ET.parse(root / "sitemap.xml")
assert "Sitemap: https://www.kainosoft.com/sitemap.xml" in (root / "robots.txt").read_text()
print("SEO validation passed: 4 pages, OG PNG, robots.txt, sitemap.xml, and JSON-LD.")
