#!/Users/raymondyee/.pyenv/versions/myenv/bin/python

# import pasteboard
import pypandoc
import click

from rdhyee_utils.clipboard.macos import GeneralPasteboard, ptypes, PasteboardItem


def escape_non_ascii_html(text):
    result = []
    for char in text:
        if ord(char) > 127:
            result.append(f"&#{ord(char)};")
        else:
            result.append(char)
    return "".join(result)


def ru_md_to_html(md=None):
    """
    if there is string content on the clipboard, convert it to HTML and place it on clipboard
    optionally, pass in the markdown instead of reading text from the clipboard
    """

    pb = GeneralPasteboard()

    if md is None:
        content = pb.get_string(ptypes.String)
    else:
        content = md

    if content:
        html = pypandoc.convert_text(
            content, "html", format="markdown+task_lists+backtick_code_blocks"
        )

        result = pb.set_content(
            [
                PasteboardItem(
                    [
                        (ptypes.HTML, escape_non_ascii_html(html)),
                        (ptypes.String, content),
                    ]
                )
            ]
        )

        # result = pb.set_string(escape_non_ascii_html(html), ptypes.HTML)

        return (result, content, pb.get_string(t=ptypes.HTML))
    else:
        return (False, content, "")


# attribute removal techniaque from
# [Pandoc: Convert Markdown to HTML *without* any HTML attributes - Stack Overflow](https://stackoverflow.com/questions/53403041/pandoc-convert-markdown-to-html-without-any-html-attributes/53412036#53412036)


def ru_html_to_md(html=None):
    pb = GeneralPasteboard()

    if html is None:
        content = pb.get_string(t=ptypes.HTML)
    else:
        content = html

    if content:
        md = pypandoc.convert_text(
            content,
            "markdown+fenced_code_blocks+backtick_code_blocks+intraword_underscores-header_attributes-link_attributes-native_divs-native_spans",
            format="html",
            extra_args=["--lua-filter=remove-attr.lua"],
        )

        # result = pb.set_contents(md, type=pasteboard.String)
        result = pb.set_content([PasteboardItem([(ptypes.String, md)])])
        return (result, content, pb.get_string())
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
    ru_md_to_html(content)


@cli.command()
@click.option(
    "--content", default=None, help="convert content as HTML instead of clipboard"
)
def html_to_md(content):
    ru_html_to_md(content)


if __name__ == "__main__":
    cli()
