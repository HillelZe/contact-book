"""
Unit tests for the ContactBook application.

This module contains tests for the core functionality of the ContactBook class,
including adding, replacing, searching, deleting, saving, and loading contacts.

"""
import unittest
import os
import csv
from contact_book import ContactBook


class TestContactBook(unittest.TestCase):
    """Unit tests for the ContactBook class aand its core functionality."""

    def setUp(self):
        """Set up a new ContactBook instance with one default contact before each test."""

        self.book = ContactBook()
        self.book.add_contact("John", "123", "john@email.com")

    def test_add_new_contact(self):
        """Test that the new default contact was added succesfuly."""

        self.assertIn("John", self.book.contacts)
        contact = self.book.contacts["John"]
        self.assertEqual(
            contact.name, "John")
        self.assertEqual(
            contact.phone, "123")
        self.assertEqual(
            contact.email, "john@email.com")

    def test_add_existing_contact_replacement(self):
        """Test replacing an existing contact."""

        self.book.add_contact("John", "999", "replace@email.com")
        contact = self.book.contacts["John"]
        self.assertEqual(
            contact.phone, "999")
        self.assertEqual(
            contact.email, "replace@email.com")

    def test_search_existing_contact(self):
        """Test searching for an existing contact."""

        self.assertEqual(self.book.search_contact("John"),
                         "Name: John, Phone: 123, Email: john@email.com.")

    def test_search_nonexistent_contact(self):
        """Test searching for a contact that does not exist."""

        self.assertEqual(self.book.search_contact("Ron"),
                         "Contact doesn't exist.")

    def test_delete_existing_contact(self):
        """Test deleting an existing contact."""

        self.book.delete_contact("John")
        self.assertEqual(self.book.search_contact("John"),
                         "Contact doesn't exist.")

    def test_delete_nonexistent_contact(self):
        """Test deleting a contact that does not exist."""

        self.assertEqual(self.book.search_contact("Ron"),
                         "Contact doesn't exist.")

    def test_save_to_file(self):
        """Test saving the contact book to a new file."""
        filename = "test.csv"
        self.book.save_to_file(filename)
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        self.assertIn("John,123,john@email.com", content)
        os.remove(filename)

    def test_load_from_file(self):
        """Test loading contacts from an existing file."""
        filename = "test.csv"
        with open(filename, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Ron", "123", "abc@gmail.com"])
        self.book.load_from_file("test.csv")
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(self.book.search_contact("Ron"),
                         "Name: Ron, Phone: 123, Email: abc@gmail.com.")
        os.remove(filename)

    def test_str_empty_contact_book(self):
        """Test __str__ method when contact book is empty."""
        self.book.delete_contact("John")
        self.assertEqual(str(self.book), "No contacts yet.")

    def test_str_non_empty_contact_book(self):
        """Test __str__ method when contact book has contacts."""
        self.assertEqual(
            str(self.book), "1. Name: John, Phone: 123, Email: john@email.com.\n")


if __name__ == '__main__':
    unittest.main()
