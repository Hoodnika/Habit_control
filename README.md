<h1>Habit_control</h1>


<h2>Как начать?</h2>
• $ git clone https://github.com/Hoodnika/Habit_control<br>
• $ pip install -r requirements.txt <br>
• Создайте и заполните файл .env по подобию .env.sample <br>
• $ python3 manage.py makemigrations <br>
• $ python3 manage.py migrate <br>
• $ celery -A config worker --beat --scheduler django --loglevel=info <br>

Теперь проект готов работать, зарегистрируйтесь в приложении <br>
Если хотите создать admin в вашем приложении используйте команду : <br>
• $ python3 manage.py createsuper <br>


