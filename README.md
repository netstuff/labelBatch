### Установка
1. `pipenv install`
1. `cd labelImg`
1. `make qt5py3`
1. `cd ..`

### Генерация кадров из видеопотока
1. подготовьте локальный файл `<file>` или ссылку на RTSP-поток `<rtsp>`
1. `pipenv run python grabber.py --input=<file|rtsp>`

### Генерация файлов разметки
1. `pipenv run python labelImg/labelImg.py`
1. загрузите изображение
1. выделите объекты рамками и определите тип каждого из них
1. сохраните файлы разметки в VOC-формате в папку `<dirname>`

### Конвертация в формат RTMIP
`pipenv run python converter.py --input=<dirname>`
