"""
Contact Book Application

A simple contact book that manages contacts by name, phone, and email.
Provides functionality to add, view, search, delete contacts, and persist them in a CSV file.

Author: Hillel Zehavi
Date: 2025-03-31
"""
import csv


class Contact:
    """Represent a simple contact with a name, phone and email."""

    def __init__(self, name: str, phone: str, email: str) -> None:
        """
        Initialize a new Contact object.
        Args:
            name (str): The contact's name.
            phone (str): The contact's phone number.
            email (str): The contact's email address.
        """
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        """Return a string representation of the contact."""
        return f'Name: {self.name}, Phone: {self.phone}, Email: {self.email}.'


class ContactBook:
    """A contact book that storres and manages contacts objects"""

    def __init__(self):
        """Initialize an empty contact book."""
        self.contacts: dict[str, Contact] = {}

    def __str__(self) -> str:
        """
        Return a string listing all contacts in the book.
        If the book is empty, return a message saying so.
        """
        if not self.contacts:
            return "No contacts yet."
        return "\n".join(f"{i+1}. {contact}" for
                         i, contact in enumerate(self.contacts.values())) + "\n"

    def add_contact(self, name: str, phone: str, email: str) -> None:
        """
        Add a new contact to the contact book or replace an existing one.

        Args:
            name (str): Contact's name.
            phone (str): Contact's phone number.
            email (str): Contact's email.
        """
        new_contact: Contact = Contact(name, phone, email)
        self.contacts[name] = new_contact

    def view_content(self) -> str:
        """
        Return the string representation of all contacts.

        Returns:
            str: All contacts or a message if the book is empty.
        """
        return str(self)

    def search_contact(self, name: str) -> str:
        """
        Search for a contact by name.

        Args:
            name (str): Name of the contact to search.

        Returns:
            str: Contact details if found, or an error message.
        """
        if name in self.contacts:
            return str(self.contacts[name])
        else:
            return "Contact doesn't exist."

    def delete_contact(self, name: str) -> None:
        """
        Delete a contact by name.

        Args:
            name (str): The name of the contact to delete.
        """
        if name in self.contacts:
            del self.contacts[name]
            print("Contact deleted.")
        else:
            print("Contact doesn't exist.")

    def load_from_file(self, filename: str) -> None:
        """
        Load contacts from a CSV file.

        Args:
            filename (str): Path to the CSV file to load from.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    # if len(row) == 0:
                    #   continue
                    # info: list[str] = line.strip().split(",")
                    if len(row) != 3:
                        print(f"Invalid line in file: {row}")
                        continue
                    self.add_contact(*row)
        except FileNotFoundError:
            print("Couldn't find older data file.")

    def save_to_file(self, filename: str) -> None:
        """
        Save contacts to a CSV file.

        Args:
            filename (str): Path to the CSV file to write to.
        """
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for contact in self.contacts.values():
                writer.writerow([contact.name, contact.phone, contact.email])


if __name__ == '__main__':
    book = ContactBook()
    book.load_from_file('data.csv')
    while True:
        print('1. Add Contact\n2. View Contacts\n3. Search Contact\n4. Delete Contact\n5. Exit')
        try:
            choice: int = int(input())
        except ValueError:
            print("Invalid choice. Please enter a number between 1-5.")
            continue
        if choice not in range(1, 6):
            print("Invalid choice. Please enter a number between 1-5.")
            continue
        if choice == 1:  # add contact
            replace_choice: int | None = None
            input_name: str = input("Enter Name:").strip()
            if input_name in book.contacts:
                try:
                    replace_choice = int(
                        input("Name already exist. Replace? enter 1, cancel? enter 2:"))
                except ValueError:
                    print("Invalid choice. Canceled addition.")
                    continue
                else:
                    if replace_choice == 2:
                        print("Addition canceled.")
                        continue
                    elif replace_choice != 1:
                        print("Invalid choice. Canceled addition")
                        continue

            input_phone: str = input("Enter phone:").strip()
            input_email: str = input("Enter Email:").strip()
            book.add_contact(input_name, input_phone, input_email)
            if replace_choice == 1:
                print("Contact was replaced.")
            else:
                print("Contact added.")

        elif choice == 2:  # view content
            print(book.view_content())
        elif choice == 3:  # search contact
            search_name = input('Name to search:')
            print(book.search_contact(search_name))
        elif choice == 4:  # delete contact
            delete_name = input('Name to delete:')
            book.delete_contact(delete_name)
        elif choice == 5:  # exit
            book.save_to_file('data.csv')
            break
