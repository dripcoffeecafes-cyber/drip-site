# Catálogo de modelos a partir de catalogo/modelos.json (fonte única):
#  1. modelos/index.html: página do catálogo, com filtros por linha, tema e sachê e ordenação;
#  2. index.html: os destaques entre <!-- CATALOGO:INICIO --> e <!-- CATALOGO:FIM --> e o botão "Ver todos";
#  3. sitemap.xml: a entrada /modelos/.
# Cabeçalho, estilos, Pixel, rodapé e WhatsApp saem do index. Rode depois de mexer no JSON ou no index:
#   python3 artes/gerar_catalogo.py            (site de verdade)
#   python3 artes/gerar_catalogo.py --exemplo  (só para prévia: junta catalogo/exemplo-artes-prontas.json; nunca publicar)
import json, os, re, sys, html
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(RAIZ, 'catalogo', 'modelos.json'), encoding='utf-8'))
if '--exemplo' in sys.argv:
    C['itens'] += json.load(open(os.path.join(RAIZ, 'catalogo', 'exemplo-artes-prontas.json'), encoding='utf-8'))
IT = sorted([i for i in C['itens'] if i.get('publicado', True)], key=lambda i: (i.get('ordem', 999), i['nome']))
TEMA = {t['id']: t['nome'] for t in C['temas']}
# Arte pronta entra sozinha na categoria "Artes prontas" (filtro e link ?tema=arte-pronta da inicial)
for _i in C['itens']:
    if _i.get('linha') == 'pronta' and 'arte-pronta' not in _i.get('temas', []):
        _i['temas'] = ['arte-pronta'] + _i.get('temas', [])
SACHE = {s['id']: s['nome'] for s in C['saches']}
LINHA = C['linhas']
esc = lambda s: html.escape(s or '', quote=True)
brl = lambda v: ('R$ %.2f' % v).replace('.', ',')
SITE = 'https://driplabel.bloomingclub.com.br/'

CARD_CSS = """.cc{display:flex;flex-direction:column;min-width:0;background:#fff;border:1px solid #E7E1D8;box-shadow:0 1px 2px rgba(30,20,10,.05),0 10px 24px -14px rgba(30,20,10,.28);transition:transform .25s,box-shadow .25s}
.cc:hover{transform:translateY(-3px);box-shadow:0 2px 4px rgba(30,20,10,.06),0 22px 40px -18px rgba(30,20,10,.38)}.cc[hidden]{display:none}
.cc-img{position:relative;background:#EDE6DC;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.cc-img img{height:80%;width:auto;max-width:86%;object-fit:contain;transition:transform .6s}.cc:hover .cc-img img{transform:scale(1.05)}
.cc-img img.cheia{width:100%;height:100%;max-width:none;object-fit:cover}
.cc-selos{position:absolute;top:8px;left:8px;z-index:1;display:flex;flex-direction:column;align-items:flex-start;gap:4px}
.cc-off{background:var(--cafe);color:#fff;font:500 10.5px/1 'Outfit',sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:6px 8px}
.cc-selo{background:var(--ink);color:#fff;font:400 9.5px/1 'Outfit',sans-serif;letter-spacing:.16em;text-transform:uppercase;padding:6px 8px}
.cc-tarja{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:var(--ink);color:#fff;font:500 9.5px/1 'Outfit',sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:6px 9px;white-space:nowrap}
.cc-tx{display:flex;flex-direction:column;flex:1;padding:14px 10px 12px;text-align:center;align-items:center}
.cc-qt{font-size:9.5px;letter-spacing:.08em;white-space:nowrap;text-transform:uppercase;color:var(--cafe)}
.cc h3{font-family:'Outfit',sans-serif!important;font-weight:500!important;font-size:13.5px;line-height:1.3;letter-spacing:.06em;text-transform:uppercase;margin:6px 0 2px;overflow-wrap:anywhere}.cc h3 a{color:var(--ink)}
.cc-med{font-size:12px;color:var(--apoio)}
.cc-de{margin-top:8px;font-size:12px;color:var(--apoio)}.cc-de span{display:block;white-space:nowrap;line-height:1.15}.cc-de b{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:24px;color:var(--ink);white-space:nowrap}
.cc-kit{font-size:11.5px;color:var(--apoio)}
.cc-bt{margin-top:auto;width:100%;height:42px;font-size:11px}.cc-kit{margin-bottom:12px}
.grade-ini{padding:0}
@media(min-width:760px){.grade-ini.tres{grid-template-columns:repeat(3,1fr)}}
@media(min-width:1100px){.grade-ini.tres{grid-template-columns:repeat(3,1fr);max-width:1000px;margin:0 auto}}"""

