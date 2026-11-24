# Gera as páginas por ocasião (empresas, casamentos, eventos, fim-de-ano, consultorios-e-escritorios)
# a partir do index.html: estilos, Pixel, cabeçalho e rodapé saem de lá. Rode depois de mudar o index:
#   python3 artes/gerar_paginas_ocasiao.py
import json, os, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
B = 'https://driplabel.bloomingclub.com.br/'


def entre(a, b):
    i = H.index(a); return H[i:H.index(b, i) + len(b)]


estilo = entre('<style>', '</style>')
pixel = entre('<!-- Meta Pixel -->', '</noscript>')
fontes = '\n'.join(l for l in H[:H.index('<style>')].splitlines() if 'fonts.g' in l)
topo = entre('<div class="aviso">', '</div>') + '\n' + entre('<header>', '</header>')
rodape = entre('<footer>', '</footer>')
zap = entre('<a class="zap-fixo', '</a>')


def rel(x):
    x = re.sub(r'(src|href)="assets/', r'\1="../assets/', x)
    x = re.sub(r'href="#([a-z]+)"', r'href="../#\1"', x)
    x = re.sub(r'href="(modelos|empresas|casamentos|eventos|fim-de-ano|consultorios-e-escritorios|sobre|contato|trocas-e-devolucoes|privacidade|condicoes-de-compra)/', r'href="../\1/', x)
    return x.replace('class="logo" href="#"', 'class="logo" href="../"')


topo, rodape, zap = rel(topo), rel(rodape), rel(zap)

MODELOS = [('kraft-classico', 'Kraft Clássico', '10 × 12 cm · impressão em preto', 'p-kraft-cut.webp?v=3', 'R$ 4,90'),
           ('kraft-premium', 'Kraft Premium', '10 × 15 cm · preto ou colorido', 'p-kraft-premium-cor-cut.webp?v=5', 'R$ 5,90'),
           ('branco-premium', 'Branco Premium', '10 × 15 cm · preto ou colorido', 'p-branco-cor-cut.webp?v=5', 'R$ 5,90')]

COMUM = [
    ('Qual é o pedido mínimo?', '50 sachês. Acima disso, a quantidade que você quiser, de 10 em 10, e o preço por sachê cai a cada 50 sachês até 300, e de novo em 400 e 500.'),
    ('Vocês criam a arte?', 'Sim, sem custo, inclusive para quem não tem logo. Mandamos a prova digital com 2 ajustes incluídos e só produzimos depois da sua aprovação.'),
    ('Qual é o prazo?', 'Produzimos em 5 dias úteis depois da aprovação da arte. Depois vem o prazo da transportadora, calculado pelo CEP no carrinho.'),
]

