# Arquivo inicial da atividade. Leia ATIVIDADE.md e altere os trechos marcados com TODO.
from pathlib import Path
import argparse
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from material.textureMaterial import TextureMaterial

from geometry.boxGeometry import BoxGeometry
IMAGENS=Path(__file__).resolve().parent/'images'
TEXTURA='mosaico.png'  # TODO 1: troque para mosaico.png
VELOCIDADE=0.8  # radianos por segundo
class Cubo(Base):
    def initialize(self):
        self.renderer=Renderer();self.scene=Scene()
        self.camera=Camera(aspectRatio=960/640)
        self.camera.setPosition([0,0,3.2])
        self.velocidade=VELOCIDADE
        # cubo principal
        textura=Texture(IMAGENS/TEXTURA)
        self.mesh=Mesh(BoxGeometry(),TextureMaterial(textura))
        self.mesh.rotateX(0.35);self.mesh.rotateY(0.5)
        self.scene.add(self.mesh)
        # TODO 2: satélite com grade_uv.png repetida 2x2
        texturaSatelite=Texture(IMAGENS/'grade_uv.png')
        self.satelite=Mesh(BoxGeometry(),TextureMaterial(texturaSatelite,{'repeatUV':[2,2]}))
        # TODO 3: filho do cubo principal, a 1.3 do centro, escala 0.4
        self.satelite.setPosition([1.3,0,0])  # primeiro posiciona
        self.satelite.scale(0.4)              # depois escala
        self.mesh.add(self.satelite)
    def update(self):
        # TODO 4: setas 'up' e 'down' alteram a velocidade do cubo principal
        if self.isKeyPressed('up'):
            self.velocidade+=1.0*self.deltaTime
        if self.isKeyPressed('down'):
            self.velocidade-=1.0*self.deltaTime
        self.mesh.rotateY(self.velocidade*self.deltaTime)
        # TODO 5: o satélite gira em torno do próprio eixo X, a 2 rad/s
        self.satelite.rotateX(2.0*self.deltaTime)
        self.renderer.render(self.scene,self.camera)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--frames',type=int);parser.add_argument('--screenshot')
    args=parser.parse_args();Cubo().run(args.frames,args.screenshot)