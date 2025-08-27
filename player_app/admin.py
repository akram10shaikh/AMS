from django.contrib import admin
from player_app.models import *

admin.site.register(Player)
admin.site.register(Player_Group)
admin.site.register(CampTournament)
# admin.site.register(CampParticipant)
admin.site.register(CampActivity)
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_id', 'name', 'program_type', 'template', 'created_by', 'created_at')
    search_fields = ('name', 'program_id')
    list_filter = ('program_type', 'template')

@admin.register(AssignedProgram)
class AssignedProgramAdmin(admin.ModelAdmin):
    list_display = ('program', 'player', 'injury_id', 'assigned_by', 'assigned_at')
    search_fields = ('program__name', 'player__name', 'injury_id')

@admin.register(WorkoutData)
class WorkoutDataAdmin(admin.ModelAdmin):
    list_display = ('assigned_program', 'player', 'created_at')
    search_fields = ('assigned_program__program__name', 'player__name')

admin.register(Injury)

@admin.register(TreatmentRecommendation)
class TreatmentRecommendationAdmin(admin.ModelAdmin):
    list_display = ("injury", "physio", "recovery_time_weeks", "created_at")
    search_fields = ("physio__user__username", "injury__player__name")

admin.site.register(InjuryActivityLog)
admin.site.register(Injury)
admin.site.register(MedicalDocument)
admin.site.register(PlayerActivityLog)
admin.site.register(TestAndResult)
admin.site.register(Team)