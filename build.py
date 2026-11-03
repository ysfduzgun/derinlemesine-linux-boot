import os
import markdown

template = ""
with open("template/template.html", "r") as f:
    template = f.read()

for src in os.listdir("src"):
    with open(f"src/{src}") as f:
         ctx = markdown.markdown(f.read(), extensions=['tables'])
         html_name = src.replace(".md", ".html")
         html_content = template.replace("{content}", ctx)
         html_content = html_content.replace("{title}", src.replace(".md", ""))
         with open(f"build/{html_name}", "w") as g:
             g.write(html_content)