P = {
 'empresas': dict(
   nome='Empresas', titulo='Brinde corporativo de café com a sua marca | Drip Coffee Label',
   desc='Drip coffee personalizado como brinde corporativo: para clientes, equipe, onboarding e endomarketing. Café especial 80+ SCA, a partir de 50 sachês.',
   olho='Brinde corporativo', h1='O brinde que a sua equipe e os seus clientes usam de verdade.',
   intro='Drip coffee com a logo da empresa impressa direto no sachê e café especial de origem única dentro. Para presentear clientes, receber quem chega e marcar presença na rotina, sem ir para a gaveta.',
   foto='real/matrikem-v.webp', alt='Drip personalizado da MatriKem sobre a mesa',
   usos=[('Clientes e parceiros', 'Vai junto da proposta, da entrega ou da visita e fica na mesa de quem recebe.'),
         ('Onboarding e boas-vindas', 'Um café com a marca no primeiro dia, no kit de boas-vindas ou na mesa do novo colaborador.'),
         ('Endomarketing', 'Datas internas, metas batidas, SIPAT, aniversário da empresa. Uma arte diferente a cada 50 sachês.'),
         ('Recepção e reuniões', 'O café da sala de espera e das reuniões, já com a sua marca.')],
   modelo='Para a maioria das empresas, o Kraft Clássico resolve. Se a logo tem cor ou você quer mais espaço para a arte, vá de Kraft Premium.',
   fotos=[('real/matrikem.webp', 'MatriKem'), ('real/necta.webp', 'Necta Negócios'), ('real/binotto.webp', 'Binotto & Zanette')],
   faq=[('Dá para ter uma arte por setor ou filial?', 'Sim. Uma arte diferente a cada 50 sachês. Com 150 sachês, por exemplo, você pode ter três artes diferentes.'),
        ('A impressão pode ser colorida?', 'Nos modelos Premium (Kraft e Branco), sim, pelo mesmo preço, para logo ou texto, sem foto nem fundo cheio. O Kraft Clássico é impresso em preto.'),
        ('Que arquivo da logo eu mando?', 'Em vetor: AI, EPS, SVG ou PDF vetorial, pelo WhatsApp depois da compra. Não tem a logo em vetor ou não tem logo? Criamos a arte sem custo.')] + COMUM),
 'casamentos': dict(
   nome='Casamentos', titulo='Lembrancinha de casamento: drip coffee personalizado | Drip Coffee Label',
   desc='Lembrancinha de casamento em drip coffee com o nome do casal: café especial 80+ SCA para o café da manhã seguinte. Arte sem custo, a partir de 50 sachês.',
   olho='Lembrancinha de casamento', h1='O café da manhã seguinte, com o nome de vocês.',
   intro='Drip coffee com o nome do casal, a data ou uma frase impressos no sachê e café especial dentro. Uma lembrancinha útil, bonita na mesa e que o convidado usa no dia seguinte.',
   foto='evento.webp', alt='Drip personalizado de casamento numa mesa decorada com flores',
   usos=[('Lembrancinha dos convidados', 'Na mesa, na saída da festa ou no kit do hotel.'),
         ('Café da manhã pós-festa', 'Para o dia seguinte começar com um café especial e a lembrança de vocês.'),
         ('Padrinhos e madrinhas', 'Junto do convite ou do kit de padrinhos, com uma frase só para eles.'),
         ('Chá de casa nova e bodas', 'Também para chá de panela, noivado, bodas e aniversário de casamento.')],
   modelo='Para casamentos, indicamos o Branco Premium: o branco dá contraste ao nome do casal e aceita impressão colorida pelo mesmo preço.',
   fotos=[('real/elenir.webp', 'Sachê de agradecimento'), ('real/dkj.webp', 'Arte com assinatura'), ('real/floema.webp', 'Arte com frase')],
   faq=[('O que vai impresso no sachê?', 'O nome do casal, a data, uma frase ou um monograma. Criamos a arte sem custo, com prova digital e 2 ajustes incluídos.'),
        ('Qual modelo vocês indicam para casamento?', 'O Branco Premium, de 10 × 15 cm: tem mais área para a arte e aceita impressão em preto ou colorida pelo mesmo preço.'),
        ('Com quanto tempo de antecedência devo pedir?', 'O ideal é pedir com folga: a arte é validada em até 48 horas e a produção leva 5 dias úteis depois da aprovação, mais o frete. Com a data do casamento, fale com a gente pelo WhatsApp.'),
        ('Dá para ter fundo colorido ou foto do casal?', 'Não. A impressão é sobre o próprio sachê: nome, data, frase ou desenho, sem foto nem fundo cheio.')] + COMUM),
 'eventos': dict(
   nome='Eventos', titulo='Brinde para eventos, feiras e congressos: drip personalizado | Drip Coffee Label',
   desc='Drip coffee personalizado para feiras, congressos e eventos corporativos. Leve, cabe na sacola e é aberto na hora. Café especial 80+ SCA, a partir de 50.',
   olho='Feiras e eventos', h1='O brinde do estande que é aberto na hora.',
   intro='Leve, cabe em qualquer sacola e não ocupa espaço na mala. O drip com a sua marca vira o café do visitante no estande, no hotel ou na volta para casa.',
   foto='o4.webp', alt='Drips personalizados em sacolas de evento',
   usos=[('Feiras e estandes', 'Para distribuir no estande e puxar conversa com quem passa.'),
         ('Congressos e palestras', 'No kit do participante, na pasta ou na sacola do evento.'),
         ('Convenções e lançamentos', 'Para equipes de vendas, parceiros e convidados.'),
         ('Kits de hotel e viagem', 'No quarto do hotel ou no kit de quem vem de fora.')],
   modelo='Para volume e distribuição rápida, o Kraft Clássico tem o menor preço por sachê. Para destacar a marca no estande, o Kraft Premium tem 25% mais área para a arte.',
   fotos=[('o4.webp', 'Sacolas de evento'), ('o5.webp', 'Mesa de evento'), ('real/onofre.webp', 'Leonardo Onofre Advocacia')],
   faq=[('Dá para fazer uma arte por dia de evento ou por patrocinador?', 'Sim. Uma arte diferente a cada 50 sachês.'),
        ('Vocês entregam no local do evento?', 'Enviamos para todo o Brasil, para o endereço que você informar no pedido. O frete e o prazo da transportadora aparecem no carrinho, pelo CEP.'),
        ('Tenho data marcada. Como faço?', 'Fale com a gente pelo WhatsApp com a data e o CEP, e conferimos se o prazo cabe antes de você pagar.'),
        ('Acima de 1.000 sachês tem condição diferente?', 'Para mais de 1.000 sachês, fale com a gente pelo WhatsApp.')] + COMUM),
 'fim-de-ano': dict(
   nome='Fim de ano', titulo='Brinde de fim de ano e Natal para empresas: drip personalizado | Drip Coffee Label',
   desc='Brinde de fim de ano e de Natal para clientes e equipe: drip coffee com a sua marca e café especial 80+ SCA. Arte sem custo, a partir de 50 sachês.',
   olho='Fim de ano e Natal', h1='Um café para agradecer o ano.',
   intro='O presente de fim de ano para clientes, parceiros e equipe: drip coffee com a sua marca e uma mensagem de agradecimento, com café especial de origem única dentro.',
   foto='real/elenir-v.webp', alt='Drip personalizado com mensagem de agradecimento de fim de ano',
   usos=[('Clientes e parceiros', 'Com uma mensagem de agradecimento e votos para o próximo ano.'),
         ('Equipe', 'Na confraternização, no amigo secreto ou no kit de fim de ano.'),
         ('Cestas e kits de Natal', 'Junto de chocolates, panetone ou cartão.'),
         ('Mensagem própria', 'Uma mensagem diferente a cada 50 sachês.')],
   modelo='Para mensagens mais longas ou com cor, o Kraft Premium e o Branco Premium têm 25% mais área. Para volume, o Kraft Clássico tem o menor preço.',
   fotos=[('real/elenir.webp', 'Mensagem de agradecimento'), ('o8.webp', 'Kit de fim de ano'), ('real/necta.webp', 'Necta Negócios')],
   faq=[('Até quando pedir para receber antes do Natal?', 'Em 2026, peça até 27/11 para receber a tempo das confraternizações e do Natal. Depois disso, fale com a gente pelo WhatsApp com a data e o CEP.'),
        ('Posso colocar uma mensagem de fim de ano?', 'Sim. Criamos a arte com a sua marca e a mensagem, sem custo, com prova digital e 2 ajustes incluídos.'),
        ('Dá para colocar o drip em uma cesta ou kit?', 'Sim. O sachê é leve e individual e combina com cestas, caixas e kits.')] + COMUM),
 'consultorios-e-escritorios': dict(
   nome='Consultórios e escritórios', titulo='Brinde para pacientes e clientes: café para consultório e escritório | Drip Coffee Label',
   desc='Drip coffee personalizado para clínicas, consultórios e escritórios: o café da recepção e o brinde para pacientes e clientes, com a sua marca. A partir de 50.',
   olho='Consultórios, clínicas e escritórios', h1='O cafezinho da sua recepção, com a sua marca.',
   intro='Para psicólogos, dentistas, médicos, advogados, contadores e arquitetos: o café que o paciente ou o cliente toma na espera e leva para casa, com a sua marca impressa no sachê.',
   foto='real/dkj-v.webp', alt='Drip personalizado de consultório de psicologia',
   usos=[('Sala de espera', 'Um café especial em sachê individual, prático e sem cafeteira.'),
         ('Brinde para pacientes e clientes', 'Na primeira consulta, na alta, no fechamento de contrato ou no aniversário.'),
         ('Datas da profissão', 'Dia do Psicólogo, do Dentista, do Advogado: uma lembrança com a sua marca.'),
         ('Pequenas quantidades', 'Pedido a partir de 50 sachês, e a arte fica por nossa conta.')],
   modelo='Para logos com cor ou assinaturas finas, o Kraft Premium dá mais área e aceita impressão colorida. Para um visual simples, o Kraft Clássico em preto.',
   fotos=[('real/dkj.webp', 'DKJ Psicologia Clínica'), ('real/binotto.webp', 'Binotto & Zanette Odontologia'), ('real/onofre.webp', 'Leonardo Onofre Advocacia')],
   faq=[('Dá para pedir só 50 sachês?', 'Sim. O pedido mínimo é de 50 sachês, e a arte é criada sem custo.'),
        ('Precisa de cafeteira?', 'Não. Abra o sachê, encaixe as abas na borda da xícara, despeje água quente aos poucos e aguarde coar.'),
        ('Qual é a validade do café?', '6 meses. O café é 100% arábica, torra média, 10 g por sachê.')] + COMUM),
}

