from datetime import datetime, timedelta
from collections import UserDict
import pickle
import atexit

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not (isinstance(self.value, str) and self.value.isdigit() and len(self.value) == 10):
            raise ValueError("Incorrect phone number format")

    @Field.value.setter
    def value(self, new_value):
        super(Phone, Phone).value.__set__(self, new_value)
        self.validate_phone()

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect birthday format")

    @Field.value.setter
    def value(self, new_value):
        super(Birthday, Birthday).value.__set__(self, new_value)
        self.validate_birthday()

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = next((p for p in self.phones if p.value == old_phone), None)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, *map(int, self.birthday.value.split('-'))).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split('-'))).date()
            return (next_birthday - today).days
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        records = list(self.data.values())
        total_records = len(records)
        current_page = 0

        while current_page < n and current_page * n < total_records:
            start_index = current_page * n
            end_index = (current_page + 1) * n
            yield records[start_index:end_index]
            current_page += 1


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(self.dump)

    def dump(self, filename="address_book.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load(self, filename="address_book.pkl"):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Starting with an empty address book.")

    def search(self, query):
        results = []
        for record in self.data.values():
            if (
                query.lower() in record.name.value.lower()
                or query in [phone.value for phone in record.phones]
            ):
                results.append(record)
        return results

if __name__ == "__main__":
    address_book = AddressBook()

    address_book.load()

    # record1 = Record("Pavlo Kostushevych", "1990-05-15")
    # record1.add_phone("1234567890")
    # address_book.add_record(record1)

    # record2 = Record("Serhii Sternenko", "1985-10-25")
    # record2.add_phone("9876543210")
    # address_book.add_record(record2)

    search_query = input("Enter search query: ")
    search_results = address_book.search(search_query)

    if search_results:
        print("\nSearch Results:")
        for result in search_results:
            print(f"{result.name.value}: {', '.join([phone.value for phone in result.phones])}")
    else:
        print("No matching records found.")



