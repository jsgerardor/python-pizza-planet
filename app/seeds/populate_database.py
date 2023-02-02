from ..repositories.managers import BeverageManager, IngredientManager, OrderManager, SizeManager
from ..controllers.order import OrderController
from faker import Faker
import threading

fake = Faker()

ingredients_name_seed = [
    "Shrimps",
    "Salami",
    "Lettuce",
    "Cheese",
    "Ham",
    "Bacon",
    "Chicken",
    "Beef",
    "Pork",
    "Egg",
]

beverages_name_seed = [
    "Coca Cola",
    "Fanta",
    "Sprite",
    "Pepsi",
    "7up",
    "Water",
    "Beer",
    "Wine",
    "Tea",
    "Coffee",
]

sizes_name_seed = [
    "Personal",
    "Small",
    "Medium",
    "Family",
    "Extra Family",
]

def generate_random_price(object):
    if object == "beverage":
        return fake.pyfloat(left_digits=None, right_digits=2, positive=True, min_value=0.75, max_value=5)
    elif object == "ingredient":
        return fake.pyfloat(left_digits=None, right_digits=2, positive=True, min_value=1, max_value=5)
    elif object == "size":
        return fake.pyfloat(left_digits=None, right_digits=2, positive=True, min_value=5, max_value=22)

def populate_random_ingredients():
    for i in range(len(ingredients_name_seed)):
        IngredientManager.create({
            "name": ingredients_name_seed[i],
            "price": generate_random_price('ingredient'),
        })

def populate_random_sizes():
    for i in range(len(sizes_name_seed)):
        SizeManager.create({
            "name": sizes_name_seed[i],
            "price": generate_random_price('size'),
        })

def generate_random_volumes():
    return fake.pyfloat(left_digits=None, right_digits=1, positive=True, min_value=0.5, max_value=3)

def populate_random_beverages():
    for i in range(len(beverages_name_seed)):
        BeverageManager.create({
            "name": beverages_name_seed[i],
            "volume": generate_random_volumes(),
            "price": generate_random_price('beverage'),
        })

def generate_random_dni():
    return fake.random_int(min=1000000000, max=9999999999)

def generate_random_date():
    return fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)

def generate_client_data():
    return {
        "client_name": fake.name(),
        "client_dni": generate_random_dni(),
        "client_address": fake.address(),
        "client_phone": fake.phone_number(),
    }

def obtain_size_for_order():
    size = SizeManager.get_all()
    return size[fake.random_int(min=0, max=len(size) - 1)]["_id"]

def obtain_ingredients_for_order():
    ingredient = IngredientManager.get_all()
    ingredients = []
    for _ in range(fake.random_int(min=1, max=5)):
        ingredients.append(ingredient[fake.random_int(min=0, max=len(ingredient) - 1)]['_id'])
    return ingredients 

def obtain_beverages_for_order():
    beverage = BeverageManager.get_all()
    beverages = []
    for _ in range(fake.random_int(min=0, max=5)):
        beverages.append(beverage[fake.random_int(min=0, max=len(beverage) - 1)]['_id'])
    return beverages

def generate_order_data():
    clients = []
    for _ in range(40):
        clients.append(generate_client_data())

    for _ in range(100):
        size_id = obtain_size_for_order()
        ingredients_ids = obtain_ingredients_for_order()
        beverages_ids = obtain_beverages_for_order()
        size_price = SizeManager.get_by_id(size_id).get('price')
        ingredients = IngredientManager.get_by_id_list(ingredients_ids)
        beverages = BeverageManager.get_by_id_list(beverages_ids)
        total_price = OrderController.calculate_order_price(size_price, ingredients, beverages)
        client = clients[fake.random_int(min=0, max=39)]
        OrderManager.create({
            "client_name": client["client_name"],
            "client_dni": client["client_dni"],
            "client_address": client["client_address"],
            "client_phone": client["client_phone"],
            "date": generate_random_date(),
            "size_id": size_id,
            "total_price": total_price,
        }, ingredients, beverages)

def populate_database():
    try:
        populate_random_ingredients()
        populate_random_sizes()
        populate_random_beverages()
        threading.Timer(1.5, generate_order_data()).start()
        print('The new data was generated successfully')
    except:
        print('An error ocurred while generating the new data')

populate_database()