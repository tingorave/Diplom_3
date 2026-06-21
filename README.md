# Автотесты для UI Stellar Burgers

Этот проект содержит автоматизированные UI-тесты для веб-приложения [Stellar Burgers](https://stellarburgers.education-services.ru/).

Тесты написаны на Python с использованием Selenium и паттерна Page Object.

---

## Что проверяется

### Основная функциональность

- переход по клику на «Конструктор»;
- переход по клику на раздел «Лента заказов»;
- если кликнуть на ингредиент, появляется всплывающее окно с деталями;
- всплывающее окно закрывается кликом по крестику;
- при добавлении ингредиента в заказ счётчик этого ингредиента увеличивается.

### Раздел «Лента заказов»

- при создании нового заказа счётчик «Выполнено за всё время» увеличивается;
- при создании нового заказа счётчик «Выполнено за сегодня» увеличивается;
- после оформления заказа его номер появляется в разделе «В работе».

---

## Структура проекта

```text
Diplom_3
├── pages/              # Page Object (майн-пейдж, лента заказов, базовый класс)
│   ├── base_page.py
│   ├── main_page.py
│   ├── orders_feed_page.py
├── tests/              # Тесты
│   ├── test_counters.py
│   ├── test_navigation.py
│   ├── test_smoke.py
├── conftest.py         # Фикстуры (driver для Chrome и Firefox)
├── pytest.ini          # Настройки pytest
├── requirements.txt    # Зависимости Python
├── allure-results      # Результаты Allure-отчёта
├── README.md           # Этот файл
```

---

## Требования

- Python 3.11+
- Chrome и Firefox (для запуска тестов)
- Java (для Allure Report)

### Установка Java

1. Скачать JDK (например, JDK 26) с официального сайта Oracle или Adoptium.
2. Установить JDK.
3. Настроить переменные среды:

   - `JAVA_HOME` = `C:\Program Files\Java\jdk-26.0.1`
   - В `PATH` добавить: `C:\Program Files\Java\jdk-26.0.1\bin`

4. Проверить:

   ```bash
   java -version
   ```

### Установка Allure

1. Скачать Allure (например, через scoop: `scoop install allure`, или вручную).
2. Проверить:

   ```bash
   allure --version
   ```

---

## Установка зависимостей Python

```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

В `requirements.txt`:

```text
selenium
pytest
allure-pytest
webdriver-manager
```

---

## Запуск тестов

1. Активировать виртуальное окружение:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Запустить тесты в **Chrome и Firefox**:

   ```powershell
   pytest -v
   ```

   Фикстура `driver` в `conftest.py` параметризована по браузерам:

   ```python
   @pytest.fixture(params=["chrome", "firefox"])
   def driver(request):
       ...
   ```

   Поэтому каждый тест выполнится в двух браузерах.

3. Запустить тесты с генерацией Allure-отчёта для обоих браузеров:

   ```powershell
   pytest -v --alluredir=allure-results
   ```

4. Открыть Allure-отчёт:

   ```powershell
   allure serve allure-results
   ```

В отчёте будут результаты тестов:
- для Chrome;
- для Firefox.

---

## Page Object

Для упрощения поддержки тестов использован паттерн **Page Object**:

- `MainPage` — описывает главную страницу (конструктор, логин, переход к ленте заказов);
- `OrdersFeedPage` — описывает ленту заказов (счётчики, список «В работе»);
- `BasePage` — базовый класс с общими методами:
  - `open()` — открыть страницу;
  - `find()` — найти элемент;
  - `find_all()` — найти все элементы;
  - `click()` — кликнуть по элементу;
  - `get_text()` — получить текст элемента.

Тесты читаются как сценарий:

```python
main = MainPage(driver)
main.open_main()
main.login("user@example.com", "password")
main.drag_first_ingredient_to_constructor()
main.click_order_button()
```

---

## Allure Report

Отчёт генерируется через `allure-pytest`:

1. Запустить тесты с параметром:

   ```bash
   pytest -v --alluredir=allure-results
   ```

2. Открыть отчёт:

   ```bash
   allure serve allure-results
   ```

В отчёте отображаются:
- статус тестов (PASSED/FAILED) для Chrome и Firefox;
- шаги тестов;
- история запусков;
- графики (status chart, trends).