CSS = '''<style>
.usos4{display:grid;gap:16px}@media(min-width:800px){.usos4{grid-template-columns:1fr 1fr}}
.usos4 div{background:#fff;border:1px solid var(--borda);padding:22px 24px}
.usos4 h3{font-size:24px;margin-bottom:6px}.usos4 p{color:var(--apoio);font-size:15.5px}
.nota-modelo{max-width:760px;margin:26px auto 0;text-align:center;color:var(--apoio)}
.fotos3{display:grid;gap:14px;grid-template-columns:repeat(3,1fr)}@media(max-width:700px){.fotos3{grid-template-columns:1fr 1fr}.fotos3 figure:last-child{display:none}}
.fotos3 figure{margin:0}.fotos3 img{display:block;width:100%;aspect-ratio:9/14;object-fit:cover;background:#EDE6DC}
.fotos3 figcaption{margin-top:8px;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--apoio)}
.passos4{display:grid;gap:20px}@media(min-width:900px){.passos4{grid-template-columns:repeat(4,1fr)}}
.passos4 div{background:#fff;padding:22px}
.passos4 b{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-weight:400;font-size:44px;color:var(--cafe);line-height:1}
.passos4 h3{font-family:'Outfit',sans-serif;font-weight:500;letter-spacing:.14em;text-transform:uppercase;font-size:13px;margin:10px 0 6px}.passos4 p{font-size:14.5px;color:var(--apoio)}
.migalha{font-size:13px;color:var(--apoio);padding:16px 0 0}.migalha a:hover{color:var(--cafe)}
.outras{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.outras a{border:1px solid var(--borda);padding:10px 16px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
.outras a:hover{border-color:var(--ink)}
.capa h1{font-size:clamp(38px,4.2vw,58px);max-width:11em}
@media(max-width:899px){.capa-foto::after{background:linear-gradient(180deg,rgba(23,22,20,.95) 0%,rgba(23,22,20,.86) 50%,rgba(23,22,20,.25) 76%,rgba(23,22,20,0) 100%)!important}}
</style>'''

