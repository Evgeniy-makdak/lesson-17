from bd_utils import *


def menu() -> (str, int):
    """ интерактив с пользователем и формирование соответствующего текста запроса """
    print("доступные действия:")
    print(" 1. показать все объявления")
    print(" 2. показать объявления конкретных пользователей")
    print(" 3. показать объявления в диапазоне цен")
    print(" 4. показать объявления для конкретного города")
    print(" 5. показать информацию для определенного пользователя и цены")
    print(" 6. выход")
    user_input = input("выберите пункт и введите его номер: >>> ")

    req_type = 0  # вид запроса 0-без группировок, 1-с группировками
    match user_input:
        case "1":
            req_text = ""
        case "2":
            user_input = input("введите пользователей через запятую: >>> ")
            list_user_str = []
            for each in user_input.split(','):
                list_user_str.append(f"{each.strip()!r}")
            list_user_str = ",".join(list_user_str)
            req_text = f"\n AND aut.name in ({list_user_str})"
        case "3":
            user_input = input("введите 2 цены через запятую: >>> ")
            user_input = user_input.split(",")
            min_price = min(int(user_input[0].strip()), int(user_input[1].strip()))
            max_price = max(int(user_input[0].strip()), int(user_input[1].strip()))
            req_text = f"\n AND ads.price < {max_price} AND ads.price > {min_price}"
            req_text += f"\n ORDER BY ads.price"
        case "4":
            user_input = input("введите наименование города: >>> ")
            req_text = f"\n AND adr.address LIKE '%{user_input}%'"
        case "5":
            req_text = ""
            req_type = 1 # группировка по пользователю
        case "6":
            return "stop", req_type
        case _:
            return "", req_type

    req_text = get_base_req(req_type) + req_text
    return req_text, req_type  # базовый запрос+условия+сортировка


def get_print(rez: list[tuple], req_type: int) -> None:
    """ красивый вывод результата выполнения запроса """
    print("--результат--")
    num = 0
    if req_type:
        for each in rez:
            num += 1
            print(str(num) + ".", each[0].strip(), ":", str(each[1]).strip())
    else:
        for each in rez:
            num += 1
            print(str(num) + ".", each[1].strip(), ":", each[2],
                  f"--- ({str(each[3]).strip()}: {str(each[4]).strip()})")
            print("   ", str(each[5]).strip().replace('\n', '\n    '))
    print("-" * 20)


def main() -> None:
    """ главный цикл """
    connection = get_connect_bd()  # попытка подключение к бд
    if connection:
        cursor = connection.cursor()  # получение курсора

        while True:
            result = ""
            req_text, req_type = menu()  # вывод меню и ввод пользователя, вернет текст запроса или stop
            if req_text == "stop":
                break
            try:
                cursor.execute(req_text)  # выполнение запроса
                result = cursor.fetchall()
            except:
                print("не удалось выполнить запрос")
                result = ""
            finally:
                get_print(result, req_type)

        disconntct_bd(connection, cursor)  # закрытие курсора и подключения к бд


if __name__ == '__main__':
    main()
