from django.contrib import admin

from .models import Message, Dispatch, DispatchError, Subscription


class DispatchInlineAdmin(admin.TabularInline):

    model = Dispatch
    extra = 0
    raw_id_fields = ('recipient',)
    readonly_fields = ('retry_count',)


class DispatchErrorInlineAdmin(admin.TabularInline):

    model = DispatchError
    extra = 0
    readonly_fields = ('time_created', 'dispatch', 'error_log')


class MessageAdmin(admin.ModelAdmin):

    list_display = ('time_created', 'cls', 'dispatches_ready')
    list_filter = ('cls', 'dispatches_ready')
    ordering = ('-time_created',)

    inlines = (DispatchInlineAdmin,)


class DispatchAdmin(admin.ModelAdmin):

    list_display = ('time_created', 'dispatch_status', 'address', 'time_dispatched', 'messenger', 'retry_count')
    list_filter = ('dispatch_status', 'messenger')
    ordering = ('-time_created',)
    raw_id_fields = ('recipient',)
    readonly_fields = ('retry_count',)

    inlines = (DispatchErrorInlineAdmin,)


class DispatchErrorAdmin(admin.ModelAdmin):

    list_display = ('time_created', 'dispatch')
    ordering = ('-time_created',)
    readonly_fields = ('time_created', 'dispatch', 'error_log')


class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('time_created', 'message_cls', 'messenger_cls')
    ordering = ('-time_created',)
    readonly_fields = ('time_created',)
    list_filter = ('message_cls', 'messenger_cls')


admin.site.register(Message, MessageAdmin)
admin.site.register(Dispatch, DispatchAdmin)
admin.site.register(DispatchError, DispatchErrorAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
