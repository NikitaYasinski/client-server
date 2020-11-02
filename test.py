alpha = 'абвгдеежзийклмнопрстуфхцчшщъюьэюя'
n = int(input("Ключ:"))
s = input("Введите текст для зашифрования:").rstrip()
res = ''
for c in s:
   res += alpha[(alpha.index(c) + n) % len(alpha)]
print('Результат: ' + res)