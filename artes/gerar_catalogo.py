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
SACHE = {s['id']: s['nome'] for s in C['saches']}
LINHA = C['linhas']
esc = lambda s: html.escape(s or '', quote=True)
brl = lambda v: ('R$ %.2f' % v).replace('.', ',')
SITE = 'https://driplabel.bloomingclub.com.br/'

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

dest = [i for i in IT if i.get('destaque')][:4]
todos = ''
if len(IT) > len(dest):
    todos = '    <p class="ver-todos"><a class="btn btn-linha" href="modelos/">Ver todos os %d modelos</a></p>\n' % len(IT)
bloco = '    <div class="produtos minis%s">\n%s    </div>\n%s' % (' quatro' if len(dest) == 4 else '', ''.join(mini(i) for i in dest), todos)
t = '<span class="olho">Nossos produtos</span><h2>'
a = H.index(t, H.index('id="modelos"')) + len(t)
H = H[:a] + ('Três sachês, o mesmo café especial' if len(IT) <= 3 else 'Com a sua marca ou com arte pronta') + H[H.index('</h2>', a):]
a = H.index('<!-- CATALOGO:INICIO'); a = H.index('\n', a) + 1
b = H.index('    <!-- CATALOGO:FIM -->')
H = H[:a] + bloco + H[b:]
if '.ver-todos{' not in H:
    H = H.replace('</style>', '  /* Catálogo (gerar_catalogo.py) */\n  .ver-todos{text-align:center;margin:28px 0 0}.ver-todos .btn{min-width:260px}\n  @media (min-width:860px){.produtos.minis.quatro{grid-template-columns:repeat(4,1fr)}}\n</style>', 1)
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

def card(i):
    temas = ' '.join(i.get('temas', []))
    meta = esc(i['med']) if i['linha'] == 'sua-marca' else esc(' · '.join([TEMA.get(t, t) for t in i.get('temas', [])][:2]))
    selo = esc(i.get('selo') or ('Novo' if i.get('novo') else ''))
    url = i['url'].replace('modelos/', '', 1) if i['url'].startswith('modelos/') else '../' + i['url']
    return ('<a class="cc" href="%s" data-linha="%s" data-temas="%s" data-sache="%s" data-preco="%.2f" data-ordem="%d" data-novo="%d">'
            '<div class="cc-img">%s<img src="../assets/img/%s" alt="%s" width="%d" height="%d" loading="lazy">%s</div>'
            '<div class="cc-tx"><span class="cc-linha">%s</span><h3>%s</h3><p class="cc-med">%s</p>'
            '<p class="cc-de">a partir de<b class="tnum">%s<small> /sachê</small></b></p></div></a>') % (
        url, i['linha'], temas, i['sache'], i['preco_de'], i.get('ordem', 999), 1 if i.get('novo') else 0,
        '<span class="cc-selo">%s</span>' % selo if selo else '', i['img'], esc(i['alt']), i['w'], i['h'],
        '<span class="cc-tarja">%s</span>' % esc(i['tarja']) if i.get('tarja') else '',
        esc(LINHA[i['linha']]['nome']), esc(i['nome']), meta, brl(i['preco_de']))

usadas_l = [l for l in LINHA if any(i['linha'] == l for i in IT)]
usados_t = [t['id'] for t in C['temas'] if any(t['id'] in i.get('temas', []) for i in IT)]
usados_s = [s['id'] for s in C['saches'] if any(i['sache'] == s['id'] for i in IT)]
chip = lambda grupo, val, nome, n, on=False: '<button type="button" class="chip" data-f="%s" data-v="%s" aria-pressed="%s">%s<small>%d</small></button>' % (grupo, val, 'true' if on else 'false', esc(nome), n)
f_linha = chip('linha', '', 'Todos', len(IT), True) + ''.join(chip('linha', l, LINHA[l]['nome'], sum(i['linha'] == l for i in IT)) for l in usadas_l) if len(usadas_l) > 1 else ''
f_tema = ''.join(chip('tema', t, TEMA[t], sum(t in i.get('temas', []) for i in IT)) for t in usados_t)
f_sache = ''.join('<option value="%s">%s</option>' % (s, esc(SACHE[s])) for s in usados_s)
min_p = min(i['preco_de'] for i in IT)

ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Modelos de drip coffee personalizado", "url": SITE + 'modelos/',
      "mainEntity": {"@type": "ItemList", "numberOfItems": len(IT), "itemListElement": [
          {"@type": "ListItem", "position": n + 1, "name": i['nome'], "url": SITE + i['url']} for n, i in enumerate(IT)]}}
