from django import forms
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index

from utils.blocks import CodeBlock


@register_snippet
class LogueAuthor(models.Model):
    """Logue author for snippets."""

    name = models.CharField(max_length=140)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [FieldPanel("name"), ImageChooserPanel("image")], heading="Name and Image"
        ),
        MultiFieldPanel([FieldPanel("website")], heading="Links"),
    ]

    def __str__(self):
        """String repr to define format for returned data."""
        return self.name

    class Meta:
        verbose_name = "Logue Author"
        verbose_name_plural = "Logue Authors"


class LogueIndexPage(Page):
    """Index of all individual Logue pages."""

    intro = RichTextField(blank=True)

    def get_context(self, request):
        """Adding custom content and/or config to the context."""
        # Include only published posts, ordered in reverse chron
        context = super().get_context(request)
        # Get all Logue posts
        all_posts = self.get_children().live().public().order_by("-first_published_at")

        # Paginate all Logue posts into 4 per page
        paginator = Paginator(all_posts, 4)

        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and ?page=x is an integer
            logue = paginator.page(page)
        except PageNotAnInteger:
            # If ?page=x is not an integer, return the first page
            logue = paginator.page(1)
        except EmptyPage:
            # If ?page=x is out of range, return the last page
            logue = paginator.page(paginator.num_pages)

        context["logue"] = logue
        return context

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]


class LoguePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "LoguePage", related_name="tagged_items", on_delete=models.CASCADE
    )


class LogueTagIndexPage(Page):
    """Index page that lists all tags."""

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get("tag")
        logue = LoguePage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["logue"] = logue
        return context


@register_snippet
class LogueCategory(models.Model):
    name = models.CharField(max_length=240)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("name"), ImageChooserPanel("icon")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Logue Category"
        verbose_name_plural = "Logue Categories"


class LoguePage(Page):
    date = models.DateField("Post date")
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("richtext_section", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("code_block", CodeBlock()),
            ("embed", EmbedBlock()),
            ("html", blocks.RawHTMLBlock()),
            ("related_content", blocks.PageChooserBlock()),
        ],
        null=True,
    )
    tags = ClusterTaggableManager(through=LoguePageTag, blank=True)
    categories = ParentalManyToManyField("logue.LogueCategory", blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel("logue_authors", label="Author", min_num=1, max_num=6),
                FieldPanel("date"),
                FieldPanel("tags"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Logue information",
        ),
        ImageChooserPanel("header_image"),
        FieldPanel("intro"),
        StreamFieldPanel("body"),
        InlinePanel("gallery_images", label="Gallery images"),
        InlinePanel("related_links", label="Related links"),
    ]

    promote_panels = [ImageChooserPanel("feed_image")]


class LogueAuthorsOrderable(Orderable):
    """Allows selection of one or more authors from Snippets."""

    page = ParentalKey(
        LoguePage, on_delete=models.CASCADE, related_name="logue_authors"
    )
    author = models.ForeignKey("logue.LogueAuthor", on_delete=models.CASCADE)

    panels = [SnippetChooserPanel("author")]


class LoguePageGalleryImage(Orderable):
    page = ParentalKey(
        LoguePage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]


class LoguePageRelatedLink(Orderable):
    page = ParentalKey(
        LoguePage, on_delete=models.CASCADE, related_name="related_links"
    )
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [FieldPanel("name"), FieldPanel("url")]