for sl, d in P.items():
    url = B + sl + '/'
    cards = ''.join('''<a class="prod mini" href="../modelos/%s/"><div class="img"><img src="../assets/img/%s" alt="Drip %s" width="416" height="605" loading="lazy"></div><div class="tx"><h3>%s</h3><p class="med">%s</p><p class="de">a partir de <b class="tnum">%s</b>/sachê</p><span class="ver">Ver modelo e preços</span></div></a>''' % m[:1] + (m[3], m[1], m[1], m[2], m[4]) if False else
                    '<a class="prod mini" href="../modelos/%s/"><div class="img"><img src="../assets/img/%s" alt="Drip %s" width="416" height="605" loading="lazy"></div><div class="tx"><h3>%s</h3><p class="med">%s</p><p class="de">a partir de <b class="tnum">%s</b>/sachê</p><span class="ver">Ver modelo e preços</span></div></a>' % (m[0], m[3], m[1], m[1], m[2], m[4]) for m in MODELOS)
    usos = ''.join('<div><h3>%s</h3><p>%s</p></div>' % u for u in d['usos'])
    fotos = ''.join('<figure><img src="../assets/img/%s" alt="Drip personalizado: %s" width="720" height="1279" loading="lazy"><figcaption>%s</figcaption></figure>' % (f, c, c) for f, c in d['fotos'])
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % q for q in d['faq'])
    outras = ''.join('<a href="../%s/">%s</a>' % (s2, d2['nome']) for s2, d2 in P.items() if s2 != sl)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": d['titulo'], "description": d['desc'], "inLanguage": "pt-BR",
         "isPartOf": {"@id": B + "#website"}, "about": {"@id": B + "#organization"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": B + "assets/img/" + d['foto']}},
        {"@type": "ItemList", "name": "Modelos de drip coffee personalizado", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": "Drip " + m[1] + " personalizado", "url": B + "modelos/" + m[0] + "/"} for i, m in enumerate(MODELOS)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in d['faq']]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": B},
            {"@type": "ListItem", "position": 2, "name": d['nome'], "item": url}]}]}
    pg = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{d['titulo']}</title>
