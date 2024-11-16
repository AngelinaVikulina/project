from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, CartItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import random
import requests
logger = logging.getLogger(__name__)

# Настройки SMS.ru
SMS_RU_API_KEY = '5F5426CA-B98C-19E0-19C3-C1F7A06DC591'

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_price = data.get('total_price')
            name = data.get('name')
            address = data.get('address')
            phone = data.get('phone')

            # Генерация случайного кода подтверждения
            confirmation_code = random.randint(100000, 999999)

            # Отправка SMS с кодом подтверждения
            response = requests.post(
                'https://sms.ru/sms/send',
                data={
                    'api_id': SMS_RU_API_KEY,
                    'to': phone,
                    'msg': f'Ваш код подтверждения: {confirmation_code}',
                    'json': 1
                }
            )

            response_data = response.json()
            if response_data['status'] == 'OK':
                # Логирование для отладки
                logger.debug(f"Received payment data: {data}")
                logger.debug(f"Confirmation code sent to {phone}: {confirmation_code}")

                # Уменьшение количества блюд в корзине
                user = request.user
                cart_items = CartItem.objects.filter(user=user)
                for cart_item in cart_items:
                    dish = cart_item.dish
                    dish.stock -= cart_item.quantity
                    dish.save()

                # Пример успешного ответа
                return JsonResponse({'success': True, 'message': 'Платеж успешно обработан', 'confirmation_code': confirmation_code})
            else:
                logger.error(f"Error sending SMS: {response_data}")
                return JsonResponse({'success': False, 'message': 'Ошибка при отправке SMS'})

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({'success': False, 'message': 'Ошибка при обработке данных'})

        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return JsonResponse({'success': False, 'message': 'Ошибка при обработке платежа'})

    # Если метод запроса не является POST, возвращаем ошибку
    return HttpResponseBadRequest('Неверный метод запроса')

def menu(request):
    # Получаем все блюда
    all_dishes = Dish.objects.all()
    # Создаем словарь для хранения уникальных блюд
    unique_dishes = {}
    for dish in all_dishes:
        if dish.name not in unique_dishes:
            unique_dishes[dish.name] = dish
    # Преобразуем словарь обратно в список
    dishes = list(unique_dishes.values())
    return render(request, 'menu/menu.html', {'dishes': dishes})

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, dish=dish)

    if not created and cart_item.quantity + 1 > dish.stock:
        return JsonResponse({'success': False, 'message': f'Извините, у нас осталось только {dish.stock} блюд {dish.name}.'})

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.is_ajax():
        return JsonResponse({'success': True})

    return redirect('menu')
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = cart_items.annotate(total=F('quantity') * F('dish__price')).aggregate(Sum('total'))['total__sum'] or 0
    return render(request, 'menu/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')
