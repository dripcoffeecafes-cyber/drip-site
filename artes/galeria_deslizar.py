# Galeria das páginas de produto (Adriano, 28/11): no celular a foto acompanha o dedo; setas, contador e troca lateral.
# Usa os botões das miniaturas (.mi button): cada passo é um clique na miniatura seguinte, então o resto da página não muda.
GAL = """<style>.gal .pr{position:relative;touch-action:pan-y;user-select:none;-webkit-user-select:none}.gal .pr img{-webkit-user-drag:none}.gal .gal-bt{position:absolute;top:50%;transform:translateY(-50%);z-index:3;width:34px;height:34px;border-radius:50%;border:0;background:rgba(30,20,16,.22);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;opacity:.85;transition:opacity .2s,background .2s}.gal .gal-bt:hover{opacity:1;background:rgba(30,20,16,.4)}.gal .gal-ant{left:8px}.gal .gal-prox{right:8px}.gal .gal-bt svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}.gal .gal-n{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);z-index:3;background:rgba(30,20,16,.35);color:#fff;font-size:10.5px;letter-spacing:.06em;padding:3px 10px}</style>
<script>(function(){var im=document.getElementById('foto');if(!im)return;var pr=im.closest('.pr'),bs=[].slice.call(document.querySelectorAll('.mi button'));if(!pr||bs.length<2)return;
pr.style.overflow='hidden';
function at(){for(var i=0;i<bs.length;i++){if(bs[i].getAttribute('aria-current')==='true')return i}return 0}
var n=document.createElement('span');n.className='gal-n';pr.appendChild(n);function conta(){n.textContent=(at()+1)+' / '+bs.length}
var calmo=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,dir=0,cl=null,T='transform .42s cubic-bezier(.22,.7,.2,1)';
function pre(i){var b=bs[(i+bs.length)%bs.length];if(b&&b.dataset.src){var x=new Image();x.src=b.dataset.src}}
/* antes de a miniatura trocar a foto: copia a foto atual por cima, para ela sair pelo lado enquanto a nova entra */
function copia(){if(calmo)return;if(cl&&cl.parentNode)cl.parentNode.removeChild(cl);cl=im.cloneNode(false);cl.removeAttribute('id');cl.setAttribute('aria-hidden','true');
cl.style.cssText='position:absolute;left:'+im.offsetLeft+'px;top:'+im.offsetTop+'px;width:'+im.offsetWidth+'px;height:'+im.offsetHeight+'px;margin:0;z-index:2;transition:none;transform:translateX(0)';pr.appendChild(cl)}
function corre(){if(calmo||!dir)return;var d=dir,c=cl;dir=0;im.style.transition='none';im.style.transform='translateX('+(d*100)+'%)';void im.offsetWidth;
requestAnimationFrame(function(){im.style.transition=T;im.style.transform='translateX(0)';if(c){c.style.transition=T;c.style.transform='translateX('+(-d*100)+'%)';setTimeout(function(){if(c.parentNode)c.parentNode.removeChild(c)},460)}})}
var arr=false;bs.forEach(function(b,i){b.addEventListener('click',function(){var a=at();if(i!==a&&!arr){dir=i>a?1:-1;copia()}setTimeout(function(){conta();if(im.complete)corre();else im.addEventListener('load',corre,{once:true});pre(i+1);pre(i-1)},0)})});
function vai(d){var a=at(),k=(a+d+bs.length)%bs.length;bs[k].click();if(!calmo){dir=d}}
[['gal-ant',-1,'M15 5l-7 7 7 7','Foto anterior'],['gal-prox',1,'M9 5l7 7-7 7','Próxima foto']].forEach(function(s){var b=document.createElement('button');b.type='button';b.className='gal-bt '+s[0];b.setAttribute('aria-label',s[3]);b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="'+s[2]+'"/></svg>';b.addEventListener('click',function(e){e.preventDefault();vai(s[1])});pr.appendChild(b)});
/* Celular: a foto acompanha o dedo; a vizinha aparece ao lado e, ao soltar, completa a troca ou volta */
var x0=null,y0=0,dx=0,modo=0,viz={},W=0,EM='transform .3s cubic-bezier(.22,.7,.2,1)';
function lado(d){var b=bs[(at()+d+bs.length)%bs.length],v=document.createElement('img');v.src=b.dataset.src;v.alt='';v.setAttribute('aria-hidden','true');v.className=b.dataset.cena==='0'?'':'cena';
v.style.cssText='position:absolute;left:'+im.offsetLeft+'px;top:'+im.offsetTop+'px;width:'+im.offsetWidth+'px;height:'+im.offsetHeight+'px;margin:0;z-index:2;transition:none;transform:translateX('+(d*W)+'px)';pr.appendChild(v);return v}
function poe(x,t){im.style.transition=t;im.style.transform='translateX('+x+'px)';[-1,1].forEach(function(d){if(viz[d]){viz[d].style.transition=t;viz[d].style.transform='translateX('+(x+d*W)+'px)'}})}
function limpa(){[-1,1].forEach(function(d){if(viz[d]&&viz[d].parentNode)viz[d].parentNode.removeChild(viz[d])});viz={}}
pr.addEventListener('touchstart',function(e){if(e.touches.length>1)return;var t=e.touches[0];x0=t.clientX;y0=t.clientY;dx=0;modo=0;W=pr.clientWidth},{passive:true});
pr.addEventListener('touchmove',function(e){if(x0===null)return;var t=e.touches[0],mx=t.clientX-x0,my=t.clientY-y0;
if(!modo){if(Math.abs(mx)<8&&Math.abs(my)<8)return;modo=Math.abs(mx)>Math.abs(my)?1:2;if(modo===1){if(cl&&cl.parentNode)cl.parentNode.removeChild(cl);limpa();viz[-1]=lado(-1);viz[1]=lado(1)}}
if(modo!==1)return;if(e.cancelable)e.preventDefault();dx=mx;poe(dx,'none')},{passive:false});
pr.addEventListener('touchend',function(){if(x0===null)return;x0=null;if(modo!==1){modo=0;return}modo=0;
if(Math.abs(dx)>W*0.18){var d=dx<0?1:-1;poe(-d*W,EM);setTimeout(function(){arr=true;bs[(at()+d+bs.length)%bs.length].click();arr=false;dir=0;im.style.transition='none';im.style.transform='translateX(0)';
var fim=function(){limpa()};if(im.complete)setTimeout(fim,30);else im.addEventListener('load',fim,{once:true});conta();pre(at()+d)},300)}
else{poe(0,EM);setTimeout(limpa,320)}},{passive:true});
pre(1);pre(-1);conta()})();</script>"""
