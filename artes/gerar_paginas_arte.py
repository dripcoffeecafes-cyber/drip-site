# Página de cada arte pronta (modelos/<slug>/index.html) a partir do catalogo/modelos.json (itens com linha "pronta" e bloco "pagina").
# Mesmo padrão das páginas dos personalizados (gerar_paginas_modelo.py): galeria, preço por quantidade, Comprar, sobre o produto,
# o café, ficha, dúvidas. Imagens em assets/img/artes/<slug>/NN.webp (1100 px) e NN-p.webp (miniatura), do drip-arts produtos/<código>/loja/.
# Comprar leva ao carrinho do www com ?drip_artes= (o checkout-drip.js põe o produto do sachê e grava a arte no campo extra "arte").
# Rode depois de mudar o JSON ou o index:
#   python3 artes/gerar_paginas_arte.py
import json, os, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
C = json.load(open(os.path.join(RAIZ, 'catalogo', 'modelos.json'), encoding='utf-8'))
AP = C['artes_prontas']
SACHE = {s['id']: s['nome'] for s in C['saches']}
# Estilo da página de produto: o mesmo dos personalizados (bloco CSS do gerar_paginas_modelo.py)
CSS = re.search(r"CSS = '''(.*?)'''", open(os.path.join(RAIZ, 'artes', 'gerar_paginas_modelo.py'), encoding='utf-8').read(), re.S).group(1)
CSS = CSS.replace('</style>', '.aviso-humor{font-size:14px;color:var(--apoio);border-left:2px solid var(--cafe);padding:2px 0 2px 12px;margin:16px 0 0}\n</style>')

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
    x = re.sub(r'href="(modelos|empresas|casamentos|eventos|fim-de-ano|consultorios-e-escritorios|sobre|contato|trocas-e-devolucoes|privacidade|condicoes-de-compra)/', r'href="../../\1/', x)
    return x.replace('class="logo" href="../../#"', 'class="logo" href="../../"').replace('class="logo" href="#"', 'class="logo" href="../../"')
topo, rodape, zap = rel(topo), rel(rodape), rel(zap)

esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
brl = lambda v: ('R$ %.2f' % v).replace('.', ',')
OK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
MAT = {'kraft-classico': ('10 × 12 cm', 'Kraft natural'), 'kraft-premium': ('10 × 15 cm', 'Kraft premium'), 'branco-premium': ('10 × 15 cm', 'Branco premium')}
SITE = 'https://driplabel.bloomingclub.com.br/'

def faq(i, pg):
    q = [('A arte é igual às fotos?', 'Sim. A arte é da Drip Coffee Label e vai exatamente como nas fotos. Não é personalizada e você não precisa enviar nenhum arquivo.'),
         ('Qual é a quantidade mínima?', 'A partir de %d sachês, de %d em %d.' % (AP['min_sache'], AP['passo'], AP['passo'])),
         ('Posso juntar artes diferentes no mesmo pedido?', 'Sim. Volte aos modelos e coloque outras artes no carrinho. Artes do mesmo sachê somam para a faixa de preço: o preço por sachê cai em %s sachês.' % (lambda l: ', '.join(l[:-1]) + ' e ' + l[-1] if len(l) > 1 else l[0])([str(x[0]) for x in AP['faixas'][i['sache']][1:]])),
         ('Dá para colocar a minha marca?', 'Na arte pronta, não. Para drip com a sua logo, nome ou frase, veja os modelos personalizados, a partir de 50 sachês, com a arte criada por nós sem custo.'),
         ('Qual é o prazo?', 'Produzimos em %d dias úteis depois da confirmação do pagamento. Em seguida vem o prazo da transportadora, que aparece no carrinho junto com o frete, depois de informar o CEP.' % AP.get('prazo_dias', 2)),
         ('Qual é a validade do café?', '6 meses. O café é 100% arábica, torra média, moído na medida para o preparo em drip.'),
         ('Precisa de cafeteira?', 'Não. Abra o sachê, encaixe as abas na borda da xícara, despeje água quente aos poucos e aguarde coar.'),
         ('Tem nota fiscal?', 'Sim, em todos os pedidos, para empresa ou pessoa física.')]
    return ''.join('<details><summary>%s</summary><p>%s</p></details>' % x for x in q), q

