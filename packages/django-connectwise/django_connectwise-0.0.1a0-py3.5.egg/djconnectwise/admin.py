# -*- coding: utf-8 -*-


from django.contrib import admin
from .models import TicketStatus, ServiceTicket, Member, Company


class TicketStatusAdmin(admin.ModelAdmin):
    model = TicketStatus
    list_display = ('status_id', 'status_name')
    search_fields = ['status_name']


class MemberAdmin(admin.ModelAdmin):
    model = Member


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('id', 'company_name', 'company_identifier', 'type', 'status')
    list_filter = ('status',)
    search_fields = ['company_name', 'company_identifier']


class ServiceTicketAdmin(admin.ModelAdmin):
    model = ServiceTicket
    list_display = ('summary', 'status', 'technicians', 'record_type',)
    list_filter = ('status','record_type',)
    search_fields = [ 'id','summary', 'members__user__username',]

    def technicians(self, obj):
        return ', '.join([str(m) for m in obj.members.all()])

admin.site.register(TicketStatus, TicketStatusAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ServiceTicket, ServiceTicketAdmin)
admin.site.register(Company, CompanyAdmin)
