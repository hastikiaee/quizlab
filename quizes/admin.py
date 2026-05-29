import nested_admin
from users.models import UserProfile
from django.contrib import admin
from .models import Quiz, Question, Option, QuizResult, ReportCard, UserAnswer


# -------------------
# UserProfile
# -------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')   # بستگی به فیلدهای UserProfile داره
    search_fields = ('user__username',)


# -------------------
# Quiz + Question + Option
# -------------------
class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 0
    max_num = 4

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 0
    inlines = [OptionInline]

@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'date', 'time')
    search_fields = ('title',)
    inlines = [QuestionInline]


# -------------------
# UserAnswer (جواب‌های کاربر به سوالات)
# -------------------
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz_result', 'option', 'is_correct_display')
    search_fields = ('quiz_result__user__username', 'quiz_result__quiz__title', 'option__question__title')
    list_filter = ('quiz_result__quiz',)

    def is_correct_display(self, obj):
        return obj.option.is_answer
    is_correct_display.short_description = 'درست بود؟'
    is_correct_display.boolean = True


# -------------------
# QuizResult
# -------------------
@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'time', 'rank')
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('quiz',)


# -------------------
# ReportCard
# -------------------
@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'time', 'rank')
    search_fields = ('user__username',)
    actions = ['update_selected_reportcards']

    def update_selected_reportcards(self, request, queryset):
        for reportcard in queryset:
            reportcard.update_score()
            reportcard.update_time()
            reportcard.update_rank()
        self.message_user(request, "کارنامه‌های انتخاب شده بروزرسانی شدند.")
    update_selected_reportcards.short_description = "بروزرسانی کارنامه‌های انتخاب شده"
