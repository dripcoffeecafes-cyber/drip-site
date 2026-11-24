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
    x = re.sub(r'href="(modelos|empresas|casamentos|eventos|fim-de-ano|consultorios-e-escritorios|sobre|contato|trocas-e-devolucoes|privacidade|condicoes-de-compra)/', r'href="../../\1/', x)
    return x.replace('class="logo" href="../../#"', 'class="logo" href="../../"').replace('class="logo" href="#"', 'class="logo" href="../../"')

topo, rodape, zap = rel(topo), rel(rodape), rel(zap)

# Galeria: artes da pasta "Arte ML" do Drive (geradas por drip-acervo/identidade/scripts/2026-11-15/ml_imagens.py e
# 2026-11-22/ml_capa_v6.py), convertidas para assets/img/ml/. Ficam fora a 05 e a 06, que falam do prazo de 24 h do Mercado Livre.
def ML(sl, alts):
    # A 07 ("O que vem no kit: 50 drips") saiu em 24/11: a venda passou a ser por unidade, a partir de 50
    return [('ml/%s-%s.webp' % (sl, n), 1, a) for n, a in zip(['01', '02', '03', '04', '07', '08'], alts) if n != '07']

# Fotos reais de clientes (Adriano, 22/11), em assets/img/real/ (recorte quadrado *-q.webp): entram logo depois da capa.
def MIX(ml, reais):
    return ml[:1] + [('real/%s-q.webp?v=3' % f, 1, a) for f, a in reais] + ml[1:]

M = {
 'kraft':  dict(sl='kraft-classico', n='Kraft Clássico', v='33', f=[[50,5.9],[100,5.8],[150,5.7],[200,5.6],[250,5.5],[300,5.4],[400,5.15],[500,4.9]], med='10 × 12 cm · impressão em preto',
   res='O drip clássico, em kraft natural, com a sua marca impressa em preto direto no sachê. O mais pedido para empresas e eventos.',
   fotos=MIX(ML('kraft-classico', ['Kraft Clássico com a sua marca', 'Diferenciais da Drip', 'Impressão em preto direto no kraft', 'Também temos a linha Premium', 'O que vem no kit', 'Marcas que já servem o Kraft Clássico']), [('floema', 'Drip Kraft Clássico da Floema Arquitetura'), ('binotto', 'Drip Kraft Clássico da Binotto & Zanette'), ('necta', 'Drip Kraft Clássico da Necta Negócios')]),
   ficha=[('Tamanho','10 × 12 cm'),('Material','Kraft natural'),('Impressão','Preto, 1 cor'),('Café','10 g · 80+ pontos SCA'),('Origem','Sul de Minas, Região Vulcânica'),('Produção','5 dias úteis após a arte')]),
 'kraftp': dict(sl='kraft-premium', n='Kraft Premium', v='281', f=[[50,6.9],[100,6.8],[150,6.7],[200,6.6],[250,6.5],[300,6.4],[400,6.15],[500,5.9]], med='10 × 15 cm · preto ou colorido',
   res='Formato maior, produzido só por nós, com 25% mais área para a sua arte que o drip tradicional. Em preto ou colorido, pelo mesmo preço.',
   fotos=MIX(ML('kraft-premium', ['Kraft Premium com a sua marca', 'Diferenciais da Drip', 'Impressão em preto ou colorida', 'Formato 10 x 15 cm exclusivo da Drip', 'O que vem no kit', 'Marcas que já servem o Kraft Premium']), [('dkj', 'Drip Kraft Premium da DKJ Psicologia'), ('matrikem', 'Drip Kraft Premium da MatriKem')]),
   ficha=[('Tamanho','10 × 15 cm'),('Material','Kraft premium'),('Impressão','Preto ou colorido'),('Café','10 g · 80+ pontos SCA'),('Origem','Sul de Minas, Região Vulcânica'),('Produção','5 dias úteis após a arte')]),
 'branco': dict(sl='branco-premium', n='Branco Premium', v='278', f=[[50,6.9],[100,6.8],[150,6.7],[200,6.6],[250,6.5],[300,6.4],[400,6.15],[500,5.9]], med='10 × 15 cm · preto ou colorido',
   res='O sachê branco no formato maior, para marcas que pedem um visual limpo. Em preto ou colorido, pelo mesmo preço.',
   fotos=ML('branco-premium', ['Branco Premium com a sua marca', 'Diferenciais da Drip', 'Impressão em preto ou colorida', 'Formato 10 x 15 cm exclusivo da Drip', 'O que vem no kit', 'Marcas que já servem o Branco Premium']),
   ficha=[('Tamanho','10 × 15 cm'),('Material','Branco premium'),('Impressão','Preto ou colorido'),('Café','10 g · 80+ pontos SCA'),('Origem','Sul de Minas, Região Vulcânica'),('Produção','5 dias úteis após a arte')]),
}

