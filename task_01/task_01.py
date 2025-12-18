import random
import time
from collections import OrderedDict

# -----------------------------
# Реалізація класу LRUCache
# -----------------------------
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        # Якщо ключ є у кеші — переміщаємо його в кінець (найновіший)
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        # Додаємо новий ключ або оновлюємо існуючий
        self.cache[key] = value
        self.cache.move_to_end(key)
        # Якщо перевищено ємність — видаляємо найстаріший
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# -----------------------------
# Функції без кешу
# -----------------------------
def range_sum_no_cache(array, left, right):
    """Обчислює суму елементів без кешування"""
    return sum(array[left:right+1])

def update_no_cache(array, index, value):
    """Оновлює елемент масиву без кешування"""
    array[index] = value


# -----------------------------
# Функції з кешем
# -----------------------------
cache = LRUCache(capacity=1000)

def range_sum_with_cache(array, left, right):
    """Обчислює суму з використанням LRU-кешу"""
    key = (left, right)
    result = cache.get(key)
    if result == -1:  # cache-miss
        result = sum(array[left:right+1])
        cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    """Оновлює елемент масиву та інвалідовує кеш"""
    array[index] = value
    # Лінійний прохід по ключах кешу для видалення діапазонів, що містять index
    keys_to_delete = []
    for (l, r) in cache.cache.keys():
        if l <= index <= r:
            keys_to_delete.append((l, r))
    for k in keys_to_delete:
        del cache.cache[k]


# -----------------------------
# Генерація запитів
# -----------------------------
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        # ~3% Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% Range
            if random.random() < p_hot:       # 95% «гарячі» діапазони
                left, right = random.choice(hot)
            else:                             # 5% випадкові
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries


# -----------------------------
# Тестування продуктивності
# -----------------------------
def run_no_cache(array, queries):
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(array, q[1], q[2])
        else:
            update_no_cache(array, q[1], q[2])

def run_with_cache(array, queries):
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(array, q[1], q[2])
        else:
            update_with_cache(array, q[1], q[2])


if __name__ == "__main__":
    N = 100_000
    Q = 50_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    # Без кешу
    arr_copy = array[:]  # копія масиву
    start = time.time()
    run_no_cache(arr_copy, queries)
    t_no_cache = time.time() - start

    # З кешем
    arr_copy = array[:]  # нова копія масиву
    start = time.time()
    run_with_cache(arr_copy, queries)
    t_with_cache = time.time() - start

    # Вивід результатів
    print(f"Без кешу : {t_no_cache:.2f} c")
    print(f"LRU-кеш  : {t_with_cache:.2f} c  (прискорення ×{t_no_cache/t_with_cache:.2f})")
