"""StreamFields Blocks."""

from wagtail.core.blocks import StructBlock, CharBlock, TextBlock, RichTextBlock


class CodeBlock(StructBlock):
    """Title and block of text to be rendered and highlighted as code."""

    title = CharBlock(required=True, help_text="Name of code block.")
    code = TextBlock(required=True, help_text="Text to be rendered as code.")
    caption = RichTextBlock(
        required=False, help_text="Brief description of code snippet."
    )

    class Meta:
        template = "utils/code_block.html"
        icon = "code"
        label = "Code Block"


class RelatedContentBlock(StructBlock):
    """Block to format related content links."""

    pass

