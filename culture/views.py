from django.shortcuts import render

def main(request):
    ctx = {'strona': 'culture club'}
    return render(request,'main_culture.html', ctx)
