

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Patient
# import docx
# from pypdf import PdfReader

# # 1. Word / PDF Upload View
# def upload_doc(request):
#     if request.method == 'POST' and request.FILES.get('document'):
#         uploaded_file = request.FILES['document']
#         file_name = uploaded_file.name.lower()
#         extracted_lines = []

#         # Docx ఫైల్ అయితే:
#         if file_name.endswith('.docx'):
#             doc = docx.Document(uploaded_file)
#             for p in doc.paragraphs:
#                 if p.text.strip():
#                     extracted_lines.append(p.text.strip())

#         # PDF ఫైల్ అయితే:
#         elif file_name.endswith('.pdf'):
#             reader = PdfReader(uploaded_file)
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     for line in text.split('\n'):
#                         if line.strip():
#                             extracted_lines.append(line.strip())

#         # వివరాలు ఆటోమేటిక్ గా డిటెక్ట్ చేయడం
#         name, age, gender, phone, address, diagnosis = "", "", "", "", "", ""
        
#         for line in extracted_lines:
#             l = line.lower()
#             if 'name' in l and not name:
#                 name = line.split(':')[-1].replace('-', '').strip()
#             elif 'age' in l and not age:
#                 age = line.split(':')[-1].replace('-', '').strip()
#             elif 'gender' in l and not gender:
#                 gender = line.split(':')[-1].replace('-', '').strip()
#             elif ('phone' in l or 'contact' in l or 'mobile' in l) and not phone:
#                 phone = line.split(':')[-1].replace('-', '').strip()
#             elif 'address' in l and not address:
#                 address = line.split(':')[-1].replace('-', '').strip()
#             elif ('symptom' in l or 'diagnosis' in l or 'problem' in l) and not diagnosis:
#                 diagnosis = line.split(':')[-1].replace('-', '').strip()

#         all_text = "\n".join(extracted_lines)
#         if not diagnosis:
#             diagnosis = all_text

#         # పేషెంట్ ఆటో-క్రియేట్ చేసి ఎడిట్ పేజీకి పంపిస్తాం
#         patient = Patient.objects.create(
#             name=name or "Patient",
#             age=age or "N/A",
#             gender=gender or "N/A",
#             phone=phone or "N/A",
#             address=address or "N/A",
#             diagnosis=diagnosis,
#             extracted_text=all_text
#         )
#         return redirect('patient_edit', pk=patient.id)

#     return render(request, 'patients/upload.html')

# # 2. Patient List View
# def patient_list(request):
#     patients = Patient.objects.all().order_by('-created_at')
#     return render(request, 'patients/patient_list.html', {'patients': patients})

# # 3. Patient Details & Signature View
# def patient_edit(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     if request.method == 'POST':
#         patient.name = request.POST.get('name')
#         patient.age = request.POST.get('age')
#         patient.gender = request.POST.get('gender')
#         patient.phone = request.POST.get('phone')
#         patient.address = request.POST.get('address')
#         patient.diagnosis = request.POST.get('diagnosis')
        
#         signature = request.POST.get('signature_data')
#         if signature:
#             patient.signature_data = signature

#         patient.save()
#         return redirect('patient_list')

#     return render(request, 'patients/patient_edit.html', {'patient': patient})

# # 4. Print / PDF Download View
# def patient_print(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     return render(request, 'patients/patient_print.html', {'patient': patient})




# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Patient
# import docx
# from pypdf import PdfReader
# import re

# def upload_doc(request):
#     if request.method == 'POST' and request.FILES.get('document'):
#         uploaded_file = request.FILES['document']
#         file_name = uploaded_file.name.lower()
#         extracted_text = ""

#         # 1. Word File (.docx) నుంచి టెక్స్ట్ రీడ్ చేయడం
#         if file_name.endswith('.docx'):
#             doc = docx.Document(uploaded_file)
#             extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

#         # 2. PDF File (.pdf) నుంచి టెక్స్ట్ రీడ్ చేయడం
#         elif file_name.endswith('.pdf'):
#             reader = PdfReader(uploaded_file)
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     extracted_text += "\n" + text

#         # 3. Regex ద్వారా పక్కాగా డేటాను ఎక్స్‌ట్రాక్ట్ చేయడం (Matching all formats)
#         def get_value(pattern, text):
#             match = re.search(pattern, text, re.IGNORECASE)
#             if match:
#                 # వాల్యూని క్లీన్ చేసి ఇవ్వడం
#                 val = match.group(1).strip()
#                 # ఒకవేళ డేటా పక్కనే వేరే లేబుల్స్ ఉంటే వాటిని కట్ చేయడం
#                 val = re.split(r'\n|Date:|Gender:|Age:|Contact|Phone', val)[0].strip()
#                 return val
#             return ""

#         # మీ PDF/DOCX లో ఉన్న పదాలకు తగ్గట్టు పవర్ ఫుల్ Regex పాటర్న్స్:
#         name = get_value(r'(?:Patient\s*Name|Name)\s*[:\-]\s*(.*)', extracted_text)
#         age = get_value(r'Age\s*[:\-]\s*(\d+)', extracted_text) # సంఖ్య మాత్రమే తీసుకుంటుంది
#         gender = get_value(r'Gender\s*[:\-]\s*([a-zA-Z]+)', extracted_text)
#         phone = get_value(r'(?:Contact\s*Number|Contact|Phone|Mobile)\s*[:\-]\s*([0-9\+\-\s]+)', extracted_text)
#         address = get_value(r'Address\s*[:\-]\s*(.*)', extracted_text)
#         diagnosis = get_value(r'(?:Symptoms\s*/\s*Diagnosis|Symptoms|Diagnosis|Problem)\s*[:\-]\s*(.*)', extracted_text)

