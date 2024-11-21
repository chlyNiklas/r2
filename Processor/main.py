import api


def get(offset: int):
    return "Hello World"


def post(data):
    print(data)
    return (200, "Okey")


if __name__ == "__main__":
    api.run_api(get, post)