PARA_QUEM = {
 'kraft': ['Brinde para clientes e fornecedores', 'Brinde de fim de ano e de Natal para a equipe', 'Kit de boas-vindas, onboarding e endomarketing', 'Lembrancinha de casamento, formatura, aniversário e chá de bebê', 'Brinde de feira, congresso e evento corporativo'],
 'kraftp': ['Brinde corporativo para clientes, parceiros e fornecedores', 'Brinde de fim de ano e de Natal para a equipe', 'Kit de boas-vindas, onboarding e endomarketing', 'Lembrancinha de casamento, formatura, aniversário e chá de bebê', 'Brinde de feira, congresso e evento corporativo'],
 'branco': ['Lembrancinha de casamento, bodas, formatura, aniversário e chá de bebê', 'Brinde corporativo para clientes, parceiros e fornecedores', 'Brinde de fim de ano e de Natal para a equipe', 'Kit de boas-vindas, onboarding e endomarketing', 'Brinde de feira, congresso e evento corporativo'],
}
SACHE = {
 'kraft': ('O sachê kraft 10 × 12 cm', ['Impressão direta na embalagem, em 1 cor, preto sólido, sem etiqueta ou adesivo colado.', 'Pode levar logo, nome, frase ou data.', 'O fundo é sempre o próprio kraft: não fazemos fundo colorido nem foto ou arte cobrindo o sachê.', 'Quer impressão colorida ou mais espaço para a arte? Veja a linha Premium 10 × 15 cm, em kraft ou branco.']),
 'kraftp': ('O sachê kraft premium 10 × 15 cm', ['Papel mais liso e cantos arredondados.', '25% mais área para a sua arte que o drip tradicional de 10 × 12 cm. Formato produzido só pela Drip Coffee Label.', 'Impressão em preto sólido ou colorida, direto na embalagem, sem etiqueta colada. O preço é o mesmo.', 'A cor vai na logo, no nome, na frase ou na ilustração. O fundo é sempre o próprio kraft: sem fundo colorido nem foto cobrindo o sachê.']),
 'branco': ('O sachê branco premium 10 × 15 cm', ['Branco que dá contraste e nitidez à sua marca. É o modelo que indicamos para casamentos.', '25% mais área para a sua arte que o drip tradicional de 10 × 12 cm. Formato produzido só pela Drip Coffee Label.', 'Impressão em preto sólido ou colorida, direto na embalagem, sem etiqueta colada. O preço é o mesmo.', 'A cor vai na logo, no nome, na frase ou na ilustração. O fundo é sempre o próprio branco do sachê: sem fundo colorido nem foto cobrindo.']),
}
KIT = {'kraft': 'sachê kraft 10 × 12 cm', 'kraftp': 'sachê kraft premium 10 × 15 cm', 'branco': 'sachê branco premium 10 × 15 cm'}
COR_FAQ = {
 'kraft': 'Neste modelo a impressão é em preto, direto no kraft. Para impressão colorida, temos a linha Premium 10 × 15 cm, em kraft ou branco, com o mesmo café e pelo mesmo preço entre preto e colorido.',
 'kraftp': 'Você escolhe preto ou colorida, pelo mesmo preço, na aprovação da arte. A cor vai na sua logo e na sua arte; o fundo é sempre o próprio sachê.',
 'branco': 'Você escolhe preto ou colorida, pelo mesmo preço, na aprovação da arte. A cor vai na sua logo e na sua arte; o fundo é sempre o próprio sachê.',
}
def faq(k, d):
    q = [('A impressão pode ser colorida?', COR_FAQ[k]),
         ('Posso colocar uma foto ou um fundo colorido?', 'Não fazemos fundo colorido nem foto ou arte cobrindo o sachê. Imprimimos a sua logo, nome, frase ou data sobre o próprio sachê.'),
         ('Qual arquivo da logo devo enviar?', 'Em vetor: PDF vetorial, AI, EPS ou SVG, com os textos convertidos em curvas. É o arquivo original da sua marca, feito no Illustrator, CorelDRAW ou Canva. Foto, print ou imagem salva como PDF não servem. Você envia pelo WhatsApp depois da compra.'),
         ('Não tenho a logo em vetor. E agora?', 'Peça o arquivo original a quem criou a sua marca (designer ou gráfica). Ele costuma estar em PDF, AI ou CDR. Se não conseguir, ou se você não tem logo nem arte, criamos a arte do seu sachê sem custo. Fale com a gente pelo WhatsApp.'),
         ('Não tenho logo nem arte. Vocês criam?', 'Sim, sem custo. Criamos a arte do sachê com o nome, uma frase ou uma data que você escolher, e mandamos a prova digital para você aprovar, com 2 ajustes incluídos.'),
         ('Posso usar mais de uma arte?', 'Sim. Uma arte diferente a cada 50 sachês. Com 150 sachês, por exemplo, você pode ter três artes diferentes.'),
         ('Qual é o prazo?', 'Produzimos em 5 dias úteis depois da aprovação da arte. Em seguida vem o prazo da transportadora, calculado pelo CEP no carrinho.'),
         ('Qual é a validade do café?', '6 meses. O café é 100% arábica, torra média, moído na medida para o preparo em drip.'),
         ('Precisa de cafeteira?', 'Não. Abra o sachê, encaixe as abas na borda da xícara, despeje água quente aos poucos e aguarde coar.')]
    return ''.join('<details><summary>%s</summary><p>%s</p></details>' % x for x in q), q

