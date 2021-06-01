from django.contrib import admin
from .models import UserProfile, Project, Mail, BlogPost, Comment, ReviewReply, CommentReply, Review, TopProject, PostLike, ProjectLike
from django.utils.http import urlencode
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.sites.models import Site

# admin.site.register([UserProfile, Project])

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title')

@admin.register(TopProject)
class TopProjectAdmin(admin.ModelAdmin):
    list_display = ('project',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'university', 'college', 'programme')

@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('email_subject','to_all','sent','send_email_link')

    def send_email_link(self, obj):
        current_site = Site.objects.get_current()

        url = "http://{}".format(current_site.domain)+str(obj.id)+"/send_email/"
        if obj.sent == False:
            return format_html('<a href="{}">send email</a>', url)
        return  format_html('<label>sent</label>', url)

    send_email_link.short_description = "action"
    
@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_post')

@admin.register(ProjectLike)
class ProjectLikeAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_project')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_project')

@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_review')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','author','date_created')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_post')

@admin.register(CommentReply)
class CoommentReviewAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_comment')

