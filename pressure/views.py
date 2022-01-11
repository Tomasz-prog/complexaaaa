from django.shortcuts import render

def main(request):
    print('tutaj jestem')
    ctx = {'strona': 'pomiar ciśnienia'}
    return render(request,'main_pressure.html', ctx)
