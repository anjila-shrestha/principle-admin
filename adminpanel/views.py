from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import csv

def dashboard_home(request):
    total = len(dummy_complaints)
    pending = len([c for c in dummy_complaints if c['status'] == 'Pending'])
    in_progress = len([c for c in dummy_complaints if c['status'] == 'In Progress'])
    resolved = len([c for c in dummy_complaints if c['status'] == 'Resolved'])

    context = {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
    }
    return render(request, 'adminpanel/dashboard_home.html', context)
dummy_complaints = [
    {"id": "CMP-2026-0042", "title": "Projector not working in Room 204", "category": "Infrastructure", "department": "Maintenance / estate office", "status": "Pending", "date": "2026-07-14"},
    {"id": "CMP-2026-0041", "title": "Mid-term syllabus not shared in advance", "category": "Academic", "department": "Academic dept / HOD", "status": "In Progress", "date": "2026-07-13"},
    {"id": "CMP-2026-0040", "title": "Water leakage in Hostel Block B", "category": "Hostel & accommodation", "department": "Warden / hostel office", "status": "Pending", "date": "2026-07-13"},
    {"id": "CMP-2026-0039", "title": "Wi-Fi drops every evening in library", "category": "IT & network", "department": "IT support", "status": "Resolved", "date": "2026-07-11"},
]
dummy_complaints[0]['identity'] = {"name": "Aarav Shrestha", "email": "aarav.shrestha@college.edu"}
dummy_complaints[1]['identity'] = {"name": "Priya Karki", "email": "priya.karki@college.edu"}
dummy_complaints[2]['identity'] = {"name": "Sujal Gurung", "email": "sujal.gurung@college.edu"}
dummy_complaints[3]['identity'] = {"name": "Nisha Thapa", "email": "nisha.thapa@college.edu"}

revealed_ids = set()
audit_log = []

def all_complaints(request):
    search = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    sort_order = request.GET.get('sort', 'newest')

    results = dummy_complaints

    if search:
        results = [c for c in results if search.lower() in c['title'].lower()]

    if status_filter:
        results = [c for c in results if c['status'] == status_filter]

    results = sorted(results, key=lambda c: c['date'], reverse=(sort_order == 'newest'))

    context = {
        'complaints': results,
        'search': search,
        'status_filter': status_filter,
        'sort_order': sort_order,
    }
    return render(request, 'adminpanel/all_complaints.html', context)
def analytics(request):
    total = len(dummy_complaints)

    status_counts = {}
    for c in dummy_complaints:
        status_counts[c['status']] = status_counts.get(c['status'], 0) + 1

    department_counts = {}
    for c in dummy_complaints:
        department_counts[c['department']] = department_counts.get(c['department'], 0) + 1

    status_data = []
    for status, count in status_counts.items():
        percent = round((count / total) * 100) if total else 0
        status_data.append({'status': status, 'count': count, 'percent': percent})

    department_data = []
    for dept, count in department_counts.items():
        percent = round((count / total) * 100) if total else 0
        department_data.append({'department': dept, 'count': count, 'percent': percent})

    context = {
        'total': total,
        'status_data': status_data,
        'department_data': department_data,
    }
    return render(request, 'adminpanel/analytics.html', context)
dummy_users = [
    {"id": 1, "name": "Mr. Rajesh Sharma", "email": "rajesh.sharma@college.edu", "role": "HOD - Academic", "status": "Active"},
    {"id": 2, "name": "Mrs. Sunita Rai", "email": "sunita.rai@college.edu", "role": "Warden - Hostel", "status": "Active"},
    {"id": 3, "name": "Mr. Bikash Thapa", "email": "bikash.thapa@college.edu", "role": "IT Support", "status": "Active"},
    {"id": 4, "name": "Ms. Kavita Shrestha", "email": "kavita.shrestha@college.edu", "role": "Library Staff", "status": "Inactive"},
]

def user_management(request):
    return render(request, 'adminpanel/user_management.html', {'users': dummy_users})
def get_complaint(complaint_id):
    for c in dummy_complaints:
        if c['id'] == complaint_id:
            return c
    return None

def complaint_detail(request, complaint_id):
    complaint = get_complaint(complaint_id)
    is_revealed = complaint_id in revealed_ids
    return render(request, 'adminpanel/complaint_detail.html', {
        'complaint': complaint,
        'is_revealed': is_revealed,
    })

def reveal_identity(request, complaint_id):
    complaint = get_complaint(complaint_id)

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if len(reason) >= 20:
            revealed_ids.add(complaint_id)
            audit_log.append({
                'complaint_id': complaint_id,
                'by': 'Principal (You)',
                'reason': reason,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            })
            return redirect('complaint_detail', complaint_id=complaint_id)
        else:
            error = "Reason must be at least 20 characters."
            return render(request, 'adminpanel/reveal_identity.html', {'complaint': complaint, 'error': error})

    return render(request, 'adminpanel/reveal_identity.html', {'complaint': complaint})

def audit_log_view(request):
    return render(request, 'adminpanel/audit_log.html', {'entries': reversed(audit_log)})
def reports(request):
    total = len(dummy_complaints)
    resolved = len([c for c in dummy_complaints if c['status'] == 'Resolved'])
    pending = len([c for c in dummy_complaints if c['status'] == 'Pending'])
    resolution_rate = round((resolved / total) * 100) if total > 0 else 0

    category_counts = {}
    for c in dummy_complaints:
        category_counts[c['category']] = category_counts.get(c['category'], 0) + 1

    category_data = []
    for cat, count in category_counts.items():
        percent = round((count / total) * 100) if total else 0
        category_data.append({'category': cat, 'count': count, 'percent': percent})

    context = {
        'total': total,
        'resolved': resolved,
        'pending': pending,
        'resolution_rate': resolution_rate,
        'category_data': category_data,
        'generated_on': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    return render(request, 'adminpanel/reports.html', context)


def export_complaints_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="complaints_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Category', 'Department', 'Status', 'Date'])
    for c in dummy_complaints:
        writer.writerow([c['id'], c['title'], c['category'], c['department'], c['status'], c['date']])

    return response