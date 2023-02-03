from .order import OrderController
from datetime import datetime
from collections import Counter

class ReportController():

    def fetch_relevant_data_for_report():
        all_orders = OrderController.get_all()
        client_names = []
        order_beverages = []
        order_ingredients = []
        order_sizes = []
        order_dates_and_prices = []

        for order in all_orders[0]:
            client_names.append(order['client_name'])         
            order_sizes.append(order['size']['name'])
            order_dates_and_prices.append({'date': order['date'], 'price': order['total_price']})
            orders_detail = order['detail']
            for i in range(len(orders_detail)):
                if (orders_detail[i]['ingredient']):
                    order_ingredients.append(orders_detail[i]['ingredient']['name'])
                if (orders_detail[i]['beverage']):
                    order_beverages.append(orders_detail[i]['beverage']['name'])

        return client_names, order_sizes, order_beverages, order_ingredients, order_dates_and_prices

    def obtain_the_most_requested_ingredient():
        _, _, _, order_ingredients, _ = ReportController.fetch_relevant_data_for_report()
        most_requested_ingredient = max(set(order_ingredients), key = order_ingredients.count)
        return most_requested_ingredient

    def obtain_the_most_requested_beverage():
        _, _, order_beverages, _, _ = ReportController.fetch_relevant_data_for_report()
        most_requested_beverage = max(set(order_beverages), key = order_beverages.count)
        return most_requested_beverage

    def obtain_the_most_requested_size():
        _, order_sizes, _, _, _ = ReportController.fetch_relevant_data_for_report()
        most_requested_size = Counter(order_sizes).most_common(1)[0][0]
        return most_requested_size
    
    def obtain_the_top_three_clients():
        client_names, _, _, _, _ = ReportController.fetch_relevant_data_for_report()
        counter = Counter(client_names)
        first, second, third = counter.most_common(3)
        top_three_clients = {
            'first': first[0],
            'second': second[0],
            'third': third[0]
        }
        return top_three_clients

    def obtain_the_total_income_for_month(year, month):
        _, _, _, _, order_dates_and_prices = ReportController.fetch_relevant_data_for_report()
        total_income_for_month = 0
        for order in order_dates_and_prices:
            date = None
            if (order['date'].__contains__('.')):
                date = datetime.strptime(order['date'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                date = datetime.strptime(order['date'], '%Y-%m-%dT%H:%M:%S')
            if (date.year == year and date.month == month):
                total_income_for_month += float(order['price'])
        return total_income_for_month

    def obtain_the_month_with_more_revenue(year):
        total_income_for_month = []
        for _ in range(12):
            total_income_for_month.append({'month': _+1, 'total_income': ReportController.obtain_the_total_income_for_month(year, _+1)})

        max_revenue_value = max(total_income_for_month, key = lambda i: i['total_income'])
        
        return max_revenue_value

    def obtain_month_name(month_index):
        months = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        return months[month_index]

    def generate_report():
        try:
            most_requested_ingredient = ReportController.obtain_the_most_requested_ingredient()
            most_requested_beverage = ReportController.obtain_the_most_requested_beverage()
            most_requested_size = ReportController.obtain_the_most_requested_size()
            top_three_clients = ReportController.obtain_the_top_three_clients()
            max_revenue_value_2022 = ReportController.obtain_the_month_with_more_revenue(2022)
            max_revenue_value_2023 = ReportController.obtain_the_month_with_more_revenue(2023)

            report = {
                'most_requested_ingredient': most_requested_ingredient,
                'most_requested_beverage': most_requested_beverage,
                'most_requested_size': most_requested_size,
                'top_three_clients': top_three_clients,
                'max_revenue_value': {
                    '2022': {'month': ReportController.obtain_month_name(max_revenue_value_2022['month']), 'income': max_revenue_value_2022['total_income']},
                    '2023': {'month': ReportController.obtain_month_name(max_revenue_value_2023['month']), 'income': round(max_revenue_value_2023['total_income'], 2)}
                }
            }
            #report = ReportController.fetch_relevant_data_for_report()
            return [report], None
        except Exception as e:            
            return None, e
            
