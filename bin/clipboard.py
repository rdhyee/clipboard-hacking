#!/Users/raymondyee/.pyenv/versions/myenv/bin/python

import pasteboard
import pypandoc
import click


STRING_TYPES = (
    pasteboard.String,
    pasteboard.RTF,
    pasteboard.HTML,
    pasteboard.TabularText,
)
BINARY_TYPES = (pasteboard.PDF, pasteboard.PNG, pasteboard.TIFF)


def pb_contents():
    pb = pasteboard.Pasteboard()
    contents = {}

    for t in STRING_TYPES + BINARY_TYPES:
        content = pb.get_contents(type=t)
        if content:
            contents[t] = content

    return contents


def pb_md_to_html(md=None):
    """
    if there is string content on the clipboard, convert it to HTML and place it on clipboard
    optionally, pass in the markdown instead of reading text from the clipboard
    """

    pb = pasteboard.Pasteboard()

    if md is None:
        content = pb.get_contents(type=pasteboard.String)
    else:
        content = md

    if content:
        html = pypandoc.convert_text(
            content, "html", format="markdown+task_lists+backtick_code_blocks"
        )

        # extra_args=['-s']
        result = pb.set_contents(html.encode("utf-8"), type=pasteboard.HTML)
        return (result, content, pb.get_contents(type=pasteboard.HTML))
    else:
        return (False, content, "")


# attribute removal techniaque from
# [Pandoc: Convert Markdown to HTML *without* any HTML attributes - Stack Overflow](https://stackoverflow.com/questions/53403041/pandoc-convert-markdown-to-html-without-any-html-attributes/53412036#53412036)


def pb_html_to_md(html=None):
    pb = pasteboard.Pasteboard()

    if html is None:
        content = pb.get_contents(type=pasteboard.HTML)
    else:
        content = html

    if content:
        md = pypandoc.convert_text(
            content,
            "markdown+fenced_code_blocks+backtick_code_blocks+intraword_underscores-header_attributes-link_attributes-native_divs-native_spans",
            format="html",
            extra_args=["--atx-headers", "--lua-filter=remove-attr.lua"],
        )

        result = pb.set_contents(md, type=pasteboard.String)
        return (result, content, pb.get_contents(type=pasteboard.String))
    else:
        return (False, content, "")


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    pass
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@click.option(
    "--content", default=None, help="convert content as markdown instead of clipboard"
)
def md_to_html(content):
    pb_md_to_html(content)


@cli.command()
@click.option(
    "--content", default=None, help="convert content as HTML instead of clipboard"
)
def html_to_md(content):
    pb_html_to_md(content)


if __name__ == "__main__":
    cli()