desc = 'Todos os modelos de drip coffee da Drip Coffee Label: com a sua marca ou com arte pronta, a partir de %s por sachê. Café especial 80+ pontos, pedido a partir de 50 unidades.' % brl(min_p)

CSS = '''<style>
.migalha{font-size:13px;color:var(--apoio);padding:22px 0 8px}.migalha a:hover{color:var(--cafe)}
.cat-cab{padding:8px 0 14px}.cat-cab h1{font-size:clamp(40px,5vw,60px);line-height:1.05;margin:8px 0 10px}.cat-cab p{max-width:620px;font-size:16px}
.filtros{position:sticky;top:64px;z-index:30;background:rgba(255,255,255,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-bottom:1px solid var(--fundo);margin:0 -20px;padding:10px 20px}
.fchips{display:flex;flex-wrap:nowrap;justify-content:flex-start;gap:8px;overflow-x:auto;scrollbar-width:none;padding:2px 0;margin:0 -20px;padding-left:20px;padding-right:20px}.fchips::-webkit-scrollbar{display:none}
.fchips .sep{flex:0 0 1px;background:var(--borda);margin:4px 4px}
@media(min-width:900px){.fchips{flex-wrap:wrap;margin:0;padding-left:0;padding-right:0}}
.chip{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 14px;border:1px solid var(--borda);background:#fff;color:var(--texto);font:400 13px/1 'Outfit',sans-serif;letter-spacing:.02em;cursor:pointer;border-radius:0;white-space:nowrap}
.chip small{font-size:11px;color:var(--apoio)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}.chip[aria-pressed="true"] small{color:#CFCBC6}
.barra{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;font-size:12.5px;color:var(--apoio)}
.barra .js-cont{white-space:nowrap}
.barra select{height:34px;border:1px solid var(--borda);background:#fff;font:400 12.5px 'Outfit',sans-serif;color:var(--texto);padding:0 6px;border-radius:0;min-width:0;max-width:48%}
.barra .sels{display:flex;gap:8px;justify-content:flex-end;flex:1}
.grade{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;padding:22px 0 64px}
@media(min-width:760px){.grade{grid-template-columns:repeat(3,1fr);gap:20px}}
@media(min-width:1100px){.grade{grid-template-columns:repeat(4,1fr)}}
.cc{display:flex;flex-direction:column;background:#fff;color:inherit;text-decoration:none;transition:box-shadow .2s}
.cc:hover{box-shadow:0 22px 50px -28px rgba(30,20,10,.35)}
.cc[hidden]{display:none}
.cc-img{position:relative;background:#EDE6DC;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.cc-img img{height:80%;width:auto;max-width:86%;object-fit:contain;transition:transform .6s}.cc:hover .cc-img img{transform:scale(1.05)}
.cc-selo{position:absolute;top:10px;left:10px;z-index:1;background:var(--ink);color:#fff;font:400 9.5px/1 'Outfit',sans-serif;letter-spacing:.18em;text-transform:uppercase;padding:6px 8px}
.cc-tarja{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:var(--ink);color:#fff;font:500 9.5px/1 'Outfit',sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:6px 9px;white-space:nowrap}
.cc-tx{padding:14px 14px 16px}
.cc-linha{display:block;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--apoio)}
.cc h3{font-size:22px;line-height:1.1;margin:6px 0 4px}
.cc-med{font-size:12.5px;color:var(--apoio);min-height:1.4em}
.cc-de{margin-top:8px;font-size:12px;color:var(--apoio)}.cc-de b{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:24px;color:var(--ink);white-space:nowrap;line-height:1.1}.cc-de b small{font:300 12px 'Outfit',sans-serif;color:var(--apoio)}
.cc{min-width:0}.cc h3{overflow-wrap:anywhere}
@media(min-width:760px){.cc-tx{padding:18px 18px 20px}.cc h3{font-size:26px}}
.vazio{grid-column:1/-1;text-align:center;padding:40px 0;color:var(--apoio)}.vazio button{background:none;border:0;color:var(--ink);text-decoration:underline;font:inherit;cursor:pointer}
.cat-nota{font-size:14px;color:var(--apoio);text-align:center;padding:0 0 56px}
</style>'''