def KIT_TXT(i):
    # Arte pronta: vendida por unidade, a partir do mínimo do sachê (artes_prontas.min_sache); personalizado: a partir de 50 (por unidade)
    if i.get('kit'):
        return 'Kit com %d sachês' % i['kit']['saches']
    if i.get('linha') == 'pronta':
        return 'A partir de %d sachês' % C.get('artes_prontas', {}).get('min_sache', 20)
    return 'A partir de 50 sachês'

def card(i, ini=False):
    # Cartão de loja (referência: cafepds.com.br/personalizados): selo de desconto, nome, preço por sachê e Comprar
    off = round((1 - i['preco_de'] / i['preco_cheio']) * 100) if i.get('preco_cheio') else 0
    selo = esc(i.get('selo') or ('Novo' if i.get('novo') else ''))
    if ini: url, pre = i['url'], ''
    else: url, pre = (i['url'].replace('modelos/', '', 1) if i['url'].startswith('modelos/') else '../' + i['url']), '../'
    sub = esc(i['med']) if i.get('med') else esc(SACHE.get(i['sache'], ''))
    return ('<article class="cc" data-temas="%s" data-sache="%s" data-preco="%.2f" data-ordem="%d" data-novo="%d" data-nome="%s">'
            '<a class="cc-img" href="%s"><span class="cc-selos">%s%s</span><img src="%sassets/img/%s" alt="%s" width="%d" height="%d" loading="lazy"%s>%s</a>'
            '<div class="cc-tx"><p class="cc-qt">Comprando em quantidade</p><h3><a href="%s">%s</a></h3><p class="cc-med">%s</p>'
            '<p class="cc-de">a partir de<span><b class="tnum">%s</b><small> /sachê</small></span></p><p class="cc-kit">%s</p>'
            '<a class="btn btn-cafe cc-bt" href="%s">Comprar</a></div></article>') % (
        ' '.join(i.get('temas', [])), i['sache'], i['preco_de'], i.get('ordem', 999), 1 if i.get('novo') else 0, esc(i['nome'].lower()),
        url, '<span class="cc-off">Até %d%% off</span>' % off if off > 0 else '', '<span class="cc-selo">%s</span>' % selo if selo else '',
        pre, i['img'], esc(i['alt']), i['w'], i['h'], ' class="cheia"' if i.get('cheia') else '', '<span class="cc-tarja">%s</span>' % esc(i['tarja']) if i.get('tarja') else '',
        url, esc(i['nome']), sub, brl(i['preco_de']), esc(KIT_TXT(i)), url)


# ---------- 1. Inicial: destaques ----------
ip = os.path.join(RAIZ, 'index.html')
H = open(ip, encoding='utf-8').read()

def mini(i):
    # Mesmo cartão que a inicial já usa (.prod.mini), para os 3 de hoje ficarem idênticos.
    selo = '<span class="selo">%s</span>\n        ' % esc(i['selo']) if i.get('selo') else ''
    tarja = '<span class="tarja">%s</span>' % esc(i['tarja']) if i.get('tarja') else ''
    dm = {'kraft-classico': 'kraft', 'branco-premium': 'branco', 'kraft-premium': 'kraftp'}.get(i['slug'], i['slug'])
    return ('      <a class="prod mini" data-modelo="%s" href="%s">\n        %s<div class="img%s"><img src="assets/img/%s" alt="%s" width="%d" height="%d" loading="lazy">%s</div>\n'
            '        <div class="tx"><h3>%s</h3><p class="med">%s</p><p class="de">a partir de <b class="tnum">%s</b>/sachê</p><span class="ver">Ver modelo e preços</span></div>\n      </a>\n'
            ) % (dm, i['url'], selo, ' tem-tarja' if tarja else '', i['img'], esc(i['alt']), i['w'], i['h'], tarja, esc(i['nome']), esc(i['med']), brl(i['preco_de']))