n_pag = 0
for i in [x for x in C['itens'] if x.get('linha') == 'pronta' and x.get('publicado', True) and x.get('pagina')]:
    pg, sl, sa = i['pagina'], i['slug'], i['sache']
    fx_ = AP['faixas'][sa]
    p_min, p_max = fx_[-1][1], fx_[0][1]
    pid = AP['produtos'].get(sa, '')
    fotos = [('artes/%s/%s.webp' % (sl, n), 'artes/%s/%s-p.webp' % (sl, n), a) for n, a in pg['fotos']]
    f0 = fotos[0]
    mi = ''.join('<button type="button" aria-current="%s" data-src="../../assets/img/%s" data-cena="1" data-alt="%s" aria-label="Foto %d"><img src="../../assets/img/%s" alt="" class="cena" width="120" height="120" loading="lazy"></button>'
                 % ('true' if k == 0 else 'false', g, esc(a), k + 1, p) for k, (g, p, a) in enumerate(fotos))
    def faixa_txt(k):
        de = fx_[k][0]; ate = fx_[k + 1][0] - 1 if k + 1 < len(fx_) else None
        return '%d a %d sachês' % (de, ate) if ate else '%d sachês ou mais' % de
    tag = lambda k: '' if k == 0 else ('<small>melhor preço</small>' if k == len(fx_) - 1 else '<small>desconto</small>')
    fx = ''.join('<button type="button" data-q="%d"><span>%s%s</span><b>%s</b></button>' % (fx_[k][0], faixa_txt(k), tag(k), brl(fx_[k][1])) for k in range(len(fx_)))
    tam, mat = MAT[sa]
    ficha = ''.join('<div><span>%s</span><b>%s</b></div>' % x for x in [('Tamanho', tam), ('Material', mat), ('Impressão', pg.get('impressao', 'Colorida')), ('Café', '10 g · 80+ pontos SCA'), ('Origem', 'Sul de Minas, Região Vulcânica'), ('Validade', '6 meses'), ('Produção', '%d dias úteis' % AP.get('prazo_dias', 2))])
    url = SITE + 'modelos/%s/' % sl
    nome = i['nome']
    desc = '%s Drip coffee de arte pronta, café especial 80+ SCA, a partir de %d sachês, de %s a %s por sachê.' % (pg['chamada'], AP['min_sache'], brl(p_min), brl(p_max))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "@id": url + "#produto", "url": url, "sku": i.get('codigo', sl), "name": "Drip Coffee " + nome, "description": pg['resumo'],
         "category": "Café especial", "material": mat, "image": [SITE + 'assets/img/' + g for g, p, a in fotos],
         "brand": {"@type": "Brand", "name": "Drip Coffee Label"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "BRL", "lowPrice": p_min, "highPrice": p_max, "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition", "url": url, "offerCount": len(fx_), "seller": {"@id": SITE + "#organization"}}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faq(i, pg)[1]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Modelos", "item": SITE + "modelos/"},
            {"@type": "ListItem", "position": 3, "name": nome, "item": url}]}]}
    aviso = '<p class="aviso-humor"><b>Aviso de humor:</b> %s</p>' % esc(pg['aviso']) if pg.get('aviso') else ''
    cfg = {'n': nome, 's': SACHE.get(sa, sa), 'p': pid, 'f': fx_, 'min': AP['min_sache'], 'passo': AP['passo'], 'k': sl}
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(pg.get('titulo_seo', 'Drip Coffee ' + nome))} | Drip Coffee Label</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Drip Coffee Label">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Drip Coffee {esc(nome)} | Drip Coffee Label">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}assets/img/{f0[0]}">
<meta property="og:image:width" content="1100">
<meta property="og:image:height" content="1100">
<meta property="og:locale" content="pt_BR">
<meta property="product:price:amount" content="{p_min:.2f}">
<meta property="product:price:currency" content="BRL">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="image" href="../../assets/img/{f0[0]}" fetchpriority="high">
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
  <nav class="migalha" aria-label="Você está em"><a href="../../">Início</a> / <a href="../">Modelos</a> / {esc(nome)}</nav>
  <div class="pp" data-modelo="{sl}">
    <div class="gal">
      <div class="pr"><img id="foto" src="../../assets/img/{f0[0]}" alt="{esc(f0[2])}" width="1100" height="1100" class="cena"></div>
      <div class="mi">{mi}</div>
    </div>
    <div class="info">
      <span class="olho">Arte pronta</span>
      <h1>{esc(nome)}</h1>
      <p class="med">{esc(i['med'])}</p>
      <p class="res">{esc(pg['resumo'])}</p>
      <div class="fx" role="group" aria-label="Preço por quantidade">{fx}</div>
      <div class="linha-q">
        <div class="stepper"><button type="button" data-passo="-1" aria-label="Menos {AP['passo']} sachês">−</button><output class="js-n tnum">{AP['min_sache']} sachês</output><button type="button" data-passo="1" aria-label="Mais {AP['passo']} sachês">+</button></div>
        <div class="tot"><span class="js-un">{brl(p_max)} por sachê</span><b class="js-tot tnum">{brl(p_max * AP['min_sache'])}</b></div>
      </div>
      <a class="btn btn-cafe js-comprar" data-produto="{sl}" href="#">Comprar</a>
      <a class="btn btn-linha js-zap" data-origem="pagina-{sl}" href="#" target="_blank" rel="noopener">Falar com a gente</a>
      <ul class="gar">
        <li>{OK}<span>Arte pronta, exatamente como nas fotos. Você não precisa enviar nenhum arquivo.</span></li>
        <li>{OK}<span>A partir de {AP['min_sache']} sachês. Artes do mesmo sachê somam para a faixa de preço.</span></li>
        <li>{OK}<span>Pronto em {AP.get('prazo_dias', 2)} dias úteis depois da confirmação do pagamento, mais o prazo da transportadora, calculado pelo CEP no carrinho.</span></li>
        <li>{OK}<span>Café especial 80+ pontos SCA, de origem única.</span></li>
      </ul>
      {aviso}
    </div>
  </div>
