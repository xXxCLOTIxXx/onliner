import requests
import random, string
import pygame
import json
from threading import Thread

class Game:
    def __init__(self):
        self.game = True
        self.server='https://onlinersw.herokuapp.com'
        self.speed=20
        self.you=pygame.transform.scale(pygame.image.load('you.png'), (50, 50))
        self.player=pygame.transform.scale(pygame.image.load('player.png'), (50, 50))
        self.session = requests.Session()
        self.id=self.gen_id()
        self.x=random.randint(0, 800)
        self.y=random.randint(0, 800)
        self.size=(1000, 1000)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('ONLINER 1.0')
        pygame.init()
        self.post_position('up')

    def gen_id(self, num: int = 8):return "".join(random.choices(string.digits, k=num))

    def render(self):
        while self.game:
            try:
                response = self.session.get(f"{self.server}/player-position?id={self.id}")
                json_ = json.loads(response.text)
                self.screen.fill((255, 255, 255))
                for i in json_['players']:
                    position = json_['players'][i]
                    if  i == self.id:self.screen.blit(self.you, position)
                    else:self.screen.blit(self.player, position)
                    try:
                        message=json_['messages'][i]
                        text1 = pygame.font.Font(None, 20).render(message, 1, (0, 0, 0))
                        self.screen.blit(text1, (position[0]+60, position[1]))
                    except:pass
                    pygame.display.update()
            except:pass

    def post_position(self, type):
        if type == 'up':self.y-=self.speed
        elif type == 'down':self.y+=self.speed
        elif type == 'left':self.x-=self.speed
        elif type == 'right':self.x+=self.speed
        data = json.dumps({'uid': self.id, 'position':(self.x, self.y)})
        resp=self.session.post(f"{self.server}/post-position", json=data)


    def send_message(self, message):
        if message:
            data = json.dumps({'uid': self.id, 'message':message})
            resp=self.session.post(f"{self.server}/post-message", json=data)

    def main(self):
        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game=False
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:self.post_position('left')
            elif keys[pygame.K_RIGHT]:self.post_position('right')
            elif keys[pygame.K_UP]:self.post_position('up')
            elif keys[pygame.K_DOWN]:self.post_position('down')


if __name__ == '__main__':
    client=Game()
    Thread(target=client.main).start()
    Thread(target=client.render).start()
    while client.game:client.send_message(input("Message>>"))
