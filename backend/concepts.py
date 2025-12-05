import time

def timer(func: function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.10f} seconds")
        return result
    return wrapper

@timer
def test_function():
    time.sleep(3)
    print("Done")

test_function()

@timer
def add(x:int, y:int):
    return x+y

add(12, 76)