pg = f'''<!DOCTYPE html>
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
  <nav class="migalha" aria-label="Você está em"><a href="../">Início</a> / Modelos</nav>
  <div class="cat-cab"><span class="olho">Nossos produtos</span><h1>Modelos</h1><p>Com a sua marca ou com arte pronta, sempre com o mesmo café especial. Pedido a partir de 50 sachês, desconto automático a partir de 150 e de 300.</p></div>
  <div class="filtros">
    <div class="fchips" role="group" aria-label="Filtrar modelos">{f_linha}{'<span class="sep" aria-hidden="true"></span>' if f_linha and f_tema else ''}{f_tema}</div>
    <div class="barra"><span class="js-cont">{len(IT)} modelos</span><span class="sels">
      {'<select class="js-sache" aria-label="Sachê"><option value="">Todos os sachês</option>' + f_sache + '</select>' if len(usados_s) > 1 else ''}
      <select class="js-ordem" aria-label="Ordenar"><option value="ordem">Destaques</option><option value="preco">Menor preço</option><option value="novo">Novidades</option></select></span></div>
  </div>
  <div class="grade">{''.join(card(i) for i in IT)}<p class="vazio" hidden>Nenhum modelo com esses filtros. <button type="button" class="js-limpa">Ver todos</button></p></div>
  <p class="cat-nota">Não achou o que procura? <a class="js-zap" data-origem="catalogo" href="#" target="_blank" rel="noopener">Fale com a gente</a> e criamos a arte com você, sem custo.</p>
</main>
{rodape}
{zap}
<script>
(function(){{
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e quero ajuda para escolher o modelo de drip.');
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP}});
  var g=document.querySelector('.grade'),cs=[].slice.call(g.querySelectorAll('.cc')),vz=g.querySelector('.vazio'),
      ss=document.querySelector('.js-sache'),so=document.querySelector('.js-ordem'),ct=document.querySelector('.js-cont'),
      F={{linha:'',tema:'',sache:'',ordem:'ordem'}};
  // Filtros na URL (?linha=pronta&tema=natal&sache=kraft-premium), para anúncios e links apontarem direto para um tema
  try{{var q=new URLSearchParams(location.search);['linha','tema','sache','ordem'].forEach(function(k){{if(q.get(k))F[k]=q.get(k)}})}}catch(e){{}}
  function aplica(){{
    var n=0;
    cs.forEach(function(c){{var ok=(!F.linha||c.dataset.linha===F.linha)&&(!F.tema||(' '+c.dataset.temas+' ').indexOf(' '+F.tema+' ')>=0)&&(!F.sache||c.dataset.sache===F.sache);c.hidden=!ok;if(ok)n++}});
    var k=F.ordem;cs.slice().sort(function(a,b){{return k==='preco'?a.dataset.preco-b.dataset.preco:k==='novo'?b.dataset.novo-a.dataset.novo||a.dataset.ordem-b.dataset.ordem:a.dataset.ordem-b.dataset.ordem}}).forEach(function(c){{g.insertBefore(c,vz)}});
    vz.hidden=n>0;ct.textContent=n+(n===1?' modelo':' modelos');
    document.querySelectorAll('.chip').forEach(function(b){{b.setAttribute('aria-pressed',String(F[b.dataset.f]===b.dataset.v))}});
    if(ss)ss.value=F.sache;so.value=F.ordem;
    var at=document.querySelector('.chip[data-f="tema"][aria-pressed="true"]')||document.querySelector('.chip[aria-pressed="true"]');if(at){{var fc=at.parentNode;fc.scrollLeft=at.offsetLeft-fc.offsetLeft-20}}
    try{{var u=new URLSearchParams();['linha','tema','sache'].forEach(function(k){{if(F[k])u.set(k,F[k])}});if(F.ordem!=='ordem')u.set('ordem',F.ordem);
      history.replaceState(null,'',location.pathname+(u.toString()?'?'+u:''))}}catch(e){{}}
  }}
  document.querySelector('.filtros').addEventListener('click',function(e){{var b=e.target.closest('.chip');if(!b)return;
    var f=b.dataset.f,v=b.dataset.v;if(f==='tema'){{F.tema=F.tema===v?'':v;if(F.tema)F.linha='pronta'}}else{{F.linha=v;F.tema=''}}aplica()}});
  if(ss)ss.addEventListener('change',function(){{F.sache=ss.value;aplica()}});
  so.addEventListener('change',function(){{F.ordem=so.value;aplica()}});
  vz.querySelector('.js-limpa').addEventListener('click',function(){{F={{linha:'',tema:'',sache:'',ordem:F.ordem}};aplica()}});
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
'''
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
