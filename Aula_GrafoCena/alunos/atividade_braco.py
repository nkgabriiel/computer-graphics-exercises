# ATIVIDADE: braço robótico com grafo de cena.
# Leia ATIVIDADE.md e complete os trechos marcados com TODO.
# ESC fecha. P salva capturas/resultado.png para a entrega.
import argparse

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.object3D import Object3D
from formas import caixa

CINZA = [0.6, 0.62, 0.66]
LARANJA = [0.98, 0.45, 0.2]
AZUL = [0.25, 0.5, 0.95]
VELOCIDADE = 1.5  # radianos por segundo


class Braco(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=960 / 640)
        self.camera.setPosition([0, 1.9, 4.2])
        self.camera.rotateX(-0.2)

        chao = caixa(6, 0.1, 6, [0.8, 0.82, 0.85])
        chao.setPosition([0, -0.05, 0])
        self.scene.add(chao)

        # base: caixa de altura 0.4, apoiada no chão
        self.base = caixa(1.0, 0.4, 1.0, CINZA)
        self.base.setPosition([0, 0.2, 0])
        self.scene.add(self.base)

        # TODO 1: ombro (pivô) no topo da base + braço laranja
        self.ombro = Object3D()
        self.ombro.setPosition([0, 0.2, 0])      # topo da base (metade de 0.4)
        self.base.add(self.ombro)

        self.braco = caixa(0.3, 1.2, 0.3, LARANJA)
        self.braco.setPosition([0, 0.6, 0])      # sobe metade de 1.2: ponta de baixo no ombro
        self.ombro.add(self.braco)

        # TODO 2: cotovelo (pivô) na ponta de cima do braço + antebraço azul
        self.cotovelo = Object3D()
        self.cotovelo.setPosition([0, 1.2, 0])   # altura TOTAL do braço, no referencial do ombro
        self.ombro.add(self.cotovelo)

        self.antebraco = caixa(0.25, 1.0, 0.25, AZUL)
        self.antebraco.setPosition([0, 0.5, 0])  # sobe metade de 1.0
        self.cotovelo.add(self.antebraco)

        # TODO 3: garra cinza na ponta do antebraço
        self.garra = caixa(0.5, 0.15, 0.5, CINZA)
        self.garra.setPosition([0, 0.5 + 0.075, 0])  # topo do antebraço + metade da garra
        self.antebraco.add(self.garra)

    def update(self):
        angulo = VELOCIDADE * self.deltaTime
        # TODO 4: A e D giram a base em torno do eixo Y
        if self.isKeyPressed('a'):
            self.base.rotateY(angulo)
        if self.isKeyPressed('d'):
            self.base.rotateY(-angulo)
        # TODO 5: W/S giram o ombro e I/K giram o cotovelo, em torno do eixo Z
        if self.isKeyPressed('w'):
            self.ombro.rotateZ(angulo)
        if self.isKeyPressed('s'):
            self.ombro.rotateZ(-angulo)
        if self.isKeyPressed('i'):
            self.cotovelo.rotateZ(angulo)
        if self.isKeyPressed('k'):
            self.cotovelo.rotateZ(-angulo)
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frames', type=int)
    parser.add_argument('--screenshot')
    args = parser.parse_args()
    Braco(title='Atividade: braço robótico').run(args.frames, args.screenshot)