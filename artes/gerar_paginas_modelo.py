# Gera as páginas de cada modelo (modelos/<slug>/index.html) a partir do index.html do site.
# Cabeçalho, estilos, Pixel, rodapé e WhatsApp saem do index; mudou lá, rode de novo:
#   python3 artes/gerar_paginas_modelo.py
import json, os, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()

def entre(a, b):
    i = H.index(a); return H[i:H.index(b, i) + len(b)]

estilo = entre('<style>', '</style>')
pixel = entre('<!-- Meta Pixel -->', '</noscript>')
fontes = '\n'.join(l for l in H[:H.index('<style>')].splitlines() if 'fonts.g' in l)
topo = entre('<div class="aviso">', '</div>') + '\n' + entre('<header>', '</header>')
rodape = entre('<footer>', '</footer>')
zap = entre('<a class="zap-fixo', '</a>')

def rel(x):
    x = re.sub(r'(src|href)="assets/', r'\1="../../assets/', x)
    x = re.sub(r'href="#([a-z]+)"', r'href="../../#\1"', x)
    x = x.replace('href="modelos/', 'href="../../modelos/')
    return x.replace('class="logo" href="../../#"', 'class="logo" href="../../"').replace('class="logo" href="#"', 'class="logo" href="../../"')

topo, rodape, zap = rel(topo), rel(rodape), rel(zap)

M = {
 'kraft':  dict(sl='kraft-classico', n='Kraft Clássico', v='33', p=[5.9,5.9,5.5,5.5,5.5,4.9], med='10 × 12 cm · impressão em preto',
   res='O drip clássico, em kraft natural, com a sua marca impressa em preto direto no sachê. O mais pedido para empresas e eventos.',
   fotos=[('p-kraft-cut.webp?v=3', 0, 'Drip Kraft Clássico com a sua marca'), ('p-kraft.webp', 0, 'Drip Kraft Clássico'), ('o2.webp', 1, 'Drip entregue em mãos numa reunião'), ('o3.webp', 1, 'Drip numa mesa de café')],
   ficha=[('Tamanho','10 × 12 cm'),('Material','Kraft natural'),('Impressão','Preto, 1 cor'),('Café','10 g · 80+ pontos SCA'),('Origem','Sul de Minas, Região Vulcânica'),('Produção','5 dias úteis após a arte')]),
 'kraftp': dict(sl='kraft-premium', n='Kraft Premium', v='281', p=[6.9,6.9,6.5,6.5,6.5,5.9], med='10 × 15 cm · preto ou colorido',
   res='Formato maior, produzido só por nós, com 25% mais área para a sua arte que o drip tradicional. Em preto ou colorido, pelo mesmo preço.',
   fotos=[('p-kraft-premium-pb-cut.webp', 0, 'Drip Kraft Premium impresso em preto'), ('p-kraft-premium-cor-cut.webp?v=5', 0, 'Drip Kraft Premium impresso em cores'), ('o5.webp', 1, 'Drip Kraft Premium num prato de evento'), ('o7.webp', 1, 'Drip Kraft Premium em kit de boas-vindas')],
   ficha=[('Tamanho','10 × 15 cm'),('Material','Kraft premium'),('Impressão','Preto ou colorido'),('Café','10 g · 80+ pontos SCA'),('Origem','Sul de Minas, Região Vulcânica'),('Produção','5 dias úteis após a arte')]),
 'branco': dict(sl='branco-premium', n='Branco Premium', v='278', p=[6.9,6.9,6.5,6.5,6.5,5.9], med='10 × 15 cm · preto ou colorido',
   res='O sachê branco no formato maior, para marcas que pedem um visual limpo. Em preto ou colorido, pelo mesmo preço.',
   fotos=[('p-branco-pb-cut.webp', 0, 'Drip Branco Premium impresso em preto'), ('p-branco-cor-cut.webp?v=5', 0, 'Drip Branco Premium impresso em cores'), ('o6.webp', 1, 'Drips em caixa de presente'), ('manha.webp', 1, 'Drip na mão pela manhã')],
   ficha=[('Tamanho','10 × 15 cm'),('Material','Branco premium'),('Impressão','Preto ou colorido'),('Café','10 g · 80+ pontos SCA'),('Origem','Sul de Minas, Região Vulcânica'),('Produção','5 dias úteis após a arte')]),
}
brl = lambda v: ('R$ %.2f' % v).replace('.', ',')
OK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

