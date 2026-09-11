from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'phone', 'created_at', 'has_signature')
    list_filter = ('gender', 'created_at')
    search_fields = ('name', 'phone', 'diagnosis')
    readonly_fields = ('created_at',)

    # సిగ్నేచర్ ఉందో లేదో Admin table లో చూపించడానికి
    def has_signature(self, obj):
        return bool(obj.signature_data)
    has_signature.boolean = True
    has_signature.short_description = 'Signed?'