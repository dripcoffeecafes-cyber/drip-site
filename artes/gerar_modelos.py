import re,json
H=open('/home/claude/drip-site/nova-inicial.html',encoding='utf-8').read()
def pega(a,b):i=H.index(a);return H[i:H.index(b,i)+len(b)]
aviso=pega('<div class="aviso">','</div>')
head=pega('<header>','</header>')
foot=pega('<footer>','</footer>')
zap=pega('<a class="zap js-zap"','</a>')
def ajusta(x):
    x=x.replace('src="assets/','src="../assets/').replace('href="modelos/','href="')
    for ancora in ['inicio','colecao','ocasioes','clientes','como','duvidas']:
        x=x.replace(f'href="#{ancora}"',f'href="../index.html#{ancora}"')
    return x
head,foot=ajusta(head),ajusta(foot)
P={
'kraft-classico':dict(k='kraft',n='Kraft Clássico',v='33',med='10 × 12 cm · impressão em preto',p=[5.9,5.9,5.5,5.5,5.5,4.9],
  res='O drip clássico, em kraft natural, com a sua marca impressa em preto direto no sachê. O mais pedido para empresas e eventos.',
  img=[('p-kraft-cut','',''),('p-kraft','',''),('o2','cena','Drip entregue em mãos'),('o3','cena','Drip na mesa de café')],
  sp=[('Tamanho','10 × 12 cm'),('Material','Kraft natural'),('Impressão','Preto, 1 cor'),('Café','10 g, 100% Arábica'),('Origem','Região Vulcânica, MG'),('Prazo','5 dias úteis após a arte')]),
'kraft-premium':dict(k='kraftp',n='Kraft Premium',v='281',med='10 × 15 cm · preto ou colorido',p=[6.9,6.9,6.5,6.5,6.5,5.9],
  res='Formato maior, produzido só por nós, com 25% mais área para a sua arte. Em preto ou colorido, pelo mesmo preço.',
  img=[('p-kraft-premium-cut','',''),('p-kraft-premium-cor-cut','',''),('o5','cena','Drip Premium em mesa de evento'),('o7','cena','Drip Premium em kit')],
  sp=[('Tamanho','10 × 15 cm'),('Material','Kraft premium'),('Impressão','Preto ou colorido'),('Café','10 g, 100% Arábica'),('Origem','Região Vulcânica, MG'),('Prazo','5 dias úteis após a arte')]),
'branco-premium':dict(k='branco',n='Branco Premium',v='278',med='10 × 15 cm · preto ou colorido',p=[6.9,6.9,6.5,6.5,6.5,5.9],
  res='O sachê branco no formato maior, para marcas que pedem um visual limpo e moderno. Em preto ou colorido, pelo mesmo preço.',
  img=[('p-branco-cut','',''),('p-branco-cor-cut','',''),('o6','cena','Drips em caixa de presente'),('manha','cena','Drip na mão pela manhã')],
  sp=[('Tamanho','10 × 15 cm'),('Material','Branco premium'),('Impressão','Preto ou colorido'),('Café','10 g, 100% Arábica'),('Origem','Região Vulcânica, MG'),('Prazo','5 dias úteis após a arte')]),
}
brl=lambda v:('R$ %.2f'%v).replace('.',',')
CK='<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
usadas=set()
for sl,d in P.items():
    im=d['img'];usadas.update(i[0] for i in im)
    princ=f'<img id="foto" src="../assets/img/{im[0][0]}.webp" alt="Drip {d["n"]} com sua marca"{" class=cena" if im[0][1] else ""}>'
    th=''.join(f'<button class="{"ativo" if i==0 else ""}" data-src="../assets/img/{f}.webp" data-cena="{c}" aria-label="Foto {i+1}"><img src="../assets/img/{f}.webp" alt="{a or "Drip "+d["n"]}" class="{c}" loading="lazy"></button>' for i,(f,c,a) in enumerate(im))
    fx=f'''<button data-k="1"><span>50 a 100 sachês</span><b>{brl(d["p"][0])}</b></button>
<button data-k="3"><span>150 a 250 sachês<small>desconto</small></span><b>{brl(d["p"][2])}</b></button>
<button data-k="6"><span>300 sachês ou mais<small>melhor preço</small></span><b>{brl(d["p"][5])}</b></button>'''
    outros=''.join(f'''<a class="mini" href="{s2}.html"><div class="foto"><img src="../assets/img/{d2["img"][0][0]}.webp" alt="Drip {d2["n"]}"></div><div class="info"><h3>{d2["n"]}</h3><div class="med">{d2["med"]}</div><div class="de">a partir de <b>{brl(d2["p"][5])}</b> /sachê</div><span class="ver">Ver modelo</span></div></a>''' for s2,d2 in P.items() if s2!=sl)
    sp=''.join(f'<div><span>{a}</span><b>{b}</b></div>' for a,b in d['sp'])
    cor='' if d['k']=='kraft' else '<div>'+CK+'<span>Preto ou colorido pelo mesmo preço, escolhido na aprovação da arte (logo ou texto, sem foto).</span></div>'
    html=f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Drip {d["n"]} personalizado com a sua marca | Drip Coffee Label</title>
