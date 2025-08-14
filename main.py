import pygame as pg

pg.init()


class Text_panel:
    
    def __init__(self, text) -> None:
        self.font = pg.font.SysFont('Calibri', 30)
        self.color = (0, 0, 0)
        self.text = text
        self.ren_text = self.font.render(text, True, self.color)

        self.limit_length = 33
        self.good_symb = '0123456789-+/*().^'
    
    def update(self, text: str):
        self.text = text
        self.ren_text = self.font.render(text, True, self.color)
    
    def add(self, symb: str):
        if symb in self.good_symb and len(self.text) < self.limit_length:
            self.text = self.text + symb
            self.ren_text = self.font.render(self.text, True, self.color) 
    
    def b_space(self):
        if self.text:
            self.text = self.text[:-1]
            self.ren_text = self.font.render(self.text, True, self.color)
    
    def draw(self, surf: pg.Surface, end, height):
        pos = end - self.ren_text.get_width() - 5, height
        surf.blit(self.ren_text, pos)


class Output_panel:

    def __init__(self, width, height, text_panel: Text_panel) -> None:
        self.width = width
        self.height = height
        self.text_panel = text_panel

        self.s = pg.surface.Surface((self.width, self.height))
        self.s.fill((200, 200, 200))

        self.text_y = 31
        self.text_panel.draw(self.s, self.width, self.text_y)

    def draw(self, surf: pg.surface.Surface, dest):
        surf.blit(self.s, dest)
    
    def update(self):
        self.s.fill((200, 200, 200))
        self.text_panel.draw(self.s, self.width, self.text_y)


class Button_panel:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.s = pg.surface.Surface((self.width, self.height))
        self.s.fill((100, 100, 100))
    
    def draw(self, surf: pg.surface.Surface, dest):
        surf.blit(self.s, dest)


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
                    else:
                        self.panel.text_panel.add(event.unicode)
            
            self.update()
            screen.blit(self.s, (0, 0))
            
            pg.display.flip()
    
    def update(self):
        self.panel.update()
        self.panel.draw(self.s, (0, 0))

        self.button_panel.draw(self.s, (0, self.panel.height))


def main():
    text_panel = Text_panel('')
    panel = Output_panel(400, 100, text_panel)
    button_panel = Button_panel(400, 400)
    window = Main_window(panel, button_panel, 400, 500)
    window.mainloop()


if __name__ == "__main__":
    main()