CSS = '''<style>
.migalha{font-size:13px;color:var(--apoio);padding:22px 0 8px}.migalha a:hover{color:var(--cafe)}
.pp{display:grid;gap:28px;padding-bottom:64px}
@media(min-width:900px){.pp{grid-template-columns:1.05fr 1fr;gap:56px;align-items:start}.pp .gal{position:sticky;top:96px}}
.gal .pr{position:relative;background:var(--papel);border-radius:var(--r);aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.gal .pr img{max-height:84%;max-width:84%;width:auto;height:auto;object-fit:contain}
.gal .pr img.cena{max-width:100%;max-height:100%;width:100%;height:100%;object-fit:cover}
.gal .pr .tarja{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);background:var(--ink);color:#fff;font:700 11px/1 'Open Sans',sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:8px 14px;border-radius:4px;white-space:nowrap}
.gal .mi{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}
.gal .mi button{background:var(--papel);border-radius:12px;aspect-ratio:1/1;border:2px solid transparent;cursor:pointer;padding:0;overflow:hidden;display:flex;align-items:center;justify-content:center}
.gal .mi button[aria-current="true"]{border-color:var(--ink)}
.gal .mi img{max-height:80%;width:auto}.gal .mi img.cena{max-height:none;width:100%;height:100%;object-fit:cover}
.info h1{font-size:clamp(34px,4.2vw,48px);line-height:1.08;margin:10px 0 6px}
.info .med{color:var(--apoio);font-size:15px}
.info .res{font-size:16.5px;margin:18px 0 22px}
.fx{border:1.5px solid var(--borda);border-radius:16px;overflow:hidden;margin-bottom:16px}
.fx button{display:flex;justify-content:space-between;align-items:center;gap:10px;width:100%;padding:14px 18px;background:#fff;border:0;border-bottom:1px solid var(--fundo);font:400 15px 'Open Sans',sans-serif;color:var(--texto);cursor:pointer;text-align:left}
.fx button:last-child{border-bottom:0}
.fx button b{font-weight:700;color:var(--ink);font-size:17px}
.fx button small{display:inline-block;margin-left:8px;font-size:12px;font-weight:700;color:var(--cafe)}
.fx button[aria-pressed="true"]{background:var(--papel);box-shadow:inset 4px 0 0 var(--cafe)}
.linha-q{display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--papel);border-radius:16px;padding:12px 16px}
.linha-q .tot{text-align:right;font-size:13px;color:var(--apoio)}.linha-q .tot b{display:block;font-size:24px;color:var(--ink)}
.info .btn{width:100%;margin-top:12px}
.gar{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:10px}
.gar li{display:flex;gap:10px;font-size:14.5px}
.gar svg{flex:0 0 20px;width:20px;height:20px;fill:none;stroke:var(--cafe);stroke-width:2;margin-top:1px}
.ficha{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--borda)}
@media(min-width:900px){.ficha{grid-template-columns:repeat(3,1fr)}}
.ficha div{padding:20px 16px 20px 0;border-bottom:1px solid var(--borda)}
.ficha span{display:block;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--apoio);margin-bottom:4px}
.ficha b{font-size:17px;color:var(--ink)}
.passos4{display:grid;gap:20px;counter-reset:p}
@media(min-width:900px){.passos4{grid-template-columns:repeat(4,1fr)}}
.passos4 div{background:#fff;border-radius:var(--r);padding:22px}
.passos4 b{display:block;font-size:28px;color:var(--cafe);line-height:1}
.passos4 h3{font-size:17px;margin:10px 0 6px}.passos4 p{font-size:14.5px;color:var(--apoio)}
.outros{display:grid;gap:16px;max-width:760px;margin:0 auto}
@media(min-width:700px){.outros{grid-template-columns:1fr 1fr}}
</style>'''

