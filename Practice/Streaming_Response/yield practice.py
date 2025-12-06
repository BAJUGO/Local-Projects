import time

# def function_1_2_3():
#     time.sleep(1)
#     yield "first call"
#     time.sleep(1)
#     yield "second call"
#     time.sleep(1)
#     yield "third call"
#
#
# #! yield делает самый обычный return, с не самым обычным условием - оно не останавливает работу функции, а временно её замораживает. При следующем вызове, мы продолжим с того
# #! места, на котором остановились
#
#
#
#
# for x in function_1_2_3():
#     print(x)
#
# # gen = function_1_2_3()
# #
# # print(next(gen))
# # print(next(gen))
# # print(next(gen))
#
#
#
# #! Потенциально здесь можно вызвать миллиард раз функцию, но мы работаем только в нашем промежутке
# def potentially_infinite_function():
#     num = 0
#     while True:
#         time.sleep(1)
#         yield num
#         num += 1
#
#
#
# gener = potentially_infinite_function()
#
#
# for x in range(5):
#     print(next(gener))
#
#
#
#
# def fibonacci(limit):
#     a, b = 0, 1
#     while a < limit:
#         time.sleep(0.5)
#         yield b
#         a, b = b, a + b
#
#
# for x in fibonacci(10000000):
#     print(x)








#! То есть мы здесь дошли до момента yield - и типа мы отправляем в тот момент, до которого дошли значение при помощи send. Обязательно нужно проскипать до этого значения при
#! помощи yield
def echo():
    while True:
        to_echo = yield
        print(to_echo)


g = echo()

next(g)

g.send("Yayaya cocojambo")



# def evens(numbers):
#     for x in numbers:
#         if not x % 2:
#             yield x
#
#
# g = evens(range(10000))
# for x in g:
#     print(x)



def numbers():
    n = 0
    while True:
        yield n
        n += 1

g = numbers()

print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))