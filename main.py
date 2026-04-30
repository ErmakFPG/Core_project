from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
import os

class WorkoutProgressBar(BoxLayout):
    """Кастомный виджет горизонтальной шкалы прогресса"""
    def __init__(self, total_segments=15, **kwargs):
        super().__init__(**kwargs)
        self.total_segments = total_segments
        self.completed_segments = 0
        self.size_hint = (0.9, None)
        self.height = 30
        self.pos_hint = {'center_x': 0.5}
        self.spacing = 4
        self.padding = [0, 0, 0, 0]
        
        # Создаём сегменты
        self.segments = []
        for i in range(total_segments):
            segment = BoxLayout(
                size_hint=(1/total_segments, 1)
            )
            # Устанавливаем серый цвет фона для сегмента
            with segment.canvas.before:
                Color(0.85, 0.85, 0.85, 1)
                segment.rect = Rectangle(size=segment.size, pos=segment.pos)
            
            segment.bind(pos=self._update_rect, size=self._update_rect)
            self.segments.append(segment)
            self.add_widget(segment)
        
        # Обновляем цвета
        self.update_colors()
    
    def _update_rect(self, instance, *args):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def set_progress(self, completed_percent):
        """Устанавливает прогресс от 0 до 100"""
        self.completed_segments = int((completed_percent / 100.0) * self.total_segments)
        self.update_colors()
    
    def increment(self):
        """Увеличивает прогресс на 1 сегмент"""
        if self.completed_segments < self.total_segments:
            self.completed_segments += 1
            self.update_colors()
        return self.completed_segments == self.total_segments
    
    def reset(self):
        """Сбрасывает прогресс"""
        self.completed_segments = 0
        self.update_colors()
    
    def update_colors(self):
        """Обновляет цвета сегментов"""
        for i, segment in enumerate(self.segments):
            if i < self.completed_segments:
                # Заполнен - синий
                segment.canvas.before.clear()
                with segment.canvas.before:
                    Color(0.25, 0.55, 0.85, 1)
                    segment.rect = Rectangle(size=segment.size, pos=segment.pos)
            else:
                # Пустой - светло-серый
                segment.canvas.before.clear()
                with segment.canvas.before:
                    Color(0.85, 0.85, 0.85, 1)
                    segment.rect = Rectangle(size=segment.size, pos=segment.pos)

class WorkoutApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.94, 0.92, 1)
        
        # Загружаем звуки
        self.load_sounds()
        
        # Список упражнений
        self.exercise_names = [
            "Вакуум живота",
            "Классическое скручивание",
            "Обратное скручивание",
            "Боковая планка",
            "Планка на прямых руках"
        ]
        
        # Упражнения с автоматическим таймером
        self.timer_exercises = [3, 4]
        self.exercise_timer_duration = 30
        
        # Параметры тренировки
        self.total_circuits = 3
        self.exercises_per_circuit = len(self.exercise_names)
        self.rest_time = 15
        
        # Общее количество упражнений во всей тренировке
        self.total_exercises = self.total_circuits * self.exercises_per_circuit
        self.current_exercise_number = 0
        
        # Основной контейнер
        self.layout = BoxLayout(orientation='vertical')
        
        self.start_screen()
        
        return self.layout
    
    def load_sounds(self):
        """Загружает звуковые файлы"""
        # Путь к папке со звуками (текущая директория)
        sound_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.tick_normal_path = os.path.join(sound_dir, 'tick_normal.wav')
        self.tick_urgent_path = os.path.join(sound_dir, 'tick_urgent.wav')
        
        # Загружаем звуки (проверяем существование файлов)
        if os.path.exists(self.tick_normal_path):
            self.tick_normal = SoundLoader.load(self.tick_normal_path)
        else:
            self.tick_normal = None
            print(f"Предупреждение: файл {self.tick_normal_path} не найден")
        
        if os.path.exists(self.tick_urgent_path):
            self.tick_urgent = SoundLoader.load(self.tick_urgent_path)
        else:
            self.tick_urgent = None
            print(f"Предупреждение: файл {self.tick_urgent_path} не найден")
    
    def play_tick(self, seconds_left):
        """Воспроизводит тик в зависимости от оставшегося времени"""
        if seconds_left >= 4:
            # Обычный тик (4-15+ секунд)
            if self.tick_normal:
                self.tick_normal.play()
        else:
            # Срочный тик (1-3 секунды)
            if self.tick_urgent:
                self.tick_urgent.play()
    
    def start_screen(self):
        self.layout.clear_widgets()
        
        center_layout = FloatLayout()
        
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
        
        self.start_btn.bind(on_press=self.start_workout)
        center_layout.add_widget(self.start_btn)
        self.layout.add_widget(center_layout)
    
    def start_workout(self, instance):
        self.current_circuit = 1
        self.current_exercise_index = 0
        self.current_exercise_number = 1
        self.waiting_for_next = False
        
        self.show_exercise_screen()
    
    def show_exercise_screen(self):
        self.layout.clear_widgets()
        
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=[30, 20, 30, 30])
        
        # Верхняя часть: прогресс-бар
        top_padding = BoxLayout(size_hint=(1, 0.15), padding=[0, 20, 0, 0])
        
        # Создаём прогресс-бар
        self.progress_bar = WorkoutProgressBar(total_segments=15)
        # Вычисляем текущий прогресс в процентах
        progress_percent = (self.current_exercise_number - 1) / self.total_exercises * 100
        self.progress_bar.set_progress(progress_percent)
        
        top_padding.add_widget(self.progress_bar)
        main_layout.add_widget(top_padding)
        
        # Название упражнения
        current_exercise = self.exercise_names[self.current_exercise_index]
        self.exercise_name = Label(
            text=current_exercise,
            font_size=48,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, 0.5)
        )
        main_layout.add_widget(self.exercise_name)
        
        # Проверяем, нужно ли показывать таймер
        if self.current_exercise_index in self.timer_exercises:
            # Упражнение с автоматическим таймером
            self.timer_label = Label(
                text=str(self.exercise_timer_duration),
                font_size=120,
                color=(0.25, 0.55, 0.85, 1),
                size_hint=(1, 0.35)
            )
            main_layout.add_widget(self.timer_label)
            
            self.timer_time_left = self.exercise_timer_duration
            self.timer_event = Clock.schedule_interval(self.update_exercise_timer, 1)
        else:
            # Обычное упражнение - кнопка "Выполнил"
            self.complete_btn = Button(
                text="ВЫПОЛНИЛ",
                font_size=55,
                size_hint=(0.8, 0.25),
                pos_hint={'center_x': 0.5},
                background_normal='',
                background_color=(0.4, 0.7, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            self.complete_btn.bind(on_press=self.complete_exercise)
            main_layout.add_widget(self.complete_btn)
        
        self.layout.add_widget(main_layout)
    
    def update_exercise_timer(self, dt):
        if self.timer_time_left > 0:
            self.timer_time_left -= 1
            self.timer_label.text = str(self.timer_time_left)
            
            # Воспроизводим тик (для планок)
            self.play_tick(self.timer_time_left)
            
            if self.timer_time_left <= 5:
                self.timer_label.color = (0.9, 0.55, 0.1, 1)
        else:
            self.timer_event.cancel()
            self.complete_exercise(None)
    
    def complete_exercise(self, instance):
        # Увеличиваем прогресс-бар
        is_complete = self.progress_bar.increment()
        
        # Проверяем, не завершена ли тренировка
        if self.current_circuit == self.total_circuits and self.current_exercise_index == self.exercises_per_circuit - 1:
            self.show_congratulations()
            return
        
        # Обновляем номер упражнения
        self.current_exercise_number += 1
        
        # Переходим к экрану отдыха
        self.show_rest_screen()
    
    def show_rest_screen(self):
        self.layout.clear_widgets()
        
        next_circuit = self.current_circuit
        next_exercise_index = self.current_exercise_index + 1
        
        if next_exercise_index >= self.exercises_per_circuit:
            next_exercise_index = 0
            next_circuit += 1
        
        next_exercise_name = self.exercise_names[next_exercise_index]
        
        rest_layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Заголовок
        rest_title = Label(
            text="ОТДЫХ",
            font_size=65,
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(1, 0.3)
        )
        
        # Таймер
        self.rest_timer_label = Label(
            text=str(self.rest_time),
            font_size=160,
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
        
        # Кнопка пропуска
        skip_btn = Button(
            text="Пропустить",
            font_size=35,
            size_hint=(1, 0.1),
            background_normal='',
            background_color=(0.8, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        skip_btn.bind(on_press=self.skip_rest)
        
        rest_layout.add_widget(rest_title)
        rest_layout.add_widget(self.rest_timer_label)
        rest_layout.add_widget(next_exercise_label)
        rest_layout.add_widget(skip_btn)
        
        self.layout.add_widget(rest_layout)
        
        self.rest_time_left = self.rest_time
        self.rest_timer_event = Clock.schedule_interval(self.update_rest_timer, 1)
    
    def update_rest_timer(self, dt):
        if self.rest_time_left > 0:
            self.rest_time_left -= 1
            self.rest_timer_label.text = str(self.rest_time_left)
            
            # Воспроизводим тик для отдыха
            self.play_tick(self.rest_time_left)
            
            if self.rest_time_left <= 5:
                self.rest_timer_label.color = (0.9, 0.55, 0.1, 1)
        else:
            self.rest_timer_event.cancel()
            self.move_to_next_exercise()
    
    def skip_rest(self, instance):
        if hasattr(self, 'rest_timer_event'):
            self.rest_timer_event.cancel()
        self.move_to_next_exercise()
    
    def move_to_next_exercise(self):
        if self.current_exercise_index < self.exercises_per_circuit - 1:
            self.current_exercise_index += 1
        else:
            self.current_circuit += 1
            self.current_exercise_index = 0
        
        self.show_exercise_screen()
    
    def show_congratulations(self):
        self.layout.clear_widgets()
        
        congrats_layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Полный прогресс-бар в конце
        self.progress_bar = WorkoutProgressBar(total_segments=15)
        self.progress_bar.set_progress(100)
        
        congrats_title = Label(
            text="ПОЗДРАВЛЯЕМ!",
            font_size=60,
            color=(0.2, 0.6, 0.2, 1),
            size_hint=(1, 0.3)
        )
        
        congrats_message = Label(
            text="Тренировка завершена!\nОтличная работа!",
            font_size=40,
            color=(0.3, 0.3, 0.3, 1),
            size_hint=(1, 0.4)
        )
        
        finish_btn = Button(
            text="Закончить",
            font_size=45,
            size_hint=(0.7, 0.15),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0.25, 0.55, 0.85, 1),
            color=(1, 1, 1, 1)
        )
        finish_btn.bind(on_press=self.back_to_start)
        
        congrats_layout.add_widget(self.progress_bar)
        congrats_layout.add_widget(congrats_title)
        congrats_layout.add_widget(congrats_message)
        congrats_layout.add_widget(finish_btn)
        
        self.layout.add_widget(congrats_layout)
    
    def back_to_start(self, instance):
        self.start_screen()

if __name__ == "__main__":
    WorkoutApp().run()
