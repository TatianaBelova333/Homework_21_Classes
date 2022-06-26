from abc import ABC, abstractmethod


class Storage(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def capacity(self):
        pass

    @abstractmethod
    def add(self, item: str, quantity: int):
        pass

    @abstractmethod
    def remove(self, item: str, quantity: int):
        pass

    @abstractmethod
    def free_space(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Warehouse(Storage):
    def __init__(self, name, capacity: int = 100):
        self._items = {}
        self._capacity = capacity
        self._name = name.upper()
        self._type = "warehouse"

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def items(self):
        return self._items

    @property
    def capacity(self):
        return self._capacity

    @property
    def free_space(self) -> int:
        occupied_space = sum(self.items.values())
        free_space = self.capacity - occupied_space
        return free_space

    def add(self, item: str, quantity: int) -> str:
        if self.is_enough_free_space(quantity, item):
            self.items[item] = self.items.get(item, 0) + quantity
            return f'Deliveryman delivered {quantity} {item} to {self.type.lower()} {self.name}'
        else:
            return f"Not enough space at {self.type.lower()} {self.name}"

    def remove(self, item: str, quantity: int) -> str:
        if item in self.items:
            if self.items[item] > quantity:
                self.items[item] -= quantity
            elif self.items[item] == quantity:
                del self.items[item]
            else:
                return f'Only {self.items[item]} {item} available at {self.type.lower()} {self.name}. Please try ' \
                       f'another request '
            return f'Deliveryman collected {quantity} {item} at {self.type.lower()} {self.name}'
        return f"Item '{item}' is not available at {self.type} {self.name}.\nPlease submit another request"

    def is_enough_free_space(self, quantity: int, item: str | None = None) -> bool:
        return self.free_space >= quantity

    def get_unique_items_count(self) -> int:
        return len(self.items)

    # checks that the item is in stock in required qty
    def item_is_in_stock(self, quantity: int, item: str) -> bool:
        return self.items.get(item, 0) >= quantity

    def __str__(self):
        if self.items:
            all_items = [f'{quantity} {product}' for product, quantity in self.items.items()]
            return f"{self.type.capitalize()} {self.name} contains:\n" + "\n".join(all_items)
        return f"{self.type.capitalize()} {self.name} is empty"


class Shop(Warehouse):
    def __init__(self, name, capacity: int = 20, product_limit=5):
        super().__init__(name, capacity)
        self._items = {}
        self._product_limit = product_limit
        self._type = 'shop'

    @property
    def items(self):
        return self._items

    @property
    def type(self):
        return self._type

    @property
    def product_limit(self):
        return self._product_limit

    @property
    def capacity(self):
        return self._capacity

    def add(self, item: str, quantity: int) -> str:
        return super().add(item, quantity)

    def remove(self, item: str, quantity: int):
        return super().remove(item, quantity)

    @property
    def free_space(self):
        return super().free_space

    def is_enough_free_space(self, quantity: int, item: str | None = None) -> bool:
        return super().is_enough_free_space(quantity) and self.is_within_product_limit(item)

    def is_within_product_limit(self, item: str) -> bool:
        if item in self.items:
            return self.get_unique_items_count() <= self.product_limit
        return self.product_limit >= self.get_unique_items_count() + 1

    def get_unique_items_count(self):
        return super().get_unique_items_count()

    def item_is_in_stock(self, quantity: int, item: str) -> bool:
        return super().item_is_in_stock(quantity, item)

    def __str__(self):
        if self.items:
            all_items = [f'{quantity} {product}' for product, quantity in self.items.items()]
            return f"{self.type.capitalize()} {self.name} contains:\n" + "\n".join(all_items)
        return f"{self.type.capitalize()} {self.name} is empty"


class Request:
    def __init__(self, request: str):
        request = request.split()
        self.from_ = request[4].upper()
        self.to_ = request[6].upper()
        self.amount = int(request[1])
        self.product = request[2]

    def __str__(self):
        return f'Deliver {self.amount} {self.product} from {self.from_} to {self.to_}'

