# Generated by Django 2.2.6 on 2019-11-01 22:36

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('logue', '0003_auto_20191030_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loguepage',
            name='body',
            field=wagtail.core.fields.StreamField([('richtext_section', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('code_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Name of code block.', required=True)), ('code', wagtail.core.blocks.TextBlock(help_text='Text to be rendered as code.', required=True)), ('caption', wagtail.core.blocks.RichTextBlock(help_text='Brief description of code snippet.', required=False))])), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('html', wagtail.core.blocks.RawHTMLBlock()), ('related_content', wagtail.core.blocks.PageChooserBlock()), ('cards', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Card title', required=True)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=79, required=True)), ('text', wagtail.core.blocks.TextBlock(max_length=240, required=True)), ('button_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.core.blocks.URLBlock(help_text='Button page will be used first.', required=False))])))]))], null=True),
        ),
    ]
