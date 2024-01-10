import markdown
import os

from django.http import HttpResponse


def home(request):
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")

    with open(readme_path, "r") as readme_file:
        readme_content = readme_file.read()

    markdown_content = markdown.markdown(readme_content)

    return HttpResponse(markdown_content)
