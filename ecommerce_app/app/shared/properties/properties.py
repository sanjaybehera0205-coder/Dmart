import configparser
from pymongo import MongoClient
import certifi
from app.shared.common import constants

config = configparser.ConfigParser()


def load_properties(file_path):
    config.read(file_path)


def initialize_sections():
    # print("Sections:", config.sections())

    # ---------------- APP SECTION ----------------
    if config.has_section("app"):
        constants.VALIDATE_ON_STARTUP = config.getboolean("app", "VALIDATE_ON_STARTUP")
        constants.INCLUDE_IN_API_DOCS = config.getboolean("app", "INCLUDE_IN_API_DOCS")
        constants.SHOULD_PROFILE = config.getboolean("app", "SHOULD_PROFILE")

    # ---------------- DATABASE SECTION ----------------
    if config.has_section("database"):
        constants.MONGO_URL = config.get("database", "MONGO_URL")
        constants.DATABASE_NAME = config.get("database", "DATABASE_NAME")

        constants.USER_COLLECTION = config.get("database", "USER_COLLECTION")
        # print(constants.USER_COLLECTION)
        constants.PRODUCT_COLLECTION = config.get("database", "PRODUCT_COLLECTION")
        constants.ORDER_COLLECTION = config.get("database", "ORDER_COLLECTION")
        constants.CATEGORY_COLLECTION = config.get("database", "CATEGORY_COLLECTION")

        # Create Mongo Connection
        client = MongoClient(
            constants.MONGO_URL,
            tls=True,
            tlsCAFile=certifi.where()
        )

        constants.DB = client[constants.DATABASE_NAME]
        # print(constants.DB)

    # ---------------- ROLES SECTION ----------------
    if config.has_section("roles"):
        constants.ADMIN = config.get("roles", "ADMIN")
        constants.CUSTOMER = config.get("roles", "CUSTOMER")