<meta name="description" content="{d["res"]} A partir de 50 sachês, de {brl(d["p"][0])} a {brl(d["p"][5])} por sachê.">
<link rel="canonical" href="https://driplabel.bloomingclub.com.br/modelos/{sl}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/novo.css">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Product","name":"Drip "+d["n"]+" personalizado","brand":{"@type":"Brand","name":"Drip Coffee Label"},"description":d["res"],"image":"https://driplabel.bloomingclub.com.br/assets/img/"+im[0][0]+".webp","offers":{"@type":"AggregateOffer","priceCurrency":"BRL","lowPrice":d["p"][5],"highPrice":d["p"][0],"availability":"https://schema.org/InStock"}},ensure_ascii=False)}</script>
</head>
<body>
{aviso}
{head}
<main class="wrap">
 <div class="migalha"><a href="../index.html">Início</a> &nbsp;/&nbsp; <a href="../index.html#colecao">Modelos</a> &nbsp;/&nbsp; {d["n"]}</div>
 <div class="pp" data-modelo="{d["k"]}" data-v="{d["v"]}" data-p='{json.dumps(d["p"])}'>
  <div class="galeria"><div class="principal">{princ}</div><div class="miniaturas">{th}</div></div>
  <div class="compra">
   <span class="sobre">Drip personalizado</span>
   <h1>{d["n"]}</h1>
   <div class="med">{d["med"]}</div>
   <p class="resumo">{d["res"]}</p>
   <div class="faixas">{fx}</div>
   <div class="qtd"><button data-passo="-1" aria-label="Menos 50">−</button><div class="n"><span class="js-n">50 sachês</span><small class="js-kit">1 kit de 50</small></div><button data-passo="1" aria-label="Mais 50">+</button></div>
   <div class="total"><span class="js-un">{brl(d["p"][0])} por sachê</span><b class="js-tot">{brl(d["p"][0]*50)}</b></div>
   <a class="btn btn-escuro js-comprar" href="#">Comprar</a>
   <a class="btn btn-linha-esc js-zap" href="#">Falar com especialista</a>
   <div class="garantias">
    <div>{CK}<span>Você manda a logo e nós montamos a arte. Nada é impresso antes do seu ok.</span></div>
    {cor}
    <div>{CK}<span>Uma arte diferente a cada 50 sachês.</span></div>
    <div>{CK}<span>Pronto em 5 dias úteis depois da aprovação. Frete calculado pelo CEP no carrinho.</span></div>
   </div>
  </div>
 </div>
</main>
<section class="sec" style="background:var(--papel);padding:80px 0">
 <div class="wrap"><div class="cab" style="margin-bottom:40px"><span class="sobre">Detalhes</span><h2 class="titulo">Ficha do produto</h2></div><div class="specs">{sp}</div></div>
</section>
<section class="sec" style="padding:80px 0">
 <div class="wrap">
  <div class="cab" style="margin-bottom:40px"><span class="sobre">Como pedir</span><h2 class="titulo">Do pedido à caixa em 4 passos</h2></div>
  <div class="passos">
   <div class="passo"><b>01</b><h3>Escolha e pague</h3><p>Quantidade aqui e pagamento na loja, com Pix, boleto ou cartão.</p></div>
   <div class="passo"><b>02</b><h3>Envie a logo</h3><p>Em vetor (AI, EPS, SVG ou PDF), pelo WhatsApp.</p></div>
   <div class="passo"><b>03</b><h3>Aprove a arte</h3><p>Mandamos a prova digital e ajustamos até ficar do seu jeito.</p></div>
   <div class="passo"><b>04</b><h3>Receba</h3><p>5 dias úteis depois da aprovação, mais o prazo da entrega.</p></div>
  </div>
 </div>
</section>
<section class="sec colecao" style="padding:80px 0">
 <div class="wrap"><div class="cab" style="margin-bottom:40px"><span class="sobre">Outros modelos</span><h2 class="titulo">Compare com</h2></div><div class="minis" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr));max-width:760px">{outros}</div></div>
</section>
{foot}
{zap}
<script>
(function(){{
 var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e quero falar com um especialista sobre o drip {d["n"]}.');
 document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP;a.target='_blank';a.rel='noopener'}});
 var c=document.querySelector('.pp'),p=JSON.parse(c.dataset.p),k=1,UTM='utm_source=drip-landing&utm_medium=site&utm_campaign=brindes&utm_content=pagina-{sl}';
 var brl=function(v){{return v.toLocaleString('pt-BR',{{style:'currency',currency:'BRL'}})}};
 var menos=c.querySelector('[data-passo="-1"]'),mais=c.querySelector('[data-passo="1"]'),fxs=c.querySelectorAll('.faixas button');
 function mostra(){{var u=p[Math.min(k-1,5)],n=k*50;
  c.querySelector('.js-n').textContent=n+' sachês';c.querySelector('.js-kit').textContent=k+(k>1?' kits':' kit')+' de 50';
  c.querySelector('.js-un').textContent=brl(u)+' por sachê';c.querySelector('.js-tot').textContent=brl(u*n);
  menos.disabled=k<=1;mais.disabled=k>=20;
  fxs.forEach(function(b){{var a=+b.dataset.k;b.classList.toggle('ativo',a===1?k<=2:a===3?(k>=3&&k<=5):k>=6)}});
  c.querySelector('.js-comprar').href='https://www.bloomingclub.com.br/checkout/cart/item/add/'+c.dataset.v+'?quantity='+k+'&'+UTM;}}
 c.addEventListener('click',function(e){{var b=e.target.closest('[data-passo]');if(b){{k=Math.max(1,Math.min(20,k+(+b.dataset.passo)));mostra()}}
  var f=e.target.closest('.faixas button');if(f){{k=+f.dataset.k;mostra()}}
  var t=e.target.closest('.miniaturas button');if(t){{var im=document.getElementById('foto');im.src=t.dataset.src;im.className=t.dataset.cena;c.querySelectorAll('.miniaturas button').forEach(function(x){{x.classList.toggle('ativo',x===t)}})}}}});
 mostra();
}})();
</script>
</body>
</html>'''
    open(f'/home/claude/drip-site/modelos/{sl}.html','w',encoding='utf-8').write(html)
print(sorted(usadas))