dest = [i for i in IT if i.get('destaque') and i.get('linha') != 'pronta'][:4]
# Artes prontas na inicial (24/11): faixa própria logo abaixo dos personalizados, as mais novas primeiro, até 4
# A mais nova entra na grade principal (3 personalizados + 1 arte pronta = grade cheia no celular e no computador);
# as outras, até 4, numa faixa própria logo abaixo.
prontas = sorted([i for i in IT if i.get('linha') == 'pronta'], key=lambda i: (not i.get('novo'), i.get('ordem', 999)))
dest = dest[:3] + prontas[:1]
prontas = prontas[1:5]
todos = '    <p class="ver-todos"><a class="btn btn-linha" href="modelos/">Ver todos os modelos</a></p>\n'
bloco = '    <div class="grade grade-ini%s">\n%s\n    </div>\n' % (' tres' if len(dest) == 3 else '', '\n'.join('      ' + card(i, True) for i in dest))
if prontas:
    bloco += ('    <div class="cab cab-ap"><span class="olho">Artes prontas · a partir de %d sachês</span><h3>Escolha a arte, a gente envia</h3><p>Drip com arte da Drip Coffee Label, pronta para presentear: sem arquivo para mandar.</p></div>\n'
              '    <div class="grade grade-ini grade-ap">\n%s\n    </div>\n'
              '    <p class="ver-todos ver-ap"><a class="btn btn-linha" href="modelos/?tema=arte-pronta">Ver todas as artes prontas</a></p>\n') % (
        C.get('artes_prontas', {}).get('min_sache', 20), '\n'.join('      ' + card(i, True) for i in prontas))
bloco += todos
i0 = H.find('  /* Catálogo (gerar_catalogo.py) */')
if i0 >= 0: H = H[:i0] + H[H.index('/* fim catálogo */', i0) + len('/* fim catálogo */\n'):]
H = H.replace('</style>', '  /* Catálogo (gerar_catalogo.py) */\n.ver-todos{text-align:center;margin:28px 0 0}.ver-todos .btn{min-width:260px}\n.cab-ap{margin:40px 0 0}.cab-ap h3{font:500 clamp(26px,4vw,34px)/1.1 \'Cormorant Garamond\',Georgia,serif;margin:6px 0 8px}.grade-ap{padding-bottom:0}.ver-ap{margin-top:8px}\n.grade{display:grid;grid-template-columns:repeat(2,1fr);gap:22px 12px;padding:18px 0 64px}\n@media(min-width:760px){.grade{grid-template-columns:repeat(3,1fr);gap:36px 22px}}\n@media(min-width:1100px){.grade{grid-template-columns:repeat(4,1fr)}}\n' + CARD_CSS + '\n/* fim catálogo */\n</style>', 1)
a = H.index('<!-- CATALOGO:INICIO'); a = H.index('\n', a) + 1
b = H.index('    <!-- CATALOGO:FIM -->')
H = H[:a] + bloco + H[b:]
open(ip, 'w', encoding='utf-8').write(H)

# ---------- 2. Página do catálogo ----------
def entre(a, b):
    i = H.index(a); return H[i:H.index(b, i) + len(b)]
estilo = entre('<style>', '</style>')
pixel = entre('<!-- Meta Pixel -->', '</noscript>')
fontes = '\n'.join(l for l in H[:H.index('<style>')].splitlines() if 'fonts.g' in l)
topo = entre('<div class="aviso">', '</div>') + '\n' + entre('<header>', '</header>')
rodape = entre('<footer>', '</footer>')
zap = entre('<a class="zap-fixo', '</a>')
def rel(x):  # a página fica em /modelos/: um nível abaixo da raiz
    x = re.sub(r'(src|href)="assets/', r'\1="../assets/', x)
    x = re.sub(r'href="#([a-z]+)"', r'href="../#\1"', x)
    x = x.replace('href="modelos/"', 'href="./"')
    x = re.sub(r'href="(modelos|empresas|casamentos|eventos|fim-de-ano|consultorios-e-escritorios|sobre|contato|trocas-e-devolucoes|privacidade|condicoes-de-compra)/', r'href="../\1/', x)
    return x.replace('class="logo" href="../#"', 'class="logo" href="../"').replace('class="logo" href="#"', 'class="logo" href="../"')
