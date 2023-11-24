# подключаем графическую библиотеку
from tkinter import *
import time
import random
# создаём новый объект — окно с игровым полем
tk = Tk()
# делаем заголовок окна
tk.title('Save Skuropat')
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800
# создаём новый холст — 1000 на 800 пикселей и весь неоходимый интерфейс
canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='aqua')

lava1 = canvas.create_rectangle(0, CANVAS_HEIGHT, 600, 785, fill='red')
lava2 = canvas.create_rectangle(700, CANVAS_HEIGHT, CANVAS_WIDTH, 785, fill='red')

wall_left = canvas.create_rectangle(0, 0, 15, CANVAS_HEIGHT, fill='blue')
wall_right = canvas.create_rectangle(985, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill='blue')
wall_ceiling = canvas.create_rectangle(0, 0, CANVAS_WIDTH, 15, fill='blue')

button_gates = canvas.create_rectangle(15, 300, 30, 340, fill="green")
button_speed_size_UP = canvas.create_rectangle(300, 15, 330, 30, fill="black")
button_speed_size_DOWN = canvas.create_rectangle(700, 15, 730, 30, fill='purple')
button_lose = canvas.create_rectangle(970, 400, 985, 420, fill='red')
button_square = canvas.create_rectangle(15, 70, 30, 100, fill='brown')

# говорим холсту, что у каждого видимого элемента будут свои отдельные координаты
canvas.pack()
# обновляем окно с холстом
tk.update()
# Описываем класс Ball, который будет отвечать за рыбку-шарик
class Ball:
    # конструктор — он вызывается в момент создания нового объекта на основе этого класса
    def __init__(self, canvas, paddle, color):
        # задаём параметры объекта, которые нам передают в скобках в момент создания
        self.canvas = canvas
        self.paddle = paddle
        # здесь появляется новое свойство id, в котором хранится внутреннее название шарика
        # создаём круг
        self.id = canvas.create_oval(10, 10, 50, 50, fill=color)
        # помещаем шарик в точку с random координатами ...
        self.starting_point_x = random.randint(150,750)
        self.starting_point_y = random.randint(50,200)
        self.canvas.move(self.id, self.starting_point_x, self.starting_point_y)
        # это будет вектор движения шарика
        self.x = random.randint(-10, 10)
        # в самом начале он всегда летит вверх
        self.y = random.randint(-6, -4)
        # шарик узнаёт свою высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # свойство, которое отвечает за то, достиг шарик дна или нет. Пока не достиг, значение будет False
        self.hit_bottom = False
        self.pause = False

    # обрабатываем касание платформы, для этого получаем 4 координаты шарика в переменной pos (левая верхняя и правая нижняя точки)
    def hit_paddle(self, pos):
        # получаем кординаты платформы через объект paddle (платформа)
        paddle_pos = self.canvas.coords(self.paddle.id)
        # если координаты касания совпадают с координатами платформы
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                # возвращаем метку о том, что мы успешно коснулись
                return True
        # возвращаем False — касания не было
        return False

    # метод, который отвечает за движение шарика
    def draw(self):
        # передвигаем шарик на заданный вектор x и y
        self.canvas.move(self.id, self.x, self.y)
        # запоминаем новые координаты шарика
        pos = self.canvas.coords(self.id)

        # если шарик правым нижним углом коснулся дна либо он попал в красную кнопку
        if (((pos[3] >= self.canvas_height) and ((pos[0] < 600) or (pos[2] > 700))) or ((pos[2] >= 970) and (pos[3] <= 450) and (pos[1] >= 370))):
            # помечаем это в отдельной переменной
            self.hit_bottom = True
            # выводим сообщение
            canvas.create_text(500, 400, text='Скуропат не выбрался :(', font=('Courier', 30), fill='black')

        # если шарик попал в ворота спасения внизу
        if ((pos[3] >= self.canvas_height) and ((pos[0] >= 600) and (pos[2] <= 700))):
            # помечаем это в отдельной переменной
            self.hit_bottom = True
            # выводим сообщение
            canvas.create_text(500, 400, text='Скуропат спасен!', font=('Courier', 30), fill='green')

        #cоздаем угловые спасительные ворота
        if ((pos[0] <= 30) and (pos[1] >= 270) and (pos[3] <= 360)):
            saving_gates = canvas.create_polygon(850, 15, 985, 15, 985, 150, fill="green")
            global flag_gates
            flag_gates = True

        #прописываем попадание в них
        if ((pos[0] >= 890) and (pos[3] <= 110) and flag_gates == True):
             self.hit_bottom = True
             canvas.create_text(500, 400, text='Скуропат спасен!', font=('Courier', 30), fill='green')

        # если шарик падает сверху
        if pos[1] <= 0:
            # задаём падение на следующем шаге = 5.5
            self.y = 5.5

        # если было касание платформы
        if self.hit_paddle(pos) == True:
            # отправляем шарик наверх
            self.y = -5.5

        # если коснулись левой стенки
        if pos[0] <= 0:
            # движемся вправо
            self.x = 5.5

        # если коснулись правой стенки
        if pos[2] >= self.canvas_width:
            # движемся влево
            self.x = -5.5

        #функционал кнопки ускорения
        if ((pos[1] <= 30) and (pos[0] >= 270) and (pos[2] <= 360)):
            self.x = self.x * 1.4
            self.y = self.y * 1.4

        #функционал кнопки замедления
        if ((pos[1] <= 30) and (pos[0] >= 670) and (pos[2] <= 760)):
            self.x = self.x * 0.9
            self.y = self.y * 0.9

       #кнопка создания отражающего квадрата
        if ((pos[0] <= 30) and (pos[1] >= 40) and (pos[3] <= 130)):
            reflect_square = canvas.create_rectangle(460, 170, 540, 250, fill="pink")
            global flag_square
            flag_square = True

        if (flag_square == True):
            #отражающий квадрат
            if ((pos[2] >= 450) and (pos[2] <= 460) and (pos[1] >= 130) and (pos[3] <= 290)):
                self.x = -5.5
            if ((pos[0] <= 550) and (pos[0] >= 540) and (pos[1] >= 130) and (pos[3] <= 290)):
                self.x = 5.5
            if ((pos[3] >= 160) and (pos[3] <= 170) and (pos[0] >= 420) and (pos[2] <= 580)):
                self.y = -5.5
            if ((pos[1] <= 260) and (pos[1] >= 250) and (pos[0] >= 420) and (pos[2] <= 580)):
                self.y = 5.5


