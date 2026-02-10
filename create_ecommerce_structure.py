import os

PROJECT_NAME = "ecommerce_app"

folders = [
    "app",
    "app/core",
    "app/models",
    "app/schemas",
    "app/routes",
    "app/services",
    "app/utils",
    "app/tests",
]

files = {
    "run.py": "",
    ".env": "",
    "requirements.txt": "",
    "README.md": "# E-Commerce Application\n",

    "app/main.py": "",
    "app/core/config.py": "",
    "app/core/database.py": "",
    "app/core/security.py": "",
    "app/core/settings.py": "",

    "app/models/user_model.py": "",
    "app/models/product_model.py": "",
    "app/models/cart_model.py": "",
    "app/models/order_model.py": "",

    "app/schemas/user_schema.py": "",
    "app/schemas/product_schema.py": "",
    "app/schemas/cart_schema.py": "",
    "app/schemas/order_schema.py": "",

    "app/routes/auth_routes.py": "",
    "app/routes/user_routes.py": "",
    "app/routes/product_routes.py": "",
    "app/routes/cart_routes.py": "",
    "app/routes/order_routes.py": "",

    "app/services/auth_service.py": "",
    "app/services/user_service.py": "",
    "app/services/product_service.py": "",
    "app/services/cart_service.py": "",
    "app/services/order_service.py": "",

    "app/utils/response.py": "",
    "app/utils/validators.py": "",

    "app/tests/test_auth.py": "",
    "app/tests/test_products.py": "",
    "app/tests/test_orders.py": "",
}


def create_project():
    os.makedirs(PROJECT_NAME, exist_ok=True)
    os.chdir(PROJECT_NAME)

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)

    print("✅ E-commerce project structure created successfully!")


if __name__ == "__main__":
    create_project()
