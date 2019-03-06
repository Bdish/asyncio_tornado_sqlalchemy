import configparser

def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section("books_db")
    config.set("books_db", "user", "root")
    config.set("books_db", "password", "root")
    config.set("books_db", "host", "localhost")
    config.set("books_db", "database", "books_db")
    config.set("books_db", "port", "3306")

    config.add_section("controllers")
    config.set("controllers", "port", "8002")
    config.set("controllers", "host", "0.0.0.0")

    config.add_section("customer_controllers")
    config.set("customer_controllers", "port", "8003")
    config.set("customer_controllers", "host", "0.0.0.0")

    config.add_section("async_log")
    config.set("async_log", "logfile", "log.log")

    config.add_section("request_info_about_customer")
    config.set("request_info_about_customer", "base_url", "http://localhost:8003")





    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = "config.ini"
    createConfig(path)