<meta name="description" content="{d['desc']}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Drip Coffee Label">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{d['titulo']}">
<meta property="og:description" content="{d['desc']}">
<meta property="og:image" content="{B}assets/img/og-drip-coffee-label.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.ico">
<link rel="preload" as="image" href="../assets/img/{d['foto']}" fetchpriority="high">
{fontes}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{estilo}
{CSS}
{pixel}
</head>
<body>
{topo}
<section class="capa">
  <div class="capa-txt">
    <span class="olho" style="color:#C9A36A">{d['olho']}</span>
    <h1 style="margin-top:12px">{d['h1']}</h1>
    <p class="sub">{d['intro']}</p>
    <div class="ctas"><a class="btn btn-branco" href="#modelos">Ver modelos e preços</a></div>
  </div>
  <figure class="capa-foto"><img src="../assets/img/{d['foto']}" alt="{d['alt']}" width="900" height="1125" fetchpriority="high"></figure>
</section>
<div class="wrap"><nav class="migalha" aria-label="Você está em"><a href="../">Início</a> / {d['nome']}</nav></div>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Como usar</span><h2>Onde o drip com a sua marca entra</h2></div>
    <div class="usos4">{usos}</div>
  </div>
</section>
<section class="sec cinza" id="modelos">
  <div class="wrap">
    <div class="cab"><span class="olho">Modelos</span><h2>Escolha o sachê</h2><p>Todos com café especial de origem única, 80+ pontos SCA, Região Vulcânica (Sul de Minas). A partir de 50 sachês.</p></div>
    <div class="produtos minis">{cards}</div>
    <p class="nota-modelo">{d['modelo']}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cab"><span class="olho">Feitos por nós</span><h2>Drips de verdade</h2></div>
    <div class="fotos3">{fotos}</div>
  </div>
</section>
<section class="sec cinza">
  <div class="wrap">
    <div class="cab"><span class="olho">Como funciona</span><h2>Do pedido à caixa em 4 passos</h2></div>
    <div class="passos4">
      <div><b>01</b><h3>Escolha e pague</h3><p>Modelo e quantidade no site, com Pix, boleto ou cartão.</p></div>
      <div><b>02</b><h3>Envie a sua logo</h3><p>Em vetor, pelo WhatsApp. Sem logo? Criamos a arte sem custo.</p></div>
      <div><b>03</b><h3>Aprove a arte</h3><p>Mandamos a prova digital, com 2 ajustes incluídos.</p></div>
      <div><b>04</b><h3>Receba</h3><p>Produção em 5 dias úteis depois da aprovação, mais o prazo da entrega.</p></div>
    </div>
  </div>
</section>
<section class="sec" id="duvidas">
  <div class="wrap">
    <div class="cab"><span class="olho">Dúvidas</span><h2>Antes de pedir</h2></div>
    <div class="faq">{faq}</div>
    <p style="text-align:center;margin-top:30px"><a class="btn btn-linha js-zap" data-origem="ocasiao-{sl}" href="#" target="_blank" rel="noopener">Falar com um especialista</a></p>
  </div>
</section>
<section class="sec cinza" style="padding-top:56px;padding-bottom:56px">
  <div class="wrap"><div class="cab" style="margin-bottom:22px"><span class="olho">Outras ocasiões</span></div><div class="outras">{outras}</div></div>
</section>
{rodape}
{zap}
<script>
(function(){{
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label (página {d['nome']}) e quero saber mais sobre o drip personalizado.');
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP;a.target='_blank';a.rel='noopener'}});
  var PX_NUVEM='29552796950978987';
  function ev(n,x){{try{{if(window.fbq)fbq('track',n,x||{{}})}}catch(e){{}}}}
  var leadFeito=false;
  function lead(nome){{try{{if(leadFeito)return;try{{if(sessionStorage.getItem('drip_lead')){{leadFeito=true;return}}}}catch(x){{}}
    if(!window.fbq)return;fbq('trackSingle',PX_NUVEM,'Lead',{{content_name:nome}});leadFeito=true;try{{sessionStorage.setItem('drip_lead','1')}}catch(x){{}}}}catch(e){{}}}}
  var viu=false,p1=document.querySelector('.prod');
  try{{if(sessionStorage.getItem('drip_viu'))viu=true}}catch(x){{}}
  if(!viu&&p1&&'IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{viu=true;try{{sessionStorage.setItem('drip_viu','1')}}catch(x){{}};io.disconnect()}}}})}},{{threshold:.5}});io.observe(p1)}}
  document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a');if(!a)return;
    if(a.classList.contains('js-zap')){{var o=a.getAttribute('data-origem')||'whatsapp';ev('Contact',{{content_name:o}});if(viu)lead('whatsapp-'+o)}}}},true);
}})();
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(RAIZ, sl), exist_ok=True)
    open(os.path.join(RAIZ, sl, 'index.html'), 'w', encoding='utf-8').write(pg)
    print(sl + '/', len(d['desc']))