topo, rodape, zap = rel(topo), rel(rodape), rel(zap)

usados_t = [t['id'] for t in C['temas'] if any(t['id'] in i.get('temas', []) for i in IT)]
usados_s = [s['id'] for s in C['saches'] if any(i['sache'] == s['id'] for i in IT)]
cat = '<button type="button" class="op" data-f="tema" data-v="" aria-pressed="true">Todos<small>%d</small></button>' % len(IT) + ''.join(
    '<button type="button" class="op" data-f="tema" data-v="%s" aria-pressed="false">%s<small>%d</small></button>' % (t, esc(TEMA[t]), sum(t in i.get('temas', []) for i in IT)) for t in usados_t)
sac = '<button type="button" class="op" data-f="sache" data-v="" aria-pressed="true">Todos os sachês</button>' + ''.join(
    '<button type="button" class="op" data-f="sache" data-v="%s" aria-pressed="false">%s</button>' % (s, esc(SACHE[s])) for s in usados_s)
min_p = min(i['preco_de'] for i in IT)

ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Modelos de drip coffee personalizado", "url": SITE + 'modelos/',
      "mainEntity": {"@type": "ItemList", "numberOfItems": len(IT), "itemListElement": [
          {"@type": "ListItem", "position": n + 1, "name": i['nome'], "url": SITE + i['url']} for n, i in enumerate(IT)]}}
desc = 'Todos os modelos de drip coffee da Drip Coffee Label: com a sua marca ou com arte pronta, para empresas, casamentos e eventos, a partir de %s por sachê. Café especial 80+ pontos, a partir de 50 sachês com a sua marca ou 20 com arte pronta.' % brl(min_p)

CSS = """<style>
.migalha{font-size:13px;color:var(--apoio);padding:22px 0 4px}.migalha a:hover{color:var(--cafe)}
.cat-cab{padding:4px 0 6px}.cat-cab h1{font-size:clamp(34px,4.6vw,52px);line-height:1.05;margin:4px 0 0;text-transform:uppercase;letter-spacing:.02em}
.ftop{position:sticky;top:64px;z-index:30;background:rgba(255,255,255,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid var(--fundo)}
.ftop .bf{display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 16px;border:1px solid var(--ink);background:#fff;color:var(--ink);font:500 12px/1 'Outfit',sans-serif;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}
.ftop .bf svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6}
.ftop .bf b{display:none;min-width:18px;height:18px;border-radius:9px;background:var(--ink);color:#fff;font:500 10px/18px 'Outfit';text-align:center;letter-spacing:0}.ftop .bf b.on{display:inline-block}
.ftop select{height:40px;border:1px solid var(--borda);background:#fff;font:400 13px 'Outfit',sans-serif;color:var(--texto);padding:0 8px;border-radius:0;margin-left:auto;max-width:52%}
.cont{font-size:13px;color:var(--apoio);padding:14px 0 0;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tag{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 10px;background:var(--fundo);border:0;font:400 12px 'Outfit',sans-serif;color:var(--ink);cursor:pointer}.tag:after{content:"×";font-size:15px}
.painel{position:fixed;inset:0;z-index:60;display:none}.painel.on{display:block}
.painel .fundo{position:absolute;inset:0;background:rgba(15,14,13,.45)}
.painel .cx{position:absolute;left:0;right:0;bottom:0;max-height:85vh;overflow:auto;background:#fff;padding:22px 20px calc(20px + env(safe-area-inset-bottom))}
@media(min-width:760px){.painel .cx{left:auto;top:0;bottom:0;width:380px;max-height:none}}
.painel h2{font-size:28px;margin:0 0 6px;display:flex;justify-content:space-between;align-items:center}.painel .x{background:none;border:0;font-size:28px;line-height:1;cursor:pointer;color:var(--ink)}
.painel h3{font:500 11px/1 'Outfit',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--apoio);margin:22px 0 10px}
.ops{display:grid;gap:0;border-top:1px solid var(--fundo)}
.op{display:flex;justify-content:space-between;align-items:center;width:100%;padding:13px 2px;background:none;border:0;border-bottom:1px solid var(--fundo);font:300 15px 'Outfit',sans-serif;color:var(--texto);cursor:pointer;text-align:left}
.op small{margin-left:8px;font-size:12px;color:var(--apoio)}.op[aria-pressed="true"]{font-weight:500;color:var(--ink)}.op[aria-pressed="true"]:before{content:"";order:2;width:8px;height:8px;background:var(--cafe);margin-left:auto;margin-right:10px}
.painel .ver{width:100%;margin-top:20px}
@media(min-width:760px){.cc-tx{padding:18px 16px 16px}.cc h3{font-size:14.5px}.cc-de b{font-size:27px}}
.vazio{grid-column:1/-1;text-align:center;padding:40px 0;color:var(--apoio)}.vazio button{background:none;border:0;color:var(--ink);text-decoration:underline;font:inherit;cursor:pointer}
.cat-nota{font-size:14px;color:var(--apoio);text-align:center;padding:0 0 56px}
</style>"""

FIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"/></svg>'
pg = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modelos de drip coffee personalizado | Drip Coffee Label</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}modelos/">
<meta property="og:type" content="website">
<meta property="og:title" content="Modelos de drip coffee personalizado | Drip Coffee Label">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}modelos/">
<meta property="og:image" content="{SITE}assets/img/og-drip-coffee-label.jpg">
<link rel="icon" href="../favicon.ico">
{fontes}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{estilo}
{CSS}
{pixel}
</head>
<body>
{topo}
<main class="wrap">
  <nav class="migalha" aria-label="Você está em"><a href="../">Início</a> › Modelos</nav>
  <div class="cat-cab"><h1 class="js-tit">Modelos</h1></div>
  <div class="ftop"><button type="button" class="bf js-abre">{FIL}Filtrar<b class="js-nf"></b></button>
    <select class="js-ordem" aria-label="Ordenar"><option value="ordem">Mais vendidos</option><option value="preco">Menores preços</option><option value="preco-">Maiores preços</option><option value="az">De A a Z</option><option value="novo">Novidades</option></select></div>
  <div class="cont"><span class="js-cont">Exibindo {len(IT)} produtos</span><span class="js-tags"></span></div>
  <div class="grade">{''.join(card(i) for i in IT)}<p class="vazio" hidden>Nenhum produto com esses filtros. <button type="button" class="js-limpa">Ver todos</button></p></div>
  <p class="cat-nota">Não achou o que procura? <a class="js-zap" data-origem="catalogo" href="#" target="_blank" rel="noopener">Fale com a gente</a> e criamos a arte com você, sem custo.</p>
</main>
<div class="painel" role="dialog" aria-modal="true" aria-label="Filtrar"><div class="fundo js-fecha"></div><div class="cx">
  <h2>Filtrar <button type="button" class="x js-fecha" aria-label="Fechar">×</button></h2>
  <h3>Categoria</h3><div class="ops">{cat}</div>
  {'<h3>Sachê</h3><div class="ops">' + sac + '</div>' if len(usados_s) > 1 else ''}
  <button type="button" class="btn btn-cafe ver js-fecha">Ver <span class="js-n">{len(IT)}</span> produtos</button>