#Описываем класс Paddle, который отвечает за платформы
class Paddle:
    # конструктор
    def __init__(self, canvas, color):
        # canvas означает, что платформа будет нарисована на нашем изначальном холсте
        self.canvas = canvas
        # создаём прямоугольную платформу 20 на 150 пикселей, закрашиваем выбранным цветом и получаем её внутреннее имя
        self.id = canvas.create_rectangle(0, 0, 150, 20, fill=color)
        # выбираем random положение платформы
        self.starting_point_x = random.randint(200, 800)
        # перемещаем платформу в стартовое положение
        self.canvas.move(self.id, self.starting_point_x, 600)
        # пока платформа никуда не движется, поэтому изменений по оси х нет
        self.x = 0
        self.y = 0
        # платформа узнаёт свою ширину и высоту
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        # задаём обработчик нажатий
        # если нажата стрелка вправо — выполняется метод turn_right()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)

      # пока платформа не двигается, поэтому ждём
        self.started = False
        # как только игрок нажмёт Return — всё стартует
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    # движемся вправо
    def turn_right(self, event):
        # будем смещаться правее на 5 пикселя по оси х
        self.x = 8

    def turn_left(self, event):
        self.x = -8

    def turn_up(self, event):
        self.y = -4

    def turn_down(self, event):
        self.y = 4


    # игра начинается
    def start_game(self, event):
        # меняем значение переменной, которая отвечает за старт движения платформы
        self.started = True

    # метод, который отвечает за движение платформы
    def draw(self):
        # сдвигаем нашу платформу на заданное количество пикселей
        self.canvas.move(self.id, self.x, self.y)
        # получаем координаты холста
        pos = self.canvas.coords(self.id)

        # если мы упёрлись в левую границу
        if pos[0] <= 15:
            # останавливаемся
            self.x = 0

        elif pos[2] >= self.canvas_width - 15:
            self.x = 0

        elif pos[1] <= 450:
            self.y = 0

        elif pos[3] >= 700:
            self.y = 0


# создаём объект — фиолетовую платформу
paddle = Paddle(canvas, 'purple')
# создаём объект — бежевую рыбку-шарик
ball = Ball(canvas, paddle, "gold")
#создаем начальный текст
start_text = canvas.create_text(500, 400, text='Нажмите Enter, чтобы начать', font=('Courier', 30), fill='green')
flag_gates = False  # создаем флаг, отвечающий за открытие угловых ворот
flag_square = False  # этот флаг отвечает за отражающий квадрат
# пока шарик не коснулся дна
while not ball.hit_bottom:
    # если игра началась и платформа может двигаться
    if paddle.started == True:
        canvas.delete(start_text)
        # двигаем шарик
        ball.draw()
        # двигаем платформу
        paddle.draw()
    # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
    tk.update_idletasks()
    # обновляем игровое поле и смотрим за тем, чтобы всё, что должно было быть сделано — было сделано
    tk.update()
    # замираем на одну сотую секунды, чтобы движение элементов выглядело плавно
    time.sleep(0.01)
time.sleep(3)
