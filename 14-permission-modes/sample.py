"""A tiny module to edit under each permission mode. Harmless on purpose."""


def add(a, b):
    result=a+b
    return result


def greet(name):
    return "hello "+name


if __name__ == "__main__":
    print(add(2, 3))
    print(greet("world"))
