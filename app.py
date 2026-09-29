def calculate_total(price, quantity):
    total = price * quantity
    return total


def divide(a, b):
    return a / b


def find_user(users, name):
    for user in users:
        if user["name"] == name:
            return user

    return None


def process_payment(amount):
    if amount > 0:
        print("Payment processed:", amount)
        return True

    return False


def calculate_discount(price, discount):
    final_price = price - (price * discount / 100)
    return final_price


def get_user_email(user):
    return user["email"]


def send_notification(user, message):
    print("Sending notification to:", user["email"])
    print("Message:", message)


def process_order(user, price, quantity):
    total = calculate_total(price, quantity)

    if total > 1000:
        total = calculate_discount(total, 10)

    print("Order processed for:", user["name"])
    print("Total:", total)

    return total


def search_products(products, keyword):
    results = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            results.append(product)

    return results


def get_average_price(products):
    total = 0

    for product in products:
        total += product["price"]

    return total / len(products)


def authenticate(username, password):
    if username == "admin" and password == "admin123":
        return True

    return False


def update_balance(user, amount):
    user["balance"] = user["balance"] + amount
    return user["balance"]


def transfer_money(sender, receiver, amount):
    if sender["balance"] < amount:
        return False

    sender["balance"] -= amount
    receiver["balance"] += amount

    return True


def generate_report(users):
    report = ""

    for user in users:
        report += (
            user["name"]
            + " : "
            + str(user["balance"])
            + "\n"
        )

    return report


def main():
    users = [
        {
            "name": "Alice",
            "email": "alice@example.com",
            "balance": 5000
        },
        {
            "name": "Bob",
            "email": "bob@example.com",
            "balance": 3000
        }
    ]

    products = [
        {
            "name": "Laptop",
            "price": 60000
        },
        {
            "name": "Mouse",
            "price": 800
        },
        {
            "name": "Keyboard",
            "price": 1500
        }
    ]

    print("Average price:", get_average_price(products))

    user = find_user(users, "Alice")

    if user:
        process_order(user, 1200, 2)

    print(
        "Authentication:",
        authenticate("admin", "admin123")
    )

    transfer_money(
        users[0],
        users[1],
        1000
    )

    print(generate_report(users))


if __name__ == "__main__":
    main()