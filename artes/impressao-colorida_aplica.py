import sys,subprocess,io
from PIL import Image
import numpy as np, cv2
base,out,x0,y0,kx,ky,svg=sys.argv[1:8];x0,y0,kx,ky=map(float,(x0,y0,kx,ky))
im=Image.open(base).convert('RGBA');W,H=im.size;a=np.array(im).astype(float);rgb=a[...,:3]
mm=lambda x,y:(int(round(x0+x*kx)),int(round(y0+y*ky)))
g=rgb.mean(-1);loc=cv2.GaussianBlur(g,(0,0),kx*5);paper=cv2.GaussianBlur(rgb,(0,0),kx*5)
# tinta = quanto o pixel é mais escuro que o papel em volta (0 papel, 1 tinta cheia)
d=np.clip((1-g/np.maximum(loc,1))/0.55,0,1)
hexc=lambda h:np.array([int(h[i:i+2],16) for i in (1,3,5)],float)
def tint(xa,ya,xb,yb,c):
    (X0,Y0),(X1,Y1)=mm(xa,ya),mm(xb,yb);sl=d[Y0:Y1,X0:X1][...,None]
    ink=paper[Y0:Y1,X0:X1]*hexc(c)/255*0.97
    rgb[Y0:Y1,X0:X1]=rgb[Y0:Y1,X0:X1]*(1-sl)+ink*sl
OURO,PETR,NAVY,MARROM='#B8892F','#1F6A73','#1E2B45','#844C29'
tint(38,43.5,62,53.5,MARROM)    # logo Drip Coffee Label
tint(30,57.5,58,67,OURO)        # sua
tint(19,70,81,84,PETR)          # MARCA
tint(42,87.5,70,100,OURO)       # aqui.
tint(24,103,76,105.2,OURO)      # fio
tint(20,107,80,112.2,NAVY)      # CAFÉ ESPECIAL · 100% ARÁBICA
tint(30,113,70,117,PETR)        # DRIP COFFEE
fw,fh=int(round(100*kx)),int(round(150*ky))
png=subprocess.run(['rsvg-convert','-w',str(fw*3),'-h',str(fh*3),svg],capture_output=True,check=True).stdout
art=Image.open(io.BytesIO(png)).convert('RGBA').resize((fw,fh),Image.LANCZOS)
L=Image.new('RGBA',(W,H),(0,0,0,0));L.paste(art,(int(round(x0)),int(round(y0))))
L=np.array(L).astype(float);al=L[...,3:4]/255*0.96*(a[...,3:4]>250)
rgb[:]=rgb*(1-al)+(rgb*L[...,:3]/255)*al
a[...,:3]=rgb
Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGBA').save(out,**({'quality':92,'method':6} if out.endswith('.webp') else {}))
