"""imports"""
from collections import UserDict

class PhoneValidateError(Exception):
    """Custom exception for validating phone number

    Args:
        Exception (_type_): text of exception
    """
    pass

class Field:
    """Class for storing data of str type"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing names of contacts. Str type of data."""
    pass


class Phone(Field):
    """Class for storing list of phone numbers."""
    def __init__(self, phone: str):
        self.validate_phone(phone)
        super().__init__(phone)

    def validate_phone(self, phone: str) -> None:
        if len(phone) != 10 or not phone.isdigit():
            raise PhoneValidateError('Wrong phone format!')


class Record:
    """Class for storing and computing contact records.
    """
    def __init__(self, contact_name: str):
        self.name = Name(contact_name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, " \
            f"phones: {'; '.join(phone.value for phone in self.phones)}"

    def add_phone(self, phone_number: str) -> None:
        if phone_number in [str(phone) for phone in self.phones]:
            raise ValueError('This phone already in list')
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_number: str, new_number: str):
        try:
            Phone(new_number)
        except ValueError as e:
            print(e)

        for number in self.phones:
            if number.value == old_number:
                number.value = new_number
                break

    def find_phone(self, phone_number: str) -> str:
        for number in self.phones:
            if number.value == phone_number:
                return phone_number

    def remove_phone(self, phone: str) -> None:
        self.phones.remove(self.find_phone(phone))


class AddressBook(UserDict):
    def add_record(self, user_record: Record) -> str:
        if user_record.name.value in self.data:
            return "User already exists"
        self.data[user_record.name.value] = user_record
        return "Contact added"

    def find(self, contact_name: str) -> str:
        return self.data[contact_name]

    def find_by_phone(self, phone_number: str) -> str:
        for name, record in self.data.items():
            if record.find_phone(phone_number):
                return name
        return "No contact found with this phone number"

    def delete(self, contact_name: str) -> str:
        if contact_name not in self.data:
            raise ValueError('Contact not found')
        del self.data[contact_name]
        return "Contact deleted"


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    print("\nrecord of John added with 2 phones:'1234567890', '5555555555'")
    for name, record in book.data.items():
        print(record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("\nrecord of Jane added with 1 phone:'9876543210'")
    for name, record in book.data.items():
        print(record)

    print("\nrecord found by phone number '5555555555'")
    print(book.find_by_phone("5555555555"))
    print("\nrecord found by phone number '9876543210'")
    print(book.find_by_phone("9876543210"))
    print("\nrecord found by phone number '7418529635'")
    print(book.find_by_phone("7418529635"))

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print("\nphone number found in record")
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    print("\nrecord of John edited")
    for name, record in book.data.items():
        print(record)

    book.delete("Jane")

    print("\nrecord of Jane deleted")
    for name, record in book.data.items():
        print(record)
