# tests if memory is working correctly, by using fibonacci.mem as input
from memory import Memory


def test_memory():
    memory = Memory('fibonacci.mem')
    memory.printAll()


if __name__ == '__main__':
    test_memory()