from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

class WorkoutApp(App):
    def build(self):
        # Устанавливаем цвет фона окна (светлый)
        Window.clearcolor = (0.95, 0.94, 0.92, 1)
        
        # Список упражнений
        self.exercise_names = [
            "Вакуум живота",
            "Классическое скручивание",
            "Обратное скручивание",
            "Боковая планка",
            "Планка на прямых руках"
        ]
        
        # Упражнения с автоматическим таймером (по индексам)
        self.timer_exercises = [3, 4]  # "Боковая планка" (индекс 3) и "Планка на прямых руках" (индекс 4)
        self.exercise_timer_duration = 30  # 30 секунд для планок
        
        # Параметры тренировки
        self.total_circuits = 3
        self.exercises_per_circuit = len(self.exercise_names)
        self.rest_time = 15  # время отдыха в секундах
        
        # Основной контейнер
        self.layout = BoxLayout(orientation='vertical')
        
        # Стартовый экран: только кнопка по центру
        self.start_screen()
        
        return self.layout
    
    def start_screen(self):
        # Очищаем всё, что было в layout
        self.layout.clear_widgets()
        
        # Создаём FloatLayout для абсолютного позиционирования
        center_layout = FloatLayout()
        
        # Квадратная кнопка по центру
        self.start_btn = Button(
            text="Старт",
            font_size=60,
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='',
            background_color=(0.25, 0.55, 0.85, 1),
            color=(1, 1, 1, 1)
        )
        
        # Привязываем событие нажатия
        self.start_btn.bind(on_press=self.start_workout)
        
        # Добавляем кнопку
        center_layout.add_widget(self.start_btn)
        self.layout.add_widget(center_layout)
    
    def start_workout(self, instance):
        # Инициализируем параметры тренировки
        self.current_circuit = 1
        self.current_exercise_index = 0
        self.waiting_for_next = False
        
        # Переходим к первому упражнению
        self.show_exercise_screen()
    
    def show_exercise_screen(self):
        # Очищаем экран
        self.layout.clear_widgets()
        
        # Создаём основной вертикальный контейнер с отступами
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=30)
        
        # Информация о круге
        self.circuit_info = Label(
            text=f"Круг {self.current_circuit} из {self.total_circuits}",
            font_size=35,
            color=(0.3, 0.3, 0.3, 1),
            size_hint=(1, 0.12)
        )
        
        # Название упражнения
        current_exercise = self.exercise_names[self.current_exercise_index]
        self.exercise_name = Label(
            text=current_exercise,
            font_size=45,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, 0.4)
        )
        
        # Прогресс в круге
        self.progress_info = Label(
            text=f"Упражнение {self.current_exercise_index + 1} из {self.exercises_per_circuit}",
            font_size=30,
            color=(0.4, 0.4, 0.4, 1),
            size_hint=(1, 0.1)
        )
        
        # Сначала добавляем все информационные виджеты
        main_layout.add_widget(self.circuit_info)
        main_layout.add_widget(self.exercise_name)
        main_layout.add_widget(self.progress_info)
        
        # Проверяем, нужно ли показывать таймер для этого упражнения
        if self.current_exercise_index in self.timer_exercises:
            # Упражнение с автоматическим таймером
            self.timer_label = Label(
                text=str(self.exercise_timer_duration),
                font_size=100,
                color=(0.25, 0.55, 0.85, 1),
                size_hint=(1, 0.25)
            )
            main_layout.add_widget(self.timer_label)
            
            # Запускаем таймер
            self.timer_time_left = self.exercise_timer_duration
            self.timer_event = Clock.schedule_interval(self.update_exercise_timer, 1)
            
            # Нет кнопки "Далее" для планок
        else:
            # Обычное упражнение - добавляем кнопку "Далее" в самый низ
            self.next_btn = Button(
                text="Далее",
                font_size=50,
                size_hint=(1, 0.15),
                background_normal='',
                background_color=(0.4, 0.7, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            self.next_btn.bind(on_press=self.complete_exercise)
            main_layout.add_widget(self.next_btn)
        
        # Добавляем main_layout в основной layout
        self.layout.add_widget(main_layout)
    
    def update_exercise_timer(self, dt):
        if self.timer_time_left > 0:
            self.timer_time_left -= 1
            self.timer_label.text = str(self.timer_time_left)
            
            # Меняем цвет таймера когда остаётся мало времени
            if self.timer_time_left <= 5:
                self.timer_label.color = (0.9, 0.55, 0.1, 1)  # Оранжевый
        else:
            # Таймер закончился - останавливаем и переходим к отдыху или следующему упражнению
            self.timer_event.cancel()
            self.complete_exercise(None)
    
    def complete_exercise(self, instance):
        # Проверяем, не завершена ли тренировка
        if self.current_circuit == self.total_circuits and self.current_exercise_index == self.exercises_per_circuit - 1:
            # Последнее упражнение завершено
            self.show_congratulations()
            return
        
        # Переходим к экрану отдыха
        self.show_rest_screen()
    
    def show_rest_screen(self):
        # Очищаем экран
        self.layout.clear_widgets()
        
        # Определяем следующее упражнение
        next_circuit = self.current_circuit
        next_exercise_index = self.current_exercise_index + 1
        
        if next_exercise_index >= self.exercises_per_circuit:
            next_exercise_index = 0
            next_circuit += 1
        
        next_exercise_name = self.exercise_names[next_exercise_index]
        
        # Создаём контейнер для экрана отдыха
        rest_layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Заголовок "Отдых"
        rest_title = Label(
            text="Отдых",
            font_size=60,
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(1, 0.3)
        )
        
        # Таймер отдыха
        self.rest_timer_label = Label(
            text=str(self.rest_time),
            font_size=150,
            color=(0.25, 0.55, 0.85, 1),
            size_hint=(1, 0.4)
        )
        
        # Следующее упражнение
        next_exercise_label = Label(
            text=f"Следующее: {next_exercise_name}",
            font_size=35,
            color=(0.4, 0.4, 0.4, 1),
            size_hint=(1, 0.2)
        )
        
        # Кнопка пропуска отдыха
        skip_btn = Button(
            text="Пропустить",
            font_size=30,
            size_hint=(1, 0.1),
            background_normal='',
            background_color=(0.8, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        skip_btn.bind(on_press=self.skip_rest)
        
        # Собираем всё
        rest_layout.add_widget(rest_title)
        rest_layout.add_widget(self.rest_timer_label)
        rest_layout.add_widget(next_exercise_label)
        rest_layout.add_widget(skip_btn)
        
        self.layout.add_widget(rest_layout)
        
        # Запускаем таймер отдыха
        self.rest_time_left = self.rest_time
        self.rest_timer_event = Clock.schedule_interval(self.update_rest_timer, 1)
    
    def update_rest_timer(self, dt):
        if self.rest_time_left > 0:
            self.rest_time_left -= 1
            self.rest_timer_label.text = str(self.rest_time_left)
            
            # Меняем цвет таймера когда остаётся мало времени
            if self.rest_time_left <= 5:
                self.rest_timer_label.color = (0.9, 0.55, 0.1, 1)  # Оранжевый
        else:
            # Время отдыха закончилось
            self.rest_timer_event.cancel()
            self.move_to_next_exercise()
    
    def skip_rest(self, instance):
        # Пропускаем отдых
        if hasattr(self, 'rest_timer_event'):
            self.rest_timer_event.cancel()
        self.move_to_next_exercise()
    
    def move_to_next_exercise(self):
        # Переходим к следующему упражнению
        if self.current_exercise_index < self.exercises_per_circuit - 1:
            self.current_exercise_index += 1
        else:
            self.current_circuit += 1
            self.current_exercise_index = 0
        
        # Показываем экран упражнения
        self.show_exercise_screen()
    
    def show_congratulations(self):
        # Очищаем экран
        self.layout.clear_widgets()
        
        # Создаём контейнер для поздравления
        congrats_layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Поздравление
        congrats_title = Label(
            text="ПОЗДРАВЛЯЕМ!",
            font_size=60,
            color=(0.2, 0.6, 0.2, 1),
            size_hint=(1, 0.3)
        )
        
        # Сообщение
        congrats_message = Label(
            text="Тренировка завершена!\nОтличная работа!",
            font_size=40,
            color=(0.3, 0.3, 0.3, 1),
            size_hint=(1, 0.5)
        )
        
        # Кнопка возврата на старт
        finish_btn = Button(
            text="Закончить",
            font_size=40,
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0.25, 0.55, 0.85, 1),
            color=(1, 1, 1, 1)
        )
        finish_btn.bind(on_press=self.back_to_start)
        
        congrats_layout.add_widget(congrats_title)
        congrats_layout.add_widget(congrats_message)
        congrats_layout.add_widget(finish_btn)
        
        self.layout.add_widget(congrats_layout)
    
    def back_to_start(self, instance):
        # Возвращаемся на стартовый экран
        self.start_screen()

if __name__ == "__main__":
    WorkoutApp().run()
