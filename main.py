import sys
import os
from src.api_adapter import APIAdapter
from src.aeroplanes import Aeroplanes
from src.json_saver import JSONSaver


def clear_screen():
    """Очищает экран консоли"""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Пауза перед продолжением"""
    input("\n▶️ Нажмите Enter, чтобы продолжить...")


def user_interaction():
    """Главная функция взаимодействия с пользователем"""
    api = APIAdapter()
    storage = JSONSaver()

    while True:
        clear_screen()
        print("=" * 60)
        print("Добро пожаловать в программу мониторинга самолетов!")
        print("=" * 60)

        print("\nВыберите действие:")
        print("1. Получить данные о самолетах по стране (из API)")
        print("2. Показать все сохраненные самолеты")
        print("3. Показать топ N самолетов по высоте")
        print("4. Показать самолеты по стране регистрации")
        print("5. Очистить все данные")
        print("0. Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        elif choice == "1":
            country = input("Введите название страны: ").strip()
            if not country:
                print("Название страны не может быть пустым")
                pause()
                continue

            try:
                print(f"Получение данных для страны '{country}'...")

                bounds = api.get_country_bounds(country)
                if bounds is None:
                    pause()
                    continue

                raw_data = api.get_aircraft(bounds)
                if raw_data is None:
                    print("Не удалось получить данные о самолетах")
                    pause()
                    continue

                states = raw_data.get("states") or []
                if not states:
                    print(f"В воздушном пространстве '{country}' нет самолетов")
                    pause()
                    continue

                max_aeroplanes = 300
                total = len(states)
                print(f"Всего в воздушном пространстве: {total} самолетов")

                if total > max_aeroplanes:
                    states = states[:max_aeroplanes]
                    print(f"Для обработки взято только {max_aeroplanes} самолетов")

                aeroplanes = Aeroplanes.from_api_data(states)
                print(f"Получено самолетов: {len(aeroplanes)}")

                storage.add_aeroplanes(aeroplanes)
                print(f"Данные сохранены в {storage.file_path}")

            except Exception as e:
                print(f"Ошибка: {e}")
            pause()

        elif choice == "2":
            all_planes = storage.get_all_aeroplanes()

            if not all_planes:
                print("Нет сохраненных данных. Сначала получите данные (пункт 1)")
            else:
                print(f"\nВСЕ СОХРАНЕННЫЕ САМОЛЕТЫ ({len(all_planes)}):")
                print("-" * 60)
                for i, plane in enumerate(all_planes, 1):
                    print(f"{i}. {plane}")
            pause()

        elif choice == "3":
            all_planes = storage.get_all_aeroplanes()

            if not all_planes:
                print("Нет сохраненных данных. Сначала получите данные (пункт 1)")
                pause()
                continue

            try:
                n = int(input("Введите количество самолетов для топа: ").strip())
                if n <= 0:
                    print("Число должно быть положительным")
                    pause()
                    continue

                sorted_planes = sorted(
                    all_planes,
                    key=lambda plane: plane.baro_altitude if plane.baro_altitude is not None else 0,
                    reverse=True,
                )
                top_n = sorted_planes[:n]

                print(f"\nТОП {len(top_n)} САМОЛЕТОВ ПО ВЫСОТЕ:")
                print("-" * 60)
                for i, plane in enumerate(top_n, 1):
                    print(f"{i}. {plane}")

            except ValueError:
                print("Введите корректное число")
            pause()

        elif choice == "4":
            country = input("Введите страну регистрации для фильтрации: ").strip()
            if not country:
                print("Название страны не может быть пустым")
                pause()
                continue

            filtered = storage.get_aeroplanes_by_country(country)

            if not filtered:
                print(f"Самолеты из страны '{country}' не найдены")
            else:
                print(f"\nСАМОЛЕТЫ ИЗ СТРАНЫ '{country.upper()}':")
                print("-" * 60)
                for i, plane in enumerate(filtered, 1):
                    print(f"{i}. {plane}")
            pause()

        elif choice == "5":
            confirm = input("Вы уверены, что хотите удалить все данные? (да/нет): ").strip().lower()
            if confirm == "да":
                storage.clear_all()
                print("Все данные удалены")
            else:
                print("Отменено")
            pause()

        else:
            print("Неверный выбор. Попробуйте снова.")
            pause()


if __name__ == "__main__":
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        sys.exit(1)
