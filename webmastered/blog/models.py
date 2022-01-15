from django.db import models
from django.shortcuts import render
from django.conf import settings

from blocks.fields import BlogListingPageFields, BlogPostPageFields

from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup

from django_comments_xtd.models import XtdComment

from modelcluster.fields import ParentalKey


class BlogListingPage(RoutablePageMixin, Page, BlogListingPageFields):
    """A model for a blog listing page"""

    template = "blog/blog_listing_page.html"

    # We only need one blog listing page in the website
    max_count = 1

    subpage_types = [
        'blog.BlogPostPage',
    ]

    content_panels = Page.content_panels + BlogListingPageFields.content_panels

    def get_context(self, request, *args, **kwargs):
        """Pass a list of blog post pages as context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPostPage.objects.live().public().order_by('-first_published_at')
        return context

    class Meta:
        verbose_name = "Blog Listing Page"
        verbose_name_plural = "Blog Listing Pages"

    @route(r'^categories/$')
    def category_listing_page(self, request, *args, **kwargs):
        """This handles the category listing pages"""
        context = self.get_context(request, *args, **kwargs)
        categorySlug = request.GET.get('category')
        if categorySlug not in (None,""):
            context = self.get_context(request, *args, **kwargs)
            category = BlogPostCategory.objects.filter(slug=categorySlug)
            if len(category) != 1:
                #If no category model matches with the query...
                context['blog_listing_page'] = BlogListingPage.objects.all()[0]
                context['errorTitle'] = "Category not found"
                context['errorMessage'] = "The category that you're looking for does not exist, please double check your query."
                return render(request, "blog/error_page.html", context)
            # If there is a match with a category model...
            context['blog_listing_page'] = BlogListingPage.objects.all()[0]
            context['posts'] = BlogPostPage.objects.filter(
                categories__in=category
                ).live().public().order_by('-first_published_at')
            context['category'] = category.first
            return render(request, "blog/category_post_listing_page.html", context)
        context['blog_listing_page'] = BlogListingPage.objects.all()[0]
        context['categories'] = BlogPostCategory.objects.all()
        return render(request, "blog/category_listing_page.html", context)



class BlogPostPage(Page, BlogPostPageFields):
    """A model for the blog posts"""

    template = "blog/blog_post_page.html"

    parent_page_type = [
        'blog.BlogListingPage',
    ]

    content_panels = Page.content_panels + BlogPostPageFields.content_panels
    settings_panels = Page.settings_panels + BlogPostPageFields.settings_panels
    promote_panels = Page.promote_panels + BlogPostPageFields.promote_panels


    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def get_absolute_url(self):
        """Get the URL of this model (used for django-comments-xtd)"""
        if settings.DEBUG:
            return 'http://localhost:8000' + self.url
        return self.full_url

    def get_context(self, request, *args, **kwargs):
        """Pass the blog listing page object as a context"""
        context = super().get_context(request, *args, **kwargs)
        context['blog_listing_page'] = BlogListingPage.objects.all()[0]
        return context


class BlogPostCategory(models.Model):
    """A category model to sort blog posts into categories"""

    name = models.CharField(max_length=255, help_text="Name your category.", unique=True)
    slug = models.SlugField(allow_unicode=True, max_length=255, help_text="A slug to identify posts by this category.", unique=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Associate an image with this category."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        ImageChooserPanel("image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Post Category"
        verbose_name_plural = "Blog Post Categories"
        ordering = ["name"]

class BlogPostCategoryAdmin(ModelAdmin):
    model = BlogPostCategory
    list_display = ('name', 'slug')
    menu_label = "Blog Categories"
    menu_icon = "folder-open-inverse"

class BlogPostComment(XtdComment):
    page = ParentalKey(BlogPostPage, on_delete=models.CASCADE, related_name='blog_post_comments')

    class Meta:
        verbose_name = "Blog Post Comment"
        verbose_name_plural = "Blog Post Comments"

    def save(self, *args, **kwargs):
        """Function that defines what happens when a comment is published (saved)"""
        if self.user:
            self.user_name = self.user.username
        self.page = BlogPostPage.objects.get(pk=self.object_pk)
        super(BlogPostComment, self).save(*args, **kwargs)

class BlogPostCommentAdmin(ModelAdmin):
    model = BlogPostComment
    # list_display = ('user', 'comment')
    menu_label = "Blog Post Comments"
    menu_icon = "group"


class BlogAdminGroup(ModelAdminGroup):
    menu_label = 'Blog'
    menu_icon = 'form'
    items = (BlogPostCategoryAdmin,)
    if settings.ENABLE_EXPERIMENTAL_BLOG_COMMENTING:
        items = (BlogPostCategoryAdmin, BlogPostCommentAdmin,)

modeladmin_register(BlogAdminGroup)