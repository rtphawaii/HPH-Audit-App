import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

from .processor import process_excel

ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.xlsm'}
MAX_UPLOAD_MB = 50


def home(request):
    return render(request, 'audit/home.html')


@require_POST
def upload_file(request):
    if 'file' not in request.FILES:
        return JsonResponse({'status': 'error', 'message': 'No file provided.'}, status=400)

    uploaded = request.FILES['file']

    ext = os.path.splitext(uploaded.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JsonResponse(
            {'status': 'error', 'message': f'Invalid file type "{ext}". Please upload an Excel file (.xlsx, .xls, .xlsm).'},
            status=400,
        )

    if uploaded.size > MAX_UPLOAD_MB * 1024 * 1024:
        return JsonResponse(
            {'status': 'error', 'message': f'File exceeds the {MAX_UPLOAD_MB} MB limit.'},
            status=400,
        )

    upload_dir = settings.MEDIA_ROOT / 'uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / uploaded.name

    with open(file_path, 'wb') as f:
        for chunk in uploaded.chunks():
            f.write(chunk)

    result = process_excel(str(file_path))
    return JsonResponse(result)
