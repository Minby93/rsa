import random
from math import gcd
import tkinter as tk
from tkinter import messagebox

# Функция для вычисления модуля
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:  # Если степень нечетная
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Функция для нахождения обратного по модулю
def mod_inverse(e, phi):
    original_phi = phi
    x0, x1 = 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + original_phi if x1 < 0 else x1

# Проверка числа на простоту
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Генерация случайного простого числа
def generate_prime_candidate(length):
    candidate = random.getrandbits(length)
    candidate |= (1 << length - 1) | 1
    return candidate

def generate_prime_number(length=8):
    candidate = generate_prime_candidate(length)
    while not is_prime(candidate):
        candidate = generate_prime_candidate(length)
    return candidate

# Генерация ключей RSA
def generate_keys(keysize=8):
    p = generate_prime_number(keysize)
    q = generate_prime_number(keysize)
    while p == q:
        q = generate_prime_number(keysize)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

# Функция шифрования
def encrypt(public_key, plaintext):
    e, n = public_key
    return [mod_exp(ord(char), e, n) for char in plaintext]

# Функция расшифровки
def decrypt(private_key, ciphertext):
    d, n = private_key
    return ''.join([chr(mod_exp(char, d, n)) for char in ciphertext])

# Интерфейс tkinter
def generate_keys_ui():
    global public_key, private_key
    public_key, private_key = generate_keys(16)
    pub_key_label.config(text=f"Публичный ключ: {public_key}")
    priv_key_label.config(text=f"Приватный ключ: {private_key}")
    messagebox.showinfo("Успех", "Ключи успешно сгенерированы!")

def encrypt_ui():
    plaintext = text_entry.get()
    if not plaintext:
        messagebox.showwarning("Ошибка", "Введите сообщение для шифрования!")
        return
    ciphertext = encrypt(public_key, plaintext)
    Res.delete(1.0, tk.END)
    Res.insert(tk.END, ' '.join(map(str, ciphertext)))

def decrypt_ui():
    ciphertext = text_entry.get()
    if not ciphertext:
        messagebox.showwarning("Ошибка", "Введите зашифрованное сообщение для расшифровки!")
        return
    try:
        ciphertext_list = list(map(int, ciphertext.split()))
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат зашифрованного сообщения!")
        return
    plaintext = decrypt(private_key, ciphertext_list)
    Res.delete(1.0, tk.END)
    Res.insert(tk.END, plaintext)

# Глобальные переменные для ключей
public_key, private_key = None, None

# Настройка окна tkinter
root = tk.Tk()
root.title("RSA Шифрование")

# Поля ввода и кнопки
text_label = tk.Label(root, text="Введите сообщение:")
text_label.grid(row=0, column=0, padx=5, pady=5)
text_entry = tk.Entry(root, width=50)
text_entry.grid(row=0, column=1, padx=5, pady=5)

pub_key_label = tk.Label(root, text="Публичный ключ: Не сгенерирован")
pub_key_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
priv_key_label = tk.Label(root, text="Приватный ключ: Не сгенерирован")
priv_key_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

generate_keys_button = tk.Button(root, text="Сгенерировать ключи", command=generate_keys_ui)
generate_keys_button.grid(row=3, column=0, columnspan=2, pady=10)

encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_ui)
encrypt_button.grid(row=4, column=0, pady=5)
decrypt_button = tk.Button(root, text="Расшифровать", command=decrypt_ui)
decrypt_button.grid(row=4, column=1, pady=5)

result_label = tk.Label(root, text="Результат:")
result_label.grid(row=5, column=0, padx=5, pady=5)
Res = tk.Text(root, height=5, width=50)
Res.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()
