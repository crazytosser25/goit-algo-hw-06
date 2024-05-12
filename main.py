"""imports"""
from collections import UserDict

class PhoneValidateError(Exception):
    """Custom exception for validating phone number

    Args:
        Exception (_type_): text of exception
    """


class Field:
    """Class for storing data of str type"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing names of contacts. Str type of data."""


class Phone(Field):
    """Class for storing list of phone numbers.
    
    Methods:
        - validate_phone: Validate a phone number format.
    """
    def __init__(self, phone: str):
        self.validate_phone(phone)
        super().__init__(phone)

    def validate_phone(self, phone: str) -> None:
        """Validate a phone number format.

        This method validates the format of a phone number by checking
        its length and whether it consists of digits only. Raises
        PhoneValidateError if the phone number format is incorrect.

        Args:
            phone (str): The phone number to validate.
        """
        if len(phone) != 10 or not phone.isdigit():
            raise PhoneValidateError('Wrong phone format!')


class Record:
    """Class for storing and processing contact records.
    
    Methods:
        - add_phone: Add a phone number to the list of phones.
        - edit_phone: Edit an existing phone number in the list.
        - find_phone: Find a phone number in the list.
        - remove_phone: Remove a phone number from the list.
    """
    def __init__(self, contact_name: str):
        self.name = Name(contact_name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, " \
            f"phones: {'; '.join(phone.value for phone in self.phones)}"

    def add_phone(self, phone_number: str) -> None:
        """Add a phone number to the list of phones.

        This method adds a new phone number to the existing list of phones.
        Raises ValueError if the provided phone number is already in the list.

        Args:
            phone_number (str): The phone number to be added.
        """
        if phone_number in [str(phone) for phone in self.phones]:
            raise ValueError('This phone already in list')
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_number: str, new_number: str):
        """Edit an existing phone number in the list.

        This method allows you to update an existing phone number with 
        a new one in the list of phones.

        Args:
            old_number (str): The current phone number to be replaced.
            new_number (str): The new phone number to replace the old one.
        """
        try:
            Phone(new_number)
        except ValueError as e:
            print(e)

        for number in self.phones:
            if number.value == old_number:
                number.value = new_number
                break

    def find_phone(self, phone_number: str) -> str:
        """Find a phone number in the list.

        This method searches for a given phone number in the list of phones and
        returns it if found.

        Args:
            phone_number (str): The phone number to search for.

        Returns:
            str: The found phone number if it exists in the list;
            otherwise, returns None.
        """
        for number in self.phones:
            if number.value == phone_number:
                return phone_number

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the list.

        This method removes the specified phone number from the list of phones.
        Raises ValueError if the provided phone number does not exist 
        in the list.

        Args:
            phone (str): The phone number to be removed.
        """
        self.phones.remove(self.find_phone(phone))


class AddressBook(UserDict):
    """A simple address book implementation.

    This class extends the UserDict class to manage a collection of contacts.
    Uses classes: Name and Phone (children of Field) to store data, and
    Record to manage phone numbers.

    Args:
        UserDict (_type_): A class from the 'collections' module.

    Methods:
        - add_record: Add a new contact record to the address book.
        - find: Find a contact record by name.
        - find_by_phone: Find a contact record by phone number.
        - delete: Delete a contact record from the address book.
    """
    def add_record(self, user_record: Record) -> str:
        """Add a new contact record to the address book.

        Args:
            user_record (Record): The contact record to be added.

        Returns:
            str: A message indicating the status of the operation.
        """
        if user_record.name.value in self.data:
            return "User already exists"
        self.data[user_record.name.value] = user_record
        return "Contact added"

    def find(self, contact_name: str) -> str:
        """Finding a contact record by name.

        Args:
            contact_name (str): The name of the contact to search for.

        Returns:
            str: The contact record corresponding to the provided name.
        """
        return self.data[contact_name]

    def find_by_phone(self, phone_number: str) -> str:
        """Find a contact record by phone number.

        Args:
            phone_number (str): The phone number to search for.

        Returns:
            str: The name of the contact associated with given phone number.
        """
        for contact_name, phone_record in self.data.items():
            if phone_record.find_phone(phone_number):
                return contact_name
        return "No contact found with this phone number"

    def delete(self, contact_name: str) -> str:
        """Delete a contact record from the address book.

        Args:
            contact_name (str): The name of the contact to be deleted.

        Returns:
            str: A message indicating the status of the operation.
        """
        if contact_name not in self.data:
            return "Contact not found"
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
