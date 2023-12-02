from datetime import datetime, timedelta
from collections import UserDict

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



"""
Test
"""

def run_tests():
    print("--Validation tests:")
    try:
        phone = Phone("123467890")
        print("\033[92mPhone validation passed.\033[0m")  
    except ValueError:
        print("\033[91mPhone validation failed.\033[0m")  

    try:
        birthday = Birthday("1990-01-08")
        print("\033[92mBirthday validation passed.\033[0m")  
    except ValueError:
        print("\033[91mBirthday validation failed.\033[0m")  
    print("\n")

    print("--Record tests:")
    record = Record("John Doe", "1990-01-01")
    record.add_phone("1234567890")
    record.add_phone("1234512350")
    print(f"Record name: {record.name.value}")
    print(f"Record birthday: {record.birthday.value}")
    print(f"Record phones: {[phone.value for phone in record.phones]}")
    
    record1 = Record("John Doe1", "1990-01-01")
    record1.add_phone("1234567890")
    record2 = Record("John Doe2", "1990-01-01")
    record2.add_phone("1234567890")
    record3 = Record("John Doe3", "1990-01-01")
    record3.add_phone("1234567890")
    print("\n")

    print("--Adress book tests:")
    address_book = AddressBook()
    address_book.add_record(record)
    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)

    found_record = address_book.find("John Doe")
    if found_record:
        print("Found record:")
        print(f"Name: {found_record.name.value}")
        print(f"Birthday: {found_record.birthday.value}")
        print(f"Phones: {[phone.value for phone in found_record.phones]}")
    else:
        print("Record not found.")
    print("\n")

    print("--Adress book iteration tests:")
    page_size = 2  
    i=1
    for page_of_records in address_book.iterator(page_size):
        print(f"{i} Page of records:")
        for record in page_of_records:
            print(f"Name: {record.name.value}, Phones: {[phone.value for phone in record.phones]}")
        i+=i


if __name__ == "__main__":
    run_tests()




