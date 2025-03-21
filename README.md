# ITIS_8_OIP
Репозиторий курса "Основы информационного поиска". Задания выполнены студентами группы 11-101: Гаврилова Елена, Катаргина Ксения

## Задание 1 выполнено и загружено в папку Task 1.
Описание задания 1:

Это задание представляет собой веб-краулер, который:  
✔️ Скачивает 120 страниц с сайта ru.top-cat.org.  
✔️ Удаляет ссылки на JS и CSS, но сохраняет HTML.  
✔️ Сохраняет страницы в .txt в папке downloaded_pages/.  
✔️ Создаёт файл index.txt с номерами файлов и ссылками на статьи.

Как использовать:

Запустить "python task1.py".  
Найти загруженные страницы в downloaded_pages/.  
Посмотреть index.txt, чтобы увидеть, какие ссылки были скачаны.

## Задание 2 выполнено и загружено в папку Task 2.
Описание задания 2:

Это задание представляет собой скрипт, который:  
✔️ Извлекает слова (токены) из HTML-текстов.  
✔️ Убирает мусор (цифры, обрывки разметки).  
✔️ Фильтрует предлоги и союзы.  
✔️ Лемматизирует слова (приводит к начальной форме).  
✔️ Сохраняет результаты в tokens/.  

Как использовать:

Запустить "python task2.py".  
Открыть файлы в tokens/.

# Проект выполнен с использованием:

1. Python 3.8

2. PyCharm

3. Библиотеки requests, beautifulsoup4, pymorphy2

# Инструкция по развертыванию:

1.Склонировать репозиторий "git clone https://github.com/LenaGavrilova/ITIS_8_OIP.git".

2.Открыть проект в PyCharm.

3.Установить зависимости: "pip install requests beautifulsoup4 pymorphy2".

4.Перейти в папкy с нужным заданием.

4.Запустить скрипт через консоль командой "python {FILE}.py" , где {FILE} - название файла  или через кнопку Run

# Release Notes
Версия 1.0   
✅ Добавлена поддержка скачивания 120 страниц.  
✅ Реализовано удаление CSS и JS.  
✅ Файлы сохраняются в downloaded_pages/ в .txt формате.  
✅ Создан index.txt для списка скачанных страниц.  

Версия 2.0  
✅ Токенизация (удаление мусора, цифр, предлогов и союзов).  
✅ Лемматизация через pymorphy2.  
✅ Сохранение токенов и лемм в отдельные файлы.  

