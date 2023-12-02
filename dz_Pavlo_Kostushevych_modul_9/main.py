def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please provide name and phone."
        except IndexError:
            return "Invalid command format."

    return wrapper

phone_book = {}

@input_error
def add_contact(name, phone_number):
    if not name or not phone_number or not name.isalpha() or not phone_number.isdigit():
        raise ValueError
    phone_book[name] = phone_number
    return f"Contact {name} with phone number {phone_number} added to the phone book."

@input_error
def change_contact(name, new_phone_number):
    if name in phone_book:
        if not new_phone_number.isdigit():
            raise ValueError("New phone number must contain digits only.")
        phone_book[name] = new_phone_number
        return f"Phone number for {name} updated to {new_phone_number}."
    else:
        raise KeyError

@input_error
def phone_contact(name):
    if name in phone_book:
        return f"Phone number for {name}: {phone_book[name]}"
    else:
        raise KeyError

def show_all_contacts():
    if not phone_book:
        return "Phone book is empty."
    else:
        result = "All contacts in the phone book:\n"
        for name, number in phone_book.items():
            result += f"{name}: {number}\n"
        return result.strip()

def exit_program():
    return "Good bye!"

def main():
    while True:
        command = input("\nEnter command: ").lower()

        if command.startswith("hello"):
            print("How can I help you?")
        elif command.startswith("add"):
            args = command.split(" ", 2)
            if len(args) == 3:
                _, name, number = args
                print(add_contact(name, number))
            else:
                print("Invalid command. Please provide name and phone.")
        elif command.startswith("change"):
            args = command.split(" ", 2)
            if len(args) == 3:
                _, name, new_number = args
                print(change_contact(name, new_number))
            else:
                print("Invalid command format. Please provide name and new phone number.")
        elif command.startswith("phone"):
            args = command.split(" ", 1)
            if len(args) == 2:
                _, name = args
                print(phone_contact(name))
            else:
                print("Invalid command. Please provide name.")
        elif command == "show all":
            print(show_all_contacts())
        elif command in ["good bye", "close", "exit", "."]:
            print(exit_program())
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

print(float or int)