</main>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Sobre o produto</span><h2>Drip Coffee {esc(nome)}</h2></div>
    <div class="sobre2">
      <div><h3>Para quem é</h3><ul class="lst">{''.join('<li>%s</li>' % esc(x) for x in pg['para_quem'])}</ul><p style="margin-top:14px">{esc(pg['chamada'])}</p></div>
      <div><h3>O café é sério</h3><ul class="lst"><li>Café especial com laudo: 80+ pontos SCA, avaliado por Q-Grader.</li><li>Origem única: Sul de Minas, Região Vulcânica.</li><li>100% arábica, torra média, moído na medida para o drip.</li><li>10 g por sachê. Validade de 6 meses.</li><li>Dosado, selado e conferido um a um, em pequenos lotes.</li></ul></div>
      <div><h3>O sachê</h3><ul class="lst"><li>Sachê {esc(mat.lower())} {tam}, com filtro interno.</li><li>Impressão {esc(pg.get('impressao', 'colorida').lower())}.</li><li>Arte da Drip Coffee Label, igual às fotos. Não é personalizado.</li></ul></div>
      <div><h3>Como preparar</h3><p>Abra o sachê na linha indicada, encaixe as abas na borda da xícara, despeje água quente aos poucos e espere escoar. Não precisa de cafeteira.</p><h3 style="margin-top:22px">Quer com a sua marca?</h3><p>Também personalizamos o sachê com a sua logo, nome ou frase, a partir de 50 unidades, com a arte criada por nós sem custo. <a href="../" style="text-decoration:underline">Veja os modelos personalizados</a>.</p></div>
    </div>
  </div>
</section>
<section class="sec cinza">
  <div class="wrap">
    <div class="cab"><span class="olho">Detalhes</span><h2>Ficha do produto</h2></div>
    <div class="ficha">{ficha}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Dúvidas</span><h2>Antes de pedir o {esc(nome)}</h2></div>
    <div class="faq">{faq(i, pg)[0]}</div>
    <p style="text-align:center;margin-top:28px;font-size:14px;color:var(--apoio)">Emitimos nota fiscal em todos os pedidos, para empresa ou pessoa física.</p>
  </div>
