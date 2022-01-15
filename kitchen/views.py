from django.shortcuts import render, HttpResponse, redirect
from .forms import ShoppingItems
from django.contrib import messages

from django.contrib import messages

from twilio.rest import Client


def formularz(request):


    if request.method == 'POST':
        form = ShoppingItems(request.POST)
        if form.is_valid():

            print('Form is valid')
            produkt1= request.POST['product1'],
            produkt2= request.POST['product2'],
            produkt3= request.POST['product3'],
            produkt4= request.POST['product4'],
            produkt5= request.POST['product5'],




            produkty = f"{produkt1} \n {produkt2} \n {produkt3}" \
                       f"{produkt4} \n {produkt5}"


            account_sid = 'AC28138893eac709bc0f3c1965b9d3e1cf'
            auth_token = 'd20c0315056b6151dd3ebed3dcd0a831'
            client = Client(account_sid, auth_token)
            wiadomosc = produkty
            tomek = '+48533199400'
            iwona = '+48668025701'



            weight = request.POST.getlist('weight')
            if weight == ['Ivona']:
                klient = "Iwona"
                message = client.messages \
                    .create(
                    body=wiadomosc,
                    from_='+19378979581',
                    to=iwona
                )

            elif weight == ['Tomek']:
                klient = "Tomek"
                message = client.messages \
                    .create(
                    body=wiadomosc,
                    from_='+19378979581',
                    to=tomek
                )

            else:
                klient = "Iwona i Tomek"
                message = client.messages \
                    .create(
                    body=wiadomosc,
                    from_='+19378979581',
                    to=iwona
                )
                message = client.messages \
                    .create(
                    body=wiadomosc,
                    from_='+19378979581',
                    to=tomek
                )
            messages.success(request, f"Wiadmość została wysłana do {klient}.")
            return render(request, "glowna.html")
            #

    else:
        form = ShoppingItems()


    return render(request, 'main_zakupy.html', {'form': form})