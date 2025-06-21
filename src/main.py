import json
from rich.live import Live
from rich.markdown import Markdown
from markdown_pdf import MarkdownPdf, Section

from google import genai
from google.genai import types

with open("secrets.json", mode="r") as secrets_file:
    secrets = json.loads(secrets_file.read())

client = genai.Client(api_key=secrets.api_key)

with open("prompt.txt", mode="r") as prompt_file:
    prompt = prompt_file.read()

with open("La prolissanza.pdf", mode="rb") as pdf_file:
    pdf_bytes = pdf_file.read()

response = client.models.generate_content_stream(
    # gemini-2.5-flash has thinking on by default for enhanced accuracy
    # you can adjust it to minimize latency/token usage (refer to documentation)
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(),
    contents=[
        types.Part.from_bytes(
            data=pdf_bytes,
            mime_type="application/pdf",
        ),
        prompt])

text = ""

with Live(Markdown(""), refresh_per_second=8) as live:
    for chunk in response:
        for part in chunk.candidates[0].content.parts:
            if part.text is not None:
                text += part.text

            live.update(Markdown(text))

pdf = MarkdownPdf(toc_level=6, optimize=True)

pdf.add_section(Section(text))

pdf.meta["author"] = "AI"

pdf.save("out.pdf")