</section>
{rodape}
{zap}
<script>
(function(){{
  var A={json.dumps(cfg, ensure_ascii=False)};
  var UTM='utm_source=drip-landing&utm_medium=site&utm_campaign=brindes&utm_content=pagina-'+A.k;
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e tenho uma dúvida sobre o drip '+A.n+'.');
  var brl=function(v){{return v.toLocaleString('pt-BR',{{style:'currency',currency:'BRL'}})}};
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP}});
  var c=document.querySelector('.pp'),q=A.min,menos=c.querySelector('[data-passo="-1"]'),fx=c.querySelectorAll('.fx button');
  function preco(n){{var p=A.f[0][1];A.f.forEach(function(x){{if(n>=x[0])p=x[1]}});return p}}
  function mostra(){{var u=preco(q);
    c.querySelector('.js-n').textContent=q+' sachês';c.querySelector('.js-un').textContent=brl(u)+' por sachê';c.querySelector('.js-tot').textContent=brl(u*q);
    menos.disabled=q<=A.min;
    fx.forEach(function(b,k){{var de=A.f[k][0],ate=k+1<A.f.length?A.f[k+1][0]:1e9;b.setAttribute('aria-pressed',String(q>=de&&q<ate))}});
    var bt=c.querySelector('.js-comprar');
    if(A.p){{bt.href='https://www.bloomingclub.com.br/checkout/cart?drip_artes='+encodeURIComponent(JSON.stringify([{{p:A.p,s:A.s,q:q,a:[[A.n,q]]}}]))+'&'+UTM;bt.removeAttribute('target')}}
    else{{bt.href='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Quero o drip '+A.n+' ('+A.s+'), '+q+' sachês.');bt.target='_blank'}}}}
  c.addEventListener('click',function(e){{
    var b=e.target.closest('[data-passo]');if(b){{q=Math.max(A.min,Math.min(5000,q+(+b.dataset.passo)*A.passo));mostra();return}}
    var f=e.target.closest('.fx button');if(f){{q=Math.max(A.min,+f.dataset.q);mostra();return}}
    var t=e.target.closest('.mi button');if(t){{var im=document.getElementById('foto');im.src=t.dataset.src;im.alt=t.dataset.alt;
      c.querySelectorAll('.mi button').forEach(function(x){{x.setAttribute('aria-current',String(x===t))}})}}}});
  mostra();
  // Pixel: igual ao das páginas dos personalizados (Comprar = InitiateCheckout no Pixel da Drip + Lead Drip no Pixel_Nuvem).
  var PX_DRIP='1636404041306148',PX_NUVEM='29552796950978987';
  function ev(nome,dados){{try{{if(!window.fbq)return;dados=dados||{{}};
    if(nome==='InitiateCheckout'){{fbq('trackSingle',PX_DRIP,nome,dados);fbq('trackSingleCustom',PX_NUVEM,'IrParaLoja',dados)}}
    else{{fbq('track',nome,dados)}}}}catch(e){{}}}}
  try{{sessionStorage.setItem('drip_viu','1')}}catch(x){{}}
  ev('ViewContent',{{content_type:'product',content_ids:[A.k],content_name:'pagina-'+A.k}});
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
    os.makedirs(os.path.join(RAIZ, 'modelos', sl), exist_ok=True)
    with open(os.path.join(RAIZ, 'modelos', sl, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(html)
    n_pag += 1
    print('modelos/%s/' % sl)

# Sitemap: uma entrada por arte pronta (depois de /modelos/)
sp = os.path.join(RAIZ, 'sitemap.xml')
S = open(sp, encoding='utf-8').read()
for i in [x for x in C['itens'] if x.get('linha') == 'pronta' and x.get('publicado', True) and x.get('pagina')]:
    loc = '<loc>%smodelos/%s/</loc>' % (SITE, i['slug'])
    if loc not in S:
        S = S.replace('</urlset>', '  <url>\n    %s\n    <lastmod>2026-11-24</lastmod>\n  </url>\n</urlset>' % loc, 1)
with open(sp, 'w', encoding='utf-8') as fh:
    fh.write(S)

# llms.txt: seção "Artes prontas" refeita a partir do modelos.json (entre "## Artes prontas" e "## Para quem")
lp = os.path.join(RAIZ, 'llms.txt')
L = open(lp, encoding='utf-8').read()
if '## Artes prontas' in L and '## Para quem' in L:
    fxs = AP['faixas']
    linhas = ['## Artes prontas',
              '- [Todas as artes prontas](%smodelos/?tema=arte-pronta): drips com arte da Drip, iguais às fotos, sem arquivo para enviar. A partir de %d sachês, de %d em %d; %s a %s nos premium e %s a %s no Kraft Clássico, conforme a quantidade.' % (
                  SITE, AP['min_sache'], AP['passo'], AP['passo'], brl(fxs['branco-premium'][0][1]), brl(fxs['branco-premium'][-1][1]), brl(fxs['kraft-classico'][0][1]), brl(fxs['kraft-classico'][-1][1]))]
    for i in [x for x in C['itens'] if x.get('linha') == 'pronta' and x.get('publicado', True) and x.get('pagina')]:
        linhas.append('- [%s](%smodelos/%s/): %s. %s' % (i['nome'], SITE, i['slug'], i['med'], i['pagina']['chamada']))
    a = L.index('## Artes prontas'); b = L.index('## Para quem')
    L = L[:a] + '\n'.join(linhas) + '\n\n' + L[b:]
    with open(lp, 'w', encoding='utf-8') as fh:
        fh.write(L)
print('%d página(s) de arte pronta' % n_pag)
