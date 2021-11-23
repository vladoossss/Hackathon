Инструкция для запуска(Windows + установленный python3.9):

0. Если у вас установлен python3 другой версии, то для работы с аудио необходимо скачать соответствующий файл с сайта https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio, который понадобится далее

1. Создание и активация виртуального окружения: 
    * cd путь к папке Hackathon
    * python -m venv venv
    * cd venv/Scripts
    * activate.bat

2. Установка зависимостей:
    * cd путь к папке Hackathon
    * В файле requirements.txt заменить путь к файлу(+ сам файл если другая версия python) PyAudio-0.2.11-cp39-cp39-win_amd64.whl на свой
    * pip install -r requirements.txt 

3. Запуск веб-сервиса:
    * python app.py
