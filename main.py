import pygame as pg

pg.init()


class Text_panel:
    
    def __init__(self, text) -> None:
        self.font = pg.font.SysFont('Calibri', 30)
        self.color = (0, 0, 0)
        self.text = text
        self.ren_text = self.font.render(text, True, self.color)
        self.text_height = self.ren_text.get_height()
        self.stock_width = self.font.render('1', True, self.color).get_width()

        self.limit_length = 19
        self.good_symb = '0123456789-+/*().^%'
    
    def update_to_new(self, text: str):
        self.text = text
        self.ren_text = self.font.render(text, True, self.color)
    
    def add(self, symb: str):
        if self.text == 'Error: Division by zero':
            self.text = ''
        if symb in self.good_symb and len(self.text) < self.limit_length:
            self.text = self.text + symb
        self.ren_text = self.font.render(self.text, True, self.color) 
    
    def b_space(self):
        if self.text:
            if self.text[0] not in self.good_symb:
                self.text = ''
            else:
                self.text = self.text[:-1]
            self.ren_text = self.font.render(self.text, True, self.color)
    
    def draw(self, surf: pg.Surface, end, height):
        pos = end - self.ren_text.get_width() - 5, height
        surf.blit(self.ren_text, pos)

        if not self.text:
            pg.draw.rect(surf, (50, 50, 50), (end - self.stock_width - 5, height, self.stock_width, self.text_height))
    
    def eval_and_replace(self):
        if not self.text or self.text[0] not in self.good_symb:
            return
        
        self.text = self.text.replace('^', '**')
        try:
            self.text = str(eval(self.text))
        except Exception as e:
            self.text = e.__class__.__name__
        
        self.ren_text = self.font.render(self.text, True, self.color) 


class Output_panel:

    def __init__(self, width, height, text_panel: Text_panel) -> None:
        self.width = width
        self.height = height
        self.text_panel = text_panel

        self.s = pg.surface.Surface((self.width, self.height))
        self.s.fill((200, 200, 200))

        self.text_y = (self.height - self.text_panel.text_height) // 2
        self.text_panel.draw(self.s, self.width, self.text_y)

    def draw(self, surf: pg.surface.Surface, dest):
        surf.blit(self.s, dest)
    
    def update(self):
        self.s.fill((200, 200, 200))
        self.text_panel.draw(self.s, self.width, self.text_y)


class Button:

    def __init__(self, width, height, color, text, func=lambda x: print(x)) -> None:
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.func = func
        self.box = None

        self.s = pg.surface.Surface((self.width, self.height))
        self.s.fill(self.color)
    
    def draw(self, surf: pg.Surface, dest, pos):
        if self.box is None:
            self.box = pg.rect.Rect(dest[0] + pos[0], dest[1] + pos[1], self.width, self.height)
        surf.blit(self.s, dest)
    
    def check_pressed(self, mouse_pos):
        if self.box is None:
            print('Error: Button hasnt been drawn')
            return
        return self.box.collidepoint((mouse_pos[0], mouse_pos[1]))

    def activate(self):
        self.func(self.text)


class Button_panel:

    def __init__(self, width, height, pos) -> None:
        self.width = width
        self.height = height
        self.pos = pos

        self.s = pg.surface.Surface((self.width, self.height))
        self.s.fill((100, 100, 100))

        self.b1 = Button(50, 50, (0, 0, 0), '1')
        self.b1.draw(self.s, (10, 10), self.pos)
    
    def draw(self, surf: pg.surface.Surface, dest):
        surf.blit(self.s, dest)
    
    def handle_press(self, mouse_pos):
        if self.b1.check_pressed(mouse_pos):
            self.b1.activate()

class Main_window:

    def __init__(self, panel: Output_panel, button_panel: Button_panel, width, height) -> None:
        self.panel = panel
        self.button_panel = button_panel
        self.width = width
        self.height = height

        self.s = pg.surface.Surface((self.width, self.height))
        self.s.blit(panel.s, (0, 0))
        self.s.blit(button_panel.s, (0, self.panel.height))
    
    def mainloop(self):
        screen = pg.display.set_mode((self.width, self.height))
        screen.blit(self.s, (0, 0))
        pg.display.set_caption('Calculator')
        icon = pg.image.load('res/icon.png')
        pg.display.set_icon(icon)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.panel.text_panel.b_space()
                    elif event.key == pg.K_RETURN:
                        self.panel.text_panel.eval_and_replace()
                    else:
                        self.panel.text_panel.add(event.unicode)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.button_panel.handle_press(pg.mouse.get_pos())
            
            self.update()
            screen.blit(self.s, (0, 0))
            
            pg.display.flip()
    
    def update(self):
        self.panel.update()
        self.panel.draw(self.s, (0, 0))

        self.button_panel.draw(self.s, (0, self.panel.height))


def main():
    text_panel = Text_panel('')
    panel = Output_panel(300, 100, text_panel)
    button_panel = Button_panel(300, 300, (0, 100))
    window = Main_window(panel, button_panel, 300, 400)
    window.mainloop()


if __name__ == "__main__":
    main()