SKU = {'kraft': '4001', 'kraftp': '5005', 'branco': '5001'}
CARD = {'kraft': 'p-kraft-cut.webp?v=3', 'kraftp': 'p-kraft-premium-cor-cut.webp?v=5', 'branco': 'p-branco-cor-cut.webp?v=5'}
brl = lambda v: ('R$ %.2f' % v).replace('.', ',')
OK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

CSS = '''<style>
.migalha{font-size:13px;color:var(--apoio);padding:22px 0 8px}.migalha a:hover{color:var(--cafe)}
.pp{display:grid;gap:28px;padding-bottom:64px}
@media(min-width:900px){.pp{grid-template-columns:1.05fr 1fr;gap:56px;align-items:start}.pp .gal{position:sticky;top:96px}}
.gal .pr{position:relative;background:#EDE6DC;border-radius:0;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.gal .pr img{max-height:84%;max-width:84%;width:auto;height:auto;object-fit:contain}
.gal .pr img.cena{max-width:100%;max-height:100%;width:100%;height:100%;object-fit:cover}
.gal .pr .tarja{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);background:var(--ink);color:#fff;font:700 11px/1 'Open Sans',sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:8px 14px;border-radius:4px;white-space:nowrap}
.gal .mi{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}
.gal .mi button{background:#EDE6DC;border-radius:0;aspect-ratio:1/1;border:2px solid transparent;cursor:pointer;padding:0;overflow:hidden;display:flex;align-items:center;justify-content:center}
.gal .mi button[aria-current="true"]{border-color:var(--ink)}
.gal .mi img{max-height:80%;width:auto}.gal .mi img.cena{max-height:none;width:100%;height:100%;object-fit:cover}
.info h1{font-size:clamp(40px,4.6vw,58px);line-height:1.08;margin:10px 0 6px}
.info .med{color:var(--apoio);font-size:15px}
.info .res{font-size:16.5px;margin:18px 0 22px}
.fx{border:1px solid var(--borda);border-radius:0;overflow:hidden;margin-bottom:16px}
.fx button{display:flex;justify-content:space-between;align-items:center;gap:10px;width:100%;padding:14px 18px;background:#fff;border:0;border-bottom:1px solid var(--fundo);font:300 15px 'Outfit',sans-serif;color:var(--texto);cursor:pointer;text-align:left}
.fx button:last-child{border-bottom:0}
.fx button b{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;color:var(--ink);font-size:23px}
.fx button small{display:inline-block;margin-left:8px;font-size:12px;font-weight:500;color:var(--cafe)}
.fx button[aria-pressed="true"]{background:var(--papel);box-shadow:inset 4px 0 0 var(--cafe)}
.linha-q{display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--papel);border-radius:0;padding:12px 16px}
.linha-q .tot{text-align:right;font-size:13px;color:var(--apoio)}.linha-q .tot b{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:32px;color:var(--ink)}
.info .btn{width:100%;margin-top:12px}
.gar{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:10px}
.gar li{display:flex;gap:10px;font-size:14.5px}
.gar svg{flex:0 0 20px;width:20px;height:20px;fill:none;stroke:var(--cafe);stroke-width:2;margin-top:1px}
.ficha{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--borda)}
@media(min-width:900px){.ficha{grid-template-columns:repeat(3,1fr)}}
.ficha div{padding:20px 16px 20px 0;border-bottom:1px solid var(--borda)}
.ficha span{display:block;font-size:11px;font-weight:400;letter-spacing:.16em;text-transform:uppercase;color:var(--apoio);margin-bottom:4px}
.ficha b{font-family:'Cormorant Garamond',Georgia,serif;font-weight:400;font-size:23px;color:var(--ink)}
.passos4{display:grid;gap:20px;counter-reset:p}
@media(min-width:900px){.passos4{grid-template-columns:repeat(4,1fr)}}
.passos4 div{background:#fff;border-radius:0;padding:22px}
.passos4 b{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-weight:400;font-size:44px;color:var(--cafe);line-height:1}
.passos4 h3{font-family:'Outfit',sans-serif;font-weight:500;letter-spacing:.14em;text-transform:uppercase;font-size:13px;margin:10px 0 6px}.passos4 p{font-size:14.5px;color:var(--apoio)}
.sobre2{display:grid;gap:34px}
@media(min-width:900px){.sobre2{grid-template-columns:1fr 1fr;gap:44px 64px}}
.sobre2 h3{font-size:26px;margin-bottom:12px}
.sobre2 p{font-size:15.5px}
.lst{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.lst li{position:relative;padding-left:20px;font-size:15.5px}
.lst li:before{content:"";position:absolute;left:0;top:.72em;width:8px;height:1px;background:var(--cafe)}
.outros{display:grid;gap:16px;max-width:760px;margin:0 auto}
@media(min-width:700px){.outros{grid-template-columns:1fr 1fr}}
</style>'''

