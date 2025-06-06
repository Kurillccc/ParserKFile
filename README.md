# ParserKFile

Приложение предназначено для парсинга K-файлов геофизической модели (для программы "ЛОГОС"), проведения расчетов и автоматической генерации CD-файлов. С его помощью можно быстро и без ошибок выделить блоки по element_solid, определить напряженности, сгруппировать их и подготовить данные к моделированию.

## ✨ Функционал

- Чтение и анализ K-файла (сбор элементов по слоям)

- Автоматическое определение и расчет напряженности по каждому element_solid

- Группировка элементов

- Генерация корректного .cd, пригодного для импорта в "ЛОГОС"

- Асинхронная обработка с помощью потоков

- GUI-обёртка для удобного использования

- Поддержка сборки под .app для macOS и .exe для windows

## 📝 Описание

Проект был реализован как практическое задание с целью ускорить работу с K/CD-файлами в программе "ЛОГОС"

Логика работы построена на следующем:

1. Чтение входящего .k файла и сбор узлов (*NODE) и элементов (*ELEMENT_SOLID)

2. Фильтрация элементов по подобласти

3. Выделение "параллелепипеда" от возможного объекта сверху и нахождение высоты грунта ("параллелепипеда")

4. Отбор id слоев по порядку от 0 по координатам

5. Отбор элементов, которые принадлежат слою

6. Выполнение математических вычислений, сбор данных в требуемом формате (формат, который способна прочитать программа "ЛОГОС") и запись во временный файл _debug.txt

7. Вставка во входящий .cd файл данных из _debug.txt (для корректной работы .txt переводится в .cd, а по завершению блока кода выполняется обратное действие) и получение конечного файла -_output.cd, который в дальнейшем открывается программой "ЛОГОС"

## 🤖 Стек

- tkinter

- PyInstaller

- PyYAML

## 📸 Скрины

### 💻 MacOS

<img width="400" alt="image" src="https://github.com/user-attachments/assets/0e1e7916-4722-42ce-9365-76f8ef91d1e9" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/acc1e23c-d980-472f-9225-44377677b1ec" />


### ⊞ Windows

<img width="400" alt="image" src="https://github.com/user-attachments/assets/f800cd2a-9db1-449b-81db-c00685cd4beb" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/08cef0c0-c6be-49be-b2fe-addf97702e36" />

### Результат работы в "ЛОГОС"

<img width="800" alt="image" src="https://github.com/user-attachments/assets/9568182d-7b73-41f4-ba73-2ada6b2941a6" />

### Результат работы в "D3PLOT"

<img width="800" alt="image" src="https://github.com/user-attachments/assets/6d7dcf27-a2a0-4d1e-81bb-1fb183fe2453" />

<img width="800" alt="image" src="https://github.com/user-attachments/assets/711327d1-a616-42e7-8b30-df1aab5cb48e" />

<img width="800" alt="image" src="https://github.com/user-attachments/assets/9b1e6cd5-a333-4139-a7a4-20f243455bba" />


## ⚡ Инструкция по запуску

1. Клонируем проект (git clone https://github.com/Kurillccc/ParserKFile)

2. Переходим в корень проекта (cd ParserKFile)

3. Устанавливаем зависимости из requirements.txt 

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

4. Запускаем приложение с графическим интерфейсом (python run.py) или (python app/cli.py --input путь/к/файлу.k) для работы через консоль (там можно посмотреть что и как считается)

