from datetime import date

client_name = '"ООО Яблоко"'
client_number = '8 800 555 35 35'

designer_name = 'Виктория Викторова'
design_type = 'LOGO'
price = 10000
is_urgent = True
deadline = date(2026, 12, 31)
today = date.today()

def create_order(design_type, designer_name, price, is_urgent, deadline):
    if is_urgent:
        s = 'Срочно'
    else:
        s = 'Не срочно'

    return f"Заказ {design_type} от дизайнера {designer_name} для клиента {client_name} на сумму {price} руб. Срок: {deadline}"

def client(client_name, client_number):
    return f"Контактные данные заказчика {client_name}: {client_number}"

def deadline_soon(deadline):
    diff = (deadline - today).days
    if 0 <= diff <= 7:
        return "Дедлайн скоро!"
    elif diff < 0:
        return "Дедлайн просрочен :("
    else:
        return "Дедлайн нескоро :)"

print(create_order(design_type, designer_name, price, is_urgent, deadline))
print(client(client_name, client_number))
print(deadline_soon(deadline))
