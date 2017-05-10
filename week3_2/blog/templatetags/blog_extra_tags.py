from django import template
import markdown


register = template.Library()


@register.filter(name='markdown')
def markdown_to_html(text):
    md = markdown.Markdown()
    return md.convert(text)