for k, d in M.items():
    f0 = d['fotos'][0]
    tarja = ''
    mi = ''.join('<button type="button" aria-current="%s" data-src="../../assets/img/%s" data-cena="%d" data-alt="%s" aria-label="Foto %d"><img src="../../assets/img/%s" alt="" class="%s" width="120" height="120" loading="lazy"></button>'
                 % ('true' if i == 0 else 'false', f, c, a, i + 1, f, 'cena' if c else '') for i, (f, c, a) in enumerate(d['fotos']))
    # Faixas por quantidade (Adriano, 24/11): por unidade, mínimo 50, R$ 0,10 a menos a cada 50 até 300, R$ 0,25 de 300 a 400 e de 400 a 500 (Precificação 31)
    F = d['f']
    fx = ''.join('<button type="button" data-q="%d"><span>%s%s</span><b>%s</b></button>' % (
        F[j][0], ('%d a %d sachês' % (F[j][0], F[j + 1][0] - 1)) if j + 1 < len(F) else '%d sachês ou mais' % F[j][0],
        '' if j == 0 else ('<small>melhor preço</small>' if j == len(F) - 1 else '<small>desconto</small>'), brl(F[j][1])) for j in range(len(F)))
    cor = '' if k == 'kraft' else '<li>%s<span>Preto ou colorido pelo mesmo preço, escolhido na aprovação da arte. Colorido para logo ou texto, sem foto nem fundo cheio.</span></li>' % OK
    ficha = ''.join('<div><span>%s</span><b>%s</b></div>' % x for x in d['ficha'])
    outros = ''.join('''<a class="prod mini" href="../%s/"><div class="img"><img src="../../assets/img/%s" alt="Drip %s" loading="lazy"></div><div class="tx"><h3>%s</h3><p class="med">%s</p><p class="de">a partir de <b>%s</b>/sachê</p><span class="ver">Ver modelo</span></div></a>'''
                     % (d2['sl'], CARD[k2], d2['n'], d2['n'], d2['med'], brl(d2['f'][-1][1])) for k2, d2 in M.items() if k2 != k)
    url = 'https://driplabel.bloomingclub.com.br/modelos/%s/' % d['sl']
    desc = 'Drip coffee %s personalizado com a sua marca, café especial 80+ SCA. A partir de 50 sachês, de %s a %s por sachê. Arte sem custo.' % (d['n'], brl(d['f'][-1][1]), brl(d['f'][0][1]))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "@id": url + "#produto", "url": url, "sku": SKU[k], "name": "Drip " + d['n'] + " personalizado", "description": d['res'],
         "category": "Café especial personalizado", "material": d['ficha'][1][1],
         "image": ["https://driplabel.bloomingclub.com.br/assets/img/" + f[0].split('?')[0] for f in d['fotos']],
         "brand": {"@type": "Brand", "name": "Drip Coffee Label"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "BRL", "lowPrice": d['f'][-1][1], "highPrice": d['f'][0][1], "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition", "url": url, "offerCount": len(d['f']), "seller": {"@id": "https://driplabel.bloomingclub.com.br/#organization"}}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faq(k, d)[1]]},
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
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Drip Coffee Label">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Drip {d['n']} personalizado | Drip Coffee Label">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://driplabel.bloomingclub.com.br/assets/img/og/{d['sl']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="pt_BR">
<meta property="product:price:amount" content="{d['f'][-1][1]:.2f}">
<meta property="product:price:currency" content="BRL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Drip {d['n']} personalizado | Drip Coffee Label">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://driplabel.bloomingclub.com.br/assets/img/og/{d['sl']}.jpg">
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
  <nav class="migalha" aria-label="Você está em"><a href="../../">Início</a> / <a href="../">Modelos</a> / {d['n']}</nav>
  <div class="pp" data-modelo="{k}">
    <div class="gal">
      <div class="pr"><img id="foto" src="../../assets/img/{f0[0]}" alt="{f0[2]}" width="1100" height="1100" class="cena">{tarja}</div>
      <div class="mi">{mi}</div>
    </div>
    <div class="info">
      <span class="olho">Drip personalizado</span>
      <h1>{d['n']}</h1>
      <p class="med">{d['med']}</p>
      <p class="res">{d['res']}</p>
      <div class="fx" role="group" aria-label="Preço por quantidade">{fx}</div>
      <div class="linha-q">
        <div class="stepper"><button type="button" data-passo="-1" aria-label="Menos 10 sachês">−</button><output class="js-n tnum">50 sachês</output><button type="button" data-passo="1" aria-label="Mais 10 sachês">+</button></div>
        <div class="tot"><span class="js-un">{brl(d['f'][0][1])} por sachê</span><b class="js-tot tnum">{brl(d['f'][0][1]*50)}</b></div>
      </div>
      <a class="btn btn-cafe js-comprar" data-produto="{k}" href="#">Comprar</a>
      <a class="btn btn-linha js-zap" data-origem="pagina-{k}" href="#" target="_blank" rel="noopener">Falar com um especialista</a>
      <ul class="gar">
        <li>{OK}<span>Você manda a logo e nós montamos a arte, sem custo. Não tem logo nem arte? Criamos do zero, também sem custo. Nada é impresso antes do seu ok.</span></li>
        {cor}
        <li>{OK}<span>Uma arte diferente a cada 50 sachês.</span></li>
        <li>{OK}<span>Pronto em 5 dias úteis depois da aprovação. Frete calculado pelo CEP no carrinho.</span></li>
      </ul>
    </div>
  </div>
