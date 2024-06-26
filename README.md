**ANDAN_FES_PROJECT**
Анализ стоимости квартир в г.Москва на основе объявлений о продаже.
Парсинг данных с сайта, дальнейшая их обработка и визуализация, выдвижение и проверка следующих гипотез:

1. Дисконт в стоимости квартиры на последнем этаже
2. Дисконт стоимости квартиры на первом этаже
3. Различия стоимости квадратного метра в апартаментах и в квартире
4. Увеличенная этажность в новых домах

Данные взяты с сайта ЦИАН. ЦИАН -  крупнейший сервис по поиску недвижимости, существующий с 2001 года.  Сайт позволяет пользователям размещать и отслеживать объявления о продаже, аренде квартир и другие услуги, связанные с недвижимостью. 
Для парсинга были взяты все 14 районов. На каждый район ЦИАН выдавал 55 страниц объявлений, содержащих по 28 предложений квартир. Общее количество объявлений - 21560, из которых в датасет попало 7700. Это связано с некими мерами ЦИАНа, предотвращающими увеличенную нагрузку на сервера сайта. 

*КОМАНДА:
Абарин Макар
Каримов Атахан
Нуруллин Ринат*

Структура репозитория:
* README - ты тут!
* parser.py - файл с парсером
* cian_offers.csv - датасет, полученный после парсинга 
* data_processing.ipynb - работа с датасетом и машинное обучение модели

Описание переменных в датасете:

Link - ссылка на объявление о продаже
Price - цена продажи
Price per m2 - цена за квадратный метр
Square - площадь квартиры в квадратных метрах
Floor - этаж квартиры
Floors - всего этажей в доме
Rooms - комнат в квартире
Is Apartment? - является ли квартира апартаментами
Year - год постройки дома
Time to metro - время до метро (в минутах)
Okrug - округ
District - район
