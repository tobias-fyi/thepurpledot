"""StreamFields Blocks."""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class CodeBlock(blocks.StructBlock):
    """Title and block of text to be rendered and highlighted as code."""

    title = blocks.CharBlock(required=True, help_text="Name of code block.")
    code = blocks.TextBlock(required=True, help_text="Text to be rendered as code.")
    caption = blocks.RichTextBlock(
        required=False, help_text="Brief description of code snippet."
    )

    class Meta:
        template = "utils/code_block.html"
        icon = "code"
        label = "Code Block"


class CardBlock(blocks.StructBlock):
    """Cards with an image, a blurb of text, and a button each."""

    title = blocks.CharBlock(required=True, help_text="Card title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=100)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False, help_text="Button page will be used first."
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "utils/card_block.html"
        icon = "placeholder"
        label = "Graph Cards"


class RelatedContentBlock(blocks.StructBlock):
    """Block to format related content links."""

    pass

