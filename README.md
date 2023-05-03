# Бот-тренажёр городов России

## Бот работает на сервере и доступен к использованию в любое время
## Бот в telegram: [ссылка](https://t.me/ru_cities_trainerbot)

### Скриншоты работы:
![You lost!](https://github.com/sasamb4ik/project2_cities/blob/dev/images/utils.png)

![You lost!](https://github.com/sasamb4ik/project2_cities/blob/dev/images/work.png)
### Если вы хотите запустить локально:
  Важно понимать, что бот одновременно может быть запущен только на одной машине. Так как он постоянно запущен на сервере, чтобы вы могли локально проверить работу, вам необходимо:
  1) Зайти в telegram-канал BotFather [ссылка](https://t.me/BotFather)
  2) Написать команду /newbot, вы получите токен, копируете его
  3) Далее переходите в папку src: 
   ```
cd src
```
  4) Открываете файл settings.py, вставляете на место TOKEN тот токен, который вы получили от BotFather
  5) Теперь вы можете корректно запустить бота локально
### Функционал:
  1) Кнопка stop - завершить тренировку
  2) Кнопка help - прочитать правила
  3) Команда /start - начать новую игру

### Правила тренировки:
  1) Вы пишете город РФ, бот отвечает вам городом, который начинается с той буквы, на которую заканчивается ваш город. Далее вы должны ответить боту по этим же правилам.
  Пример: я ввожу: МосквА, бот отвечает АрмавиР, я должен ввести любой город на Р (Ржев, например)
