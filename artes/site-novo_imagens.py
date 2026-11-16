import sys
sys.path.insert(0,'/home/claude/drip-acervo/identidade/scripts/2026-11-15')
from base_ml import *
from PIL import ImageOps, ImageEnhance
D='/home/claude/drip-site/assets/img/'
F_='fotos/2026-11_%s-fundo-transparente.png'
def tile(nome,out,w=800,h=1000,frac=.62):
    im=fundo_padrao(w,h,chao=.74); o=recorte(F_%nome)
    hh=int(h*frac); 
    if o.width/o.height*hh>w*.74: hh=int(w*.74*o.height/o.width)
    cola(im,o,w//2,int(h*.80),hh); im.save(D+out,quality=84,method=6)
for n,o in [('termolar_kraft','s-termolar'),('clrd_kraft-premium','s-clrd'),('nieto_kraft-premium','s-nieto'),('conceito-joias_branco-premium','s-conceito'),('brastelha_kraft-boa-conversa','s-brastelha'),('glfibra_kraft','s-glfibra')]:
    tile(n,o+'.webp')
tile('moido_kraft-coisas-boas','s-moido.webp',900,1125,.66)
# capa escura: estúdio escuro com três sachês reais
def fundo_escuro(w,h,chao=.72):
    y,x=np.mgrid[0:h,0:w].astype(np.float32)
    r=np.sqrt(((x-w*.5)/(w*.8))**2+((y-h*.40)/(h*.8))**2).clip(0,1)[...,None]
    c0=np.array((62,58,54),np.float32);c1=np.array((29,29,27),np.float32)
    col=c0+(c1-c0)*np.clip(r/.85,0,1)**.9
    g=((y-h*chao)/(h*(1-chao))).clip(0,1)[...,None]
    col=col*(1-.18*np.sqrt(g))+np.random.default_rng(7).normal(0,.7,col.shape)
    return Image.fromarray(col.clip(0,255).astype(np.uint8),'RGB')
w,h=1200,1500; im=fundo_escuro(w,h)
cola(im,recorte(F_%'clrd_kraft-premium'),int(w*.24),int(h*.73),int(h*.47),ang=6,sombra=230)
cola(im,recorte(F_%'termolar_kraft'),int(w*.79),int(h*.74),int(h*.37),ang=-6,sombra=230)
cola(im,recorte(F_%'nieto_branco-premium'),int(w*.52),int(h*.83),int(h*.52),sombra=240)
im.save(D+'s-capa.webp',quality=86,method=6)

# mockups oficiais (preto e colorido) no mesmo enquadramento dos recortes do site
def encaixa(m,ref,out):
    r=Image.open(D+ref).convert('RGBA');W,H=r.size;bx=r.split()[3].point(lambda v:255 if v>128 else 0).getbbox()
    m=m.crop(m.split()[3].point(lambda v:255 if v>128 else 0).getbbox())
    m=m.resize((bx[2]-bx[0],bx[3]-bx[1]),Image.LANCZOS);c=Image.new('RGBA',(W,H),(0,0,0,0));c.paste(m,(bx[0],bx[1]),m);c.save(D+out,quality=92,method=6)
import shutil,subprocess
for linha,ref in [('branco','p-branco-cut.webp'),('kraft-premium','p-kraft-premium-cut.webp')]:
    subprocess.run(['git','-C','/home/claude/drip-site','checkout','origin/main','--','assets/img/'+ref],check=True)
    encaixa(mockup_kit(linha,True),ref,ref.replace('-cut','-cor-cut'))
    encaixa(mockup_kit(linha),ref,ref.replace('-cut','-pb-cut'))