</main>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Sobre o produto</span><h2>Drip personalizado {d['n']}</h2></div>
    <div class="sobre2">
      <div><h3>Para quem é</h3><ul class="lst">{''.join('<li>%s</li>' % x for x in PARA_QUEM[k])}</ul></div>
      <div><h3>{SACHE[k][0]}</h3><ul class="lst">{''.join('<li>%s</li>' % x for x in SACHE[k][1])}</ul></div>
      <div><h3>O café</h3><ul class="lst"><li>Café especial com laudo: 80+ pontos SCA, avaliado por Q-Grader.</li><li>Origem única: Sul de Minas, Região Vulcânica.</li><li>100% arábica, torra média, moído na medida para o drip.</li><li>10 g por sachê. Validade de 6 meses.</li><li>Dosado, selado e conferido um a um, em pequenos lotes.</li></ul></div>
      <div><h3>O que vem no pedido</h3><ul class="lst"><li>Os drips personalizados em {KIT[k]}, na quantidade escolhida (a partir de 50, de 10 em 10), enviados em caixa.</li><li>Arte criada por nós, sem custo, mesmo para quem não tem logo, com prova digital e 2 ajustes incluídos.</li></ul><h3 style="margin-top:22px">Como preparar</h3><p>Abra o sachê, encaixe as abas na borda da xícara, despeje água quente aos poucos e aguarde coar. Retire o filtro e aproveite. Não precisa de cafeteira.</p></div>
    </div>
  </div>
