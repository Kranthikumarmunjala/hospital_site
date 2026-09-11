from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientForm

# 1. పేషెంట్ ఫారమ్ సబ్మిట్ చేయడానికి
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})

# 2. పేషెంట్ల లిస్ట్ మొత్తం చూడటానికి
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients/patient_list.html', {'patients': patients})

# 3. పేషెంట్ వివరాలు ఎడిట్ చేసి సంతకం (Signature) పెట్టడానికి
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        signature = request.POST.get('signature_data')
        
        if form.is_valid():
            updated_patient = form.save(commit=False)
            if signature: 
                updated_patient.signature_data = signature
            updated_patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_edit.html', {'form': form, 'patient': patient})

# 4. వివరాలు ప్రింట్ / PDF డౌన్‌లోడ్ చేయడానికి
def patient_print(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_print.html', {'patient': patient})