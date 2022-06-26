from storage import Warehouse, Shop, Request


def main():
    # Create Warehouse instances
    warehouse_1 = Warehouse(name='W-1')
    warehouse_1.add(item="cookies", quantity=10)
    warehouse_1.add(item="cookies", quantity=7)
    warehouse_1.add(item="ice_creams", quantity=15)
    warehouse_1.add(item="doughnuts", quantity=20)
    warehouse_1.add(item="chocolates", quantity=50)

    warehouse_2 = Warehouse(name='W-2')
    warehouse_2.add(item="candies", quantity=10)
    warehouse_2.add(item="waffles", quantity=14)
    warehouse_2.add(item="cokes", quantity=14)

    # Create list of warehouses
    warehouses = [warehouse_1, warehouse_2]

    # Creates Shop instances
    shop_1 = Shop(name='S-1')
    shop_1.add(item="candies", quantity=5)
    shop_1.add(item="doughnuts", quantity=3)
    shop_1.add(item='waffles', quantity=5)

    shop_2 = Shop(name='S-2')
    shop_2.add(item="chocolates", quantity=2)
    shop_2.add(item="doughnuts", quantity=3)

    # Create list of shops
    shops = [shop_1, shop_2]

    # All storage facilities
    facilities = warehouses + shops

    while True:
        user_request = input('Please enter your request in the following format: '
                             '"Deliver {quantity} {product} from '
                             '{origin name} to {destination name}"')
        # For testing
        # Deliver 100 cookies from W-1 to S-1
        # Deliver 3 candies from W-2 to S-1
        # Deliver 5 candies from W-1 to S-1
        # Deliver 5 cokes from W-1 to S-1
        # Deliver 20 cookies from W-1 to S-1
        # Deliver 5 candies from S-1 to W-2
        # Deliver 5 candies from S-2 to W-2
        # Deliver 2 chocolates from S-2 to W-2
        try:
            req = Request(user_request)
            origin = [facility for facility in facilities if facility.name == req.from_][0]
            destination = [facility for facility in facilities if facility.name == req.to_][0]
        except Exception:
            print('Invalid request')
            continue
        if not origin.item_is_in_stock(item=req.product, quantity=req.amount):
            print(origin.remove(item=req.product, quantity=req.amount))
        elif not destination.is_enough_free_space(item=req.product, quantity=req.amount):
            print(destination.add(item=req.product, quantity=req.amount))
        else:
            print(origin.remove(item=req.product, quantity=req.amount))
            print(destination.add(item=req.product, quantity=req.amount))
            print()
            print(origin)
            print(destination)
        another_request = input('Would you like to try another request?').lower()
        if another_request.startswith('ye'):
            continue
        else:
            print('Request completed')
            break


if __name__ == "__main__":
    main()