</section>
<section class="sec cinza">
  <div class="wrap">
    <div class="cab"><span class="olho">Detalhes</span><h2>Ficha do produto</h2></div>
    <div class="ficha">{ficha}</div>
    <div class="cab" style="margin-top:56px"><span class="olho">Como funciona</span><h2>Do pedido à caixa em 4 passos</h2></div>
    <div class="passos4">
      <div><b>01</b><h3>Escolha e pague</h3><p>Quantidade aqui e pagamento na loja, com Pix, boleto ou cartão.</p></div>
      <div><b>02</b><h3>Envie a sua logo</h3><p>Em vetor (AI, EPS, SVG ou PDF), pelo WhatsApp. Sem logo? Criamos a arte sem custo.</p></div>
      <div><b>03</b><h3>Aprove a arte</h3><p>Mandamos a prova digital, com 2 ajustes incluídos.</p></div>
      <div><b>04</b><h3>Receba</h3><p>Produção em 5 dias úteis depois da aprovação, mais o prazo da entrega.</p></div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Dúvidas</span><h2>Antes de pedir o {d['n']}</h2></div>
    <div class="faq">{faq(k, d)[0]}</div>
  </div>
</section>
<section class="sec cinza">
  <div class="wrap">
    <div class="cab"><span class="olho">Outros modelos</span><h2>Compare com</h2></div>
    <div class="outros">{outros}</div>
  </div>
</section>
{rodape}
{zap}
<script>
(function(){{
  var M={json.dumps({k: dict(n=d['n'], f=d['f'], v=d['v'])}, ensure_ascii=False)}['{k}'];
  var UTM='utm_source=drip-landing&utm_medium=site&utm_campaign=brindes&utm_content=pagina-{k}';
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e quero falar com um especialista sobre o drip '+M.n+'.');
  var brl=function(v){{return v.toLocaleString('pt-BR',{{style:'currency',currency:'BRL'}})}};
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP}});
  // Quantidade em sachês: mínimo 50, de 10 em 10 (o carrinho trava no mínimo pelo campo Tamanho do produto)
  var c=document.querySelector('.pp'),MIN=50,PASSO=10,q=MIN,menos=c.querySelector('[data-passo="-1"]'),mais=c.querySelector('[data-passo="1"]'),fx=c.querySelectorAll('.fx button');
  function preco(n){{var p=M.f[0][1];M.f.forEach(function(x){{if(n>=x[0])p=x[1]}});return p}}
  function mostra(){{var u=preco(q);
    c.querySelector('.js-n').textContent=q+' sachês';c.querySelector('.js-un').textContent=brl(u)+' por sachê';c.querySelector('.js-tot').textContent=brl(u*q);
    menos.disabled=q<=MIN;mais.disabled=q>=5000;
    fx.forEach(function(b,j){{var de=M.f[j][0],ate=j+1<M.f.length?M.f[j+1][0]:1e9;b.setAttribute('aria-pressed',String(q>=de&&q<ate))}});
    c.querySelector('.js-comprar').href='https://www.bloomingclub.com.br/checkout/cart/item/add/'+M.v+'?quantity='+q+'&'+UTM}}
  c.addEventListener('click',function(e){{
    var b=e.target.closest('[data-passo]');if(b){{q=Math.max(MIN,Math.min(5000,q+(+b.dataset.passo)*PASSO));mostra();return}}
    var f=e.target.closest('.fx button');if(f){{q=+f.dataset.q;mostra();return}}
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