</div></div>
{rodape}
{zap}
<script>
(function(){{
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e quero ajuda para escolher o modelo de drip.');
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP}});
  var TEMA={json.dumps(TEMA, ensure_ascii=False)},SACHE={json.dumps(SACHE, ensure_ascii=False)};
  var g=document.querySelector('.grade'),cs=[].slice.call(g.querySelectorAll('.cc')),vz=g.querySelector('.vazio'),
      so=document.querySelector('.js-ordem'),pn=document.querySelector('.painel'),F={{tema:'',sache:'',ordem:'ordem'}};
  // Filtros na URL (?tema=casamento&sache=branco-premium): anúncios e menus podem apontar direto para uma categoria
  try{{var q=new URLSearchParams(location.search);['tema','sache','ordem'].forEach(function(k){{if(q.get(k))F[k]=q.get(k)}})}}catch(e){{}}
  function aplica(){{
    var n=0;
    cs.forEach(function(c){{var ok=(!F.tema||(' '+c.dataset.temas+' ').indexOf(' '+F.tema+' ')>=0)&&(!F.sache||c.dataset.sache===F.sache);c.hidden=!ok;if(ok)n++}});
    var k=F.ordem;cs.slice().sort(function(a,b){{return k==='preco'?a.dataset.preco-b.dataset.preco:k==='preco-'?b.dataset.preco-a.dataset.preco:k==='az'?a.dataset.nome.localeCompare(b.dataset.nome):k==='novo'?b.dataset.novo-a.dataset.novo||a.dataset.ordem-b.dataset.ordem:a.dataset.ordem-b.dataset.ordem}}).forEach(function(c){{g.insertBefore(c,vz)}});
    vz.hidden=n>0;
    document.querySelector('.js-cont').textContent='Exibindo '+n+(n===1?' produto':' produtos');
    document.querySelector('.js-n').textContent=n;
    document.querySelector('.js-tit').textContent=F.tema?TEMA[F.tema]||'Modelos':'Modelos';
    var t='',nf=0;if(F.tema){{t+='<button type="button" class="tag" data-f="tema">'+TEMA[F.tema]+'</button>';nf++}}
    if(F.sache){{t+='<button type="button" class="tag" data-f="sache">'+SACHE[F.sache]+'</button>';nf++}}
    document.querySelector('.js-tags').innerHTML=t;var b=document.querySelector('.js-nf');b.textContent=nf;b.className='js-nf'+(nf?' on':'');
    document.querySelectorAll('.op').forEach(function(o){{o.setAttribute('aria-pressed',String(F[o.dataset.f]===o.dataset.v))}});
    so.value=F.ordem;
    try{{var u=new URLSearchParams();['tema','sache'].forEach(function(k){{if(F[k])u.set(k,F[k])}});if(F.ordem!=='ordem')u.set('ordem',F.ordem);
      history.replaceState(null,'',location.pathname+(u.toString()?'?'+u:''))}}catch(e){{}}
  }}
  document.querySelector('.js-abre').addEventListener('click',function(){{pn.classList.add('on')}});
  pn.addEventListener('click',function(e){{var o=e.target.closest('.op');if(o){{F[o.dataset.f]=o.dataset.v;aplica();return}}
    if(e.target.closest('.js-fecha'))pn.classList.remove('on')}});
  document.querySelector('.js-tags').addEventListener('click',function(e){{var t=e.target.closest('.tag');if(t){{F[t.dataset.f]='';aplica()}}}});
  so.addEventListener('change',function(){{F.ordem=so.value;aplica()}});
  vz.querySelector('.js-limpa').addEventListener('click',function(){{F.tema='';F.sache='';aplica()}});
  aplica();
  // Pixel: ver o catálogo já é ver os produtos (regra do Lead Drip de 18/11)
  try{{sessionStorage.setItem('drip_viu','1')}}catch(x){{}}
  try{{if(window.fbq)fbq('track','ViewContent',{{content_type:'product_group',content_name:'catalogo'}})}}catch(e){{}}
  document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a.js-zap');if(!a)return;
    try{{if(!window.fbq)return;fbq('track','Contact',{{content_name:'catalogo'}});
      if(!sessionStorage.getItem('drip_lead')){{fbq('trackSingle','29552796950978987','Lead',{{content_name:'whatsapp-catalogo'}});sessionStorage.setItem('drip_lead','1')}}}}catch(x){{}}}},true);
}})();
</script>
</body>
</html>
"""
os.makedirs(os.path.join(RAIZ, 'modelos'), exist_ok=True)
open(os.path.join(RAIZ, 'modelos', 'index.html'), 'w', encoding='utf-8').write(pg)

# ---------- 3. Sitemap ----------
sp = os.path.join(RAIZ, 'sitemap.xml')
S = open(sp, encoding='utf-8').read()
if '<loc>%smodelos/</loc>' % SITE not in S:
    S = S.replace('  <url>\n    <loc>%smodelos/kraft-classico/</loc>' % SITE,
                  '  <url>\n    <loc>%smodelos/</loc>\n    <lastmod>2026-11-23</lastmod>\n  </url>\n  <url>\n    <loc>%smodelos/kraft-classico/</loc>' % (SITE, SITE), 1)
    open(sp, 'w', encoding='utf-8').write(S)
print('catálogo: %d modelos (%d na inicial)' % (len(IT), len(dest)))
