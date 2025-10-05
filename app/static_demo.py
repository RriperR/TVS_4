# 1. Неиспользуемый импорт
import json

# 2. Слишком длинная строка
very_long_line = "x" * 160

# 3. Bare except
try:
    1 / 0
except:
    pass

# 4. Изменяемый аргумент по умолчанию
def append_item(x: list = []):
    x.append(1)
    return x

# 5. Неиспользуемая переменная
def foo():
    tmp = 42
    return 0