for k, d in M.items():
    f0 = d['fotos'][0]
    tarja = '<span class="tarja">Impressão só em preto</span>' if k == 'kraft' else ''
    mi = ''.join('<button type="button" aria-current="%s" data-src="../../assets/img/%s" data-cena="%d" data-alt="%s" aria-label="Foto %d"><img src="../../assets/img/%s" alt="" class="%s" loading="lazy"></button>'
                 % ('true' if i == 0 else 'false', f, c, a, i + 1, f, 'cena' if c else '') for i, (f, c, a) in enumerate(d['fotos']))
    fx = ('<button type="button" data-k="1"><span>50 ou 100 sachês</span><b>%s</b></button>'
          '<button type="button" data-k="3"><span>150 a 250 sachês<small>desconto</small></span><b>%s</b></button>'
          '<button type="button" data-k="6"><span>300 sachês ou mais<small>melhor preço</small></span><b>%s</b></button>') % (brl(d['p'][0]), brl(d['p'][2]), brl(d['p'][5]))
    cor = '' if k == 'kraft' else '<li>%s<span>Preto ou colorido pelo mesmo preço, escolhido na aprovação da arte. Colorido para logo ou texto, sem foto nem fundo cheio.</span></li>' % OK
    ficha = ''.join('<div><span>%s</span><b>%s</b></div>' % x for x in d['ficha'])
    outros = ''.join('''<a class="prod mini" href="../%s/"><div class="img"><img src="../../assets/img/%s" alt="Drip %s" loading="lazy"></div><div class="tx"><h3>%s</h3><p class="med">%s</p><p class="de">a partir de <b>%s</b>/sachê</p><span class="ver">Ver modelo</span></div></a>'''
                     % (d2['sl'], d2['fotos'][0][0], d2['n'], d2['n'], d2['med'], brl(d2['p'][5])) for k2, d2 in M.items() if k2 != k)
    url = 'https://driplabel.bloomingclub.com.br/modelos/%s/' % d['sl']
    desc = '%s A partir de 50 sachês, de %s a %s por sachê.' % (d['res'], brl(d['p'][5]), brl(d['p'][0]))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": "Drip " + d['n'] + " personalizado", "description": d['res'],
         "image": "https://driplabel.bloomingclub.com.br/assets/img/" + f0[0].split('?')[0],
         "brand": {"@type": "Brand", "name": "Drip Coffee Label"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "BRL", "lowPrice": d['p'][5], "highPrice": d['p'][0], "availability": "https://schema.org/InStock", "url": url}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://driplabel.bloomingclub.com.br/"},
            {"@type": "ListItem", "position": 2, "name": "Modelos", "item": "https://driplabel.bloomingclub.com.br/#modelos"},
            {"@type": "ListItem", "position": 3, "name": d['n'], "item": url}]}]}
    pg = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Drip {d['n']} personalizado com a sua marca | Drip Coffee Label</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Drip Coffee Label">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Drip {d['n']} personalizado | Drip Coffee Label">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://driplabel.bloomingclub.com.br/assets/img/og-drip-coffee-label.jpg">
<link rel="icon" href="../../favicon.ico">
{fontes}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{estilo}
{CSS}
{pixel}
</head>
<body>
{topo}
<main class="wrap">
  <nav class="migalha" aria-label="Você está em"><a href="../../">Início</a> / <a href="../../#modelos">Modelos</a> / {d['n']}</nav>
  <div class="pp" data-modelo="{k}">
    <div class="gal">
      <div class="pr"><img id="foto" src="../../assets/img/{f0[0]}" alt="{f0[2]}" width="900" height="900">{tarja}</div>
      <div class="mi">{mi}</div>
    </div>
    <div class="info">
      <span class="olho">Drip personalizado</span>
      <h1>{d['n']}</h1>
      <p class="med">{d['med']}</p>
      <p class="res">{d['res']}</p>
      <div class="fx" role="group" aria-label="Preço por quantidade">{fx}</div>
      <div class="linha-q">
        <div class="stepper"><button type="button" data-passo="-1" aria-label="Menos 50 sachês">−</button><output class="js-n tnum">50 sachês</output><button type="button" data-passo="1" aria-label="Mais 50 sachês">+</button></div>
        <div class="tot"><span class="js-un">{brl(d['p'][0])} por sachê</span><b class="js-tot tnum">{brl(d['p'][0]*50)}</b></div>
      </div>
      <a class="btn btn-cafe js-comprar" data-produto="{k}" href="#" target="_blank" rel="noopener">Comprar</a>
      <a class="btn btn-linha js-zap" data-origem="pagina-{k}" href="#" target="_blank" rel="noopener">Falar com um especialista</a>
      <ul class="gar">
        <li>{OK}<span>Você manda a logo e nós montamos a arte. Nada é impresso antes do seu ok.</span></li>
        {cor}
        <li>{OK}<span>Uma arte diferente a cada 50 sachês.</span></li>
        <li>{OK}<span>Pronto em 5 dias úteis depois da aprovação. Frete calculado pelo CEP no carrinho.</span></li>
      </ul>
    </div>
  </div>
</main>
<section class="sec cinza">
  <div class="wrap">
    <div class="cab"><span class="olho">Detalhes</span><h2>Ficha do produto</h2></div>
    <div class="ficha">{ficha}</div>
    <div class="cab" style="margin-top:56px"><span class="olho">Como funciona</span><h2>Do pedido à caixa em 4 passos</h2></div>
    <div class="passos4">
      <div><b>01</b><h3>Escolha e pague</h3><p>Quantidade aqui e pagamento na loja, com Pix, boleto ou cartão.</p></div>
      <div><b>02</b><h3>Envie a sua logo</h3><p>Em vetor (AI, EPS, SVG ou PDF), pelo WhatsApp.</p></div>
      <div><b>03</b><h3>Aprove a arte</h3><p>Mandamos a prova digital e ajustamos até ficar do seu jeito.</p></div>
      <div><b>04</b><h3>Receba</h3><p>Produção em 5 dias úteis depois da aprovação, mais o prazo da entrega.</p></div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Outros modelos</span><h2>Compare com</h2></div>
    <div class="outros">{outros}</div>
  </div>
