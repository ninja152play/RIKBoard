RICBoard - записывание действий
==================================================

RICBoard - это программа для записи твоих действий.

В программе представлены 3 варианта записи и 2 воспроизведение:

1. Keyboard - записывает действия только клавиатуры
2. Keyboard and mouse - записывает действия клавиатуры и мыши
3. AHK - записывает действия в качестве ahk скрипта

Player воспроизводит 1-ю и 2-ю вариант записи (в одиночном режиме и цикличном)

Установка
=========

1. ```git clone https://github.com/ninja152play/RIKBoard.git```
2. ```cd RICBoard```
3. ```python -m venv venv```
4. Для Linux ```source venv/bin/activate``` Для Windows ```venv\Scripts\activate.bat```
5. ```pip install -r requirements.txt```

Запуск
======

1. Для Linux ```source venv/bin/activate``` Для Windows ```venv\Scripts\activate.bat```
2. ```python main.py```

Документация
============
Вариант записи AHK нужен для игр в которых мышка центрирована (Elden Ring, Cyberpunk 2077 и т.д.)

При записи в режиме AHK после поворота мыши сдвиньте в обратную сторону на пиксель!!!