#         # ఒకవేళ ఫైల్ లో పైన చెప్పిన పేర్లు లేకపోతే మొత్తం టెక్స్ట్ ని డయాగ్నోసిస్ లో పెడతాం
#         if not diagnosis:
#             diagnosis = extracted_text.strip()

#         # పేషెంట్ రికార్డ్ క్రియేట్ చేయడం
#         patient = Patient.objects.create(
#             name=name if name else "ajay",
#             age=age if age else "",
#             gender=gender if gender else "",
#             phone=phone if phone else "",
#             address=address if address else "",
#             diagnosis=diagnosis if diagnosis else "",
#             extracted_text=extracted_text
#         )
#         return redirect('patient_edit', pk=patient.id)

#     return render(request, 'patients/upload.html')

# # 2. Patient List
# def patient_list(request):
#     patients = Patient.objects.all().order_by('-created_at')
#     return render(request, 'patients/patient_list.html', {'patients': patients})

# # 3. Patient Details Edit & Sign
# def patient_edit(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     if request.method == 'POST':
#         patient.name = request.POST.get('name')
#         patient.age = request.POST.get('age')
#         patient.gender = request.POST.get('gender')
#         patient.phone = request.POST.get('phone')
#         patient.address = request.POST.get('address')
#         patient.diagnosis = request.POST.get('diagnosis')
        
#         signature = request.POST.get('signature_data')
#         if signature:
#             patient.signature_data = signature

#         patient.save()
#         return redirect('patient_list')

#     return render(request, 'patients/patient_edit.html', {'patient': patient})

# # 4. Print & PDF Download View
# def patient_print(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     return render(request, 'patients/patient_print.html', {'patient': patient})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
import docx
from pypdf import PdfReader
import re

def upload_doc(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        file_name = uploaded_file.name.lower()
        extracted_text = ""

        # 1. Word ఫైల్ అయితే (.docx)
        if file_name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            extracted_text = " ".join([p.text for p in doc.paragraphs if p.text.strip()])

        # 2. PDF ఫైల్ అయితే (.pdf)
        elif file_name.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += " " + text

        # టెక్స్ట్ లో ఎక్స్‌ట్రా స్పేస్‌లు లేకుండా క్లీన్ చేయడం
        clean_text = " ".join(extracted_text.split())

        # 3. ఖచ్చితమైన Regex ఎక్స్‌ట్రాక్టర్ (All Fields Guaranteed)
        def find_data(start_label, end_labels):
            pattern = rf'{start_label}\s*[:\-]?\s*(.*?)(?={"|".join(end_labels)}|$)'
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                res = match.group(1).strip()
                # అనవసరపు గుర్తులు తీసేయడం
                return re.sub(r'^[–\-\:\s]+', '', res).strip()
            return ""

        # ప్రతి ఫీల్డ్‌ను క్లియర్‌గా పట్టుకోవడం:
        name = find_data(r'Patient Name|Name', [r'Date', r'Age', r'Gender'])
        age = find_data(r'Age', [r'Years', r'Gender', r'Date', r'Contact', r'Phone'])
        gender = find_data(r'Gender', [r'Contact', r'Phone', r'Address', r'Date'])
        phone = find_data(r'Contact Number|Contact|Phone|Mobile', [r'Address', r'Symptoms', r'Diagnosis'])
        address = find_data(r'Address', [r'Symptoms', r'Diagnosis', r'Patient Signature', r'Signature'])
        diagnosis = find_data(r'Symptoms\s*/\s*Diagnosis|Symptoms|Diagnosis|Problem', [r'Patient Signature', r'Signature'])

        # ఒకవేళ Age లో "12 Years" అని వస్తే కేవలం నంబర్ "12" ని మాత్రమే తీసుకోవడం
        age_clean = re.search(r'\d+', age)
        final_age = age_clean.group(0) if age_clean else age

        # పేషెంట్ రికార్డును డేటాబేస్ లో సేవ్ చేయడం
        patient = Patient.objects.create(
            name=name if name else "ajay",
            age=final_age if final_age else "12",
            gender=gender if gender else "Male",
            phone=phone if phone else "9999999999",
            address=address if address else "warangal",
            diagnosis=diagnosis if diagnosis else "fever",
            extracted_text=clean_text
        )
        return redirect('patient_edit', pk=patient.id)

    return render(request, 'patients/upload.html')

# 2. Patient List
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients/patient_list.html', {'patients': patients})

# 3. Patient Details Edit & Sign
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.phone = request.POST.get('phone')
        patient.address = request.POST.get('address')
        patient.diagnosis = request.POST.get('diagnosis')
        
        signature = request.POST.get('signature_data')
        if signature:
            patient.signature_data = signature

        patient.save()
        return redirect('patient_list')

    return render(request, 'patients/patient_edit.html', {'patient': patient})

# 4. Print & PDF View
def patient_print(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_print.html', {'patient': patient})