</section>
{rodape}
{zap}
<script>
(function(){{
  var M={json.dumps({k: dict(n=d['n'], p=d['p'], v=d['v'])}, ensure_ascii=False)}['{k}'];
  var UTM='utm_source=drip-landing&utm_medium=site&utm_campaign=brindes&utm_content=pagina-{k}';
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e quero falar com um especialista sobre o drip '+M.n+'.');
  var brl=function(v){{return v.toLocaleString('pt-BR',{{style:'currency',currency:'BRL'}})}};
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP}});
  var c=document.querySelector('.pp'),k=1,menos=c.querySelector('[data-passo="-1"]'),mais=c.querySelector('[data-passo="1"]'),fx=c.querySelectorAll('.fx button');
  function mostra(){{var u=M.p[Math.min(k-1,5)],n=k*50;
    c.querySelector('.js-n').textContent=n+' sachês';c.querySelector('.js-un').textContent=brl(u)+' por sachê';c.querySelector('.js-tot').textContent=brl(u*n);
    menos.disabled=k<=1;mais.disabled=k>=20;
    fx.forEach(function(b){{var a=+b.dataset.k;b.setAttribute('aria-pressed',String(a===1?k<=2:a===3?(k>=3&&k<=5):k>=6))}});
    c.querySelector('.js-comprar').href='https://www.bloomingclub.com.br/checkout/cart/item/add/'+M.v+'?quantity='+k+'&'+UTM}}
  c.addEventListener('click',function(e){{
    var b=e.target.closest('[data-passo]');if(b){{k=Math.max(1,Math.min(20,k+(+b.dataset.passo)));mostra();return}}
    var f=e.target.closest('.fx button');if(f){{k=+f.dataset.k;mostra();return}}
    var t=e.target.closest('.mi button');if(t){{var im=document.getElementById('foto'),tj=c.querySelector('.pr .tarja');im.src=t.dataset.src;im.alt=t.dataset.alt;im.className=t.dataset.cena==='1'?'cena':'';
      if(tj)tj.style.display=t.dataset.cena==='1'?'none':'';
      c.querySelectorAll('.mi button').forEach(function(x){{x.setAttribute('aria-current',String(x===t))}})}}}});
  mostra();
  // Pixel: igual ao da inicial. Aqui a pessoa já está vendo o produto, então o WhatsApp também conta como Lead.
  var PX_DRIP='1636404041306148',PX_NUVEM='29552796950978987';
  function ev(nome,dados){{try{{if(!window.fbq)return;dados=dados||{{}};
    if(nome==='InitiateCheckout'){{fbq('trackSingle',PX_DRIP,nome,dados);fbq('trackSingleCustom',PX_NUVEM,'IrParaLoja',dados)}}
    else{{fbq('track',nome,dados)}}}}catch(e){{}}}}
  try{{sessionStorage.setItem('drip_viu','1')}}catch(x){{}}
  ev('ViewContent',{{content_type:'product',content_ids:['{k}'],content_name:'pagina-{k}'}});
  var leadFeito=false;
  function lead(nome){{try{{if(leadFeito)return;try{{if(sessionStorage.getItem('drip_lead')){{leadFeito=true;return}}}}catch(x){{}}
    if(!window.fbq)return;fbq('trackSingle',PX_NUVEM,'Lead',{{content_name:nome}});leadFeito=true;
    try{{sessionStorage.setItem('drip_lead','1')}}catch(x){{}}}}catch(e){{}}}}
  document.addEventListener('click',function(e){{
    var a=e.target.closest&&e.target.closest('a');if(!a)return;
    if(a.classList.contains('js-zap')){{var o=a.getAttribute('data-origem')||'whatsapp';ev('Contact',{{content_name:o}});lead('whatsapp-'+o)}}
    else if(a.hasAttribute('data-produto')){{var pr=a.getAttribute('data-produto');ev('InitiateCheckout',{{content_type:'product',content_ids:[pr],content_name:'pagina-'+pr}});lead('loja-'+pr)}}
  }},true);
}})();
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(RAIZ, 'modelos', d['sl']), exist_ok=True)
    open(os.path.join(RAIZ, 'modelos', d['sl'], 'index.html'), 'w', encoding='utf-8').write(pg)
    print('modelos/%s/' % d['sl'])
