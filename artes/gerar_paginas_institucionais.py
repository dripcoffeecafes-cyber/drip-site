# Gera as páginas institucionais (sobre, contato, trocas-e-devolucoes, privacidade, condicoes-de-compra)
# a partir do index.html. Rode depois de mudar o index:  python3 artes/gerar_paginas_institucionais.py
import json, os, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
B = 'https://driplabel.bloomingclub.com.br/'
SL = 'modelos|empresas|casamentos|eventos|fim-de-ano|consultorios-e-escritorios|sobre|contato|trocas-e-devolucoes|privacidade|condicoes-de-compra'


def entre(a, b):
    i = H.index(a); return H[i:H.index(b, i) + len(b)]


estilo = entre('<style>', '</style>')
pixel = entre('<!-- Meta Pixel -->', '</noscript>')
fontes = '\n'.join(l for l in H[:H.index('<style>')].splitlines() if 'fonts.g' in l)


def rel(x):
    x = re.sub(r'(src|href)="assets/', r'\1="../assets/', x)
    x = re.sub(r'href="#([a-z]+)"', r'href="../#\1"', x)
    x = re.sub(r'href="(%s)/' % SL, r'href="../\1/', x)
    return x.replace('class="logo" href="#"', 'class="logo" href="../"')


topo = rel(entre('<div class="aviso">', '</div>') + '\n' + entre('<header>', '</header>'))
rodape = rel(entre('<footer>', '</footer>'))
zap = rel(entre('<a class="zap-fixo', '</a>'))
ATUAL = '22/11/2026'
WA = '<a class="js-zap" data-origem="%s" href="#" target="_blank" rel="noopener">WhatsApp (54) 99708-1666</a>'

P = {
 'sobre': dict(tipo='AboutPage', nome='Sobre a Drip', titulo='Sobre a Drip Coffee Label: drip personalizado do grupo Blooming',
   desc='A Drip Coffee Label faz drip coffee personalizado com café especial de origem única, em Erechim/RS. Uma marca do grupo Blooming, clube de cafés especiais.',
   olho='Sobre nós', h1='Café especial com a sua marca, feito por quem vive de café.',
   corpo='''<p>A Drip Coffee Label é a marca de drip coffee personalizado do grupo Blooming, de Erechim, no Rio Grande do Sul. Fazemos drips com a marca, o nome ou a mensagem de quem presenteia, impressos direto no sachê, e com café especial de origem única dentro.</p>
<h2>De onde viemos</h2>
<p>O grupo nasceu do Blooming Club, clube de assinatura de cafés especiais criado por Manoela e Adriano. Os dois viveram cinco anos no Sul de Minas, em Alfenas e Poços de Caldas, onde conheceram o café especial de perto, com os produtores da região. De volta a Erechim, resolveram dividir essa descoberta, primeiro com os assinantes do clube e depois com empresas, casais e eventos, pela Drip.</p>
<h2>O que vai no sachê</h2>
<p>O café da Drip é o mesmo que vai para os assinantes do Blooming Club: especial, com 80+ pontos no protocolo SCA, avaliado por Q-Grader, de origem única no Sul de Minas, na Região Vulcânica. Nunca é blend. É 100% arábica, de torra média, com 10 g por sachê.</p>
<h2>Como trabalhamos</h2>
<ul class="lst"><li>Café, arte, impressão, envase e selagem com a mesma equipe.</li><li>A arte é impressa direto no sachê, sem etiqueta colada.</li><li>Criamos a arte sem custo, inclusive para quem não tem logo, e só produzimos depois da sua aprovação.</li><li>Cada sachê é dosado, selado e conferido um a um, em pequenos lotes.</li></ul>
<p class="fim"><a class="btn btn-cafe" href="../#modelos">Ver modelos e preços</a></p>'''),
 'contato': dict(tipo='ContactPage', nome='Contato', titulo='Contato | Drip Coffee Label',
   desc='Fale com a Drip Coffee Label pelo WhatsApp (54) 99708-1666, pelo e-mail ou pelo Instagram @driplabel.cafes. Drip coffee personalizado, Erechim/RS.',
   olho='Contato', h1='Fale com a gente.',
   corpo='''<div class="contatos">
<div><span>WhatsApp</span><b>%s</b><p>O caminho mais rápido para dúvidas, pedidos especiais, casamentos e quantidades acima de 1.000 sachês.</p></div>
<div><span>E-mail</span><b>dripcoffee@bloomingclub.com.br</b><p>Para propostas, notas e assuntos que precisam de registro.</p></div>
<div><span>Instagram</span><b><a href="https://www.instagram.com/driplabel.cafes/" target="_blank" rel="noopener">@driplabel.cafes</a></b><p>Drips de clientes e novidades.</p></div>
<div><span>Atendimento</span><b>Segunda a sexta</b><p>Das 9h às 12h e das 13h às 17h.</p></div>
</div>
<h2>Onde estamos</h2>
<p>Blooming Club Cafés Especiais Ltda, CNPJ 62.660.408/0001-47, Erechim/RS. Enviamos para todo o Brasil.</p>
<h2>Já comprou?</h2>
<p>Os pedidos são finalizados na loja Blooming Club. Para ver o seu pedido, acesse <a href="https://www.bloomingclub.com.br/contato?entrar=1" target="_blank" rel="noopener">Minha conta</a>. Para mandar a logo ou aprovar a arte, use o WhatsApp.</p>''' % (WA % 'contato')),
 'trocas-e-devolucoes': dict(tipo='WebPage', nome='Trocas e devoluções', titulo='Trocas e devoluções | Drip Coffee Label',
   desc='Política de trocas e devoluções da Drip Coffee Label para drip coffee personalizado: defeito de fabricação, avaria no transporte, prazos e como pedir.',
   olho='Políticas', h1='Trocas e devoluções',
   corpo='''<p>O drip personalizado é feito sob encomenda, com a sua arte. Por isso, as regras de troca são diferentes das de um produto de prateleira. Esta política segue a <a href="https://www.bloomingclub.com.br/politica-de-troca-e-devolucao" target="_blank" rel="noopener">política de troca e devolução da Blooming Club</a>, loja onde a compra é finalizada.</p>
<h2>Produto personalizado</h2>
<ul class="lst"><li>Não há direito de arrependimento depois da aprovação da arte e do início da produção.</li><li>Trocamos o produto em caso de defeito de fabricação ou se ele sair diferente da arte aprovada.</li><li>Erros de grafia ou de conteúdo que já estavam na arte aprovada por você não dão direito a troca ou reembolso. Por isso, confira a prova digital com atenção.</li><li>Se o seu pedido ainda não teve a arte aprovada, fale com a gente pelo WhatsApp.</li></ul>
<h2>Avaria no transporte</h2>
<ul class="lst"><li>Mande fotos do dano em até 48 horas depois do recebimento.</li><li>Dano real, como sachê rompido ou vazamento: repomos o item ou estornamos, parcial ou totalmente, conforme a análise.</li><li>Caixa de transporte amassada, sem dano aos sachês, não dá direito a troca.</li></ul>
<h2>Prazos</h2>
<ul class="lst"><li>Fotos de avaria: até 48 horas depois do recebimento.</li><li>Reclamação de defeito aparente: até 30 dias depois do recebimento.</li></ul>
<h2>Como pedir</h2>
<p>Envie pelo %s ou pelo e-mail cafes@bloomingclub.com.br: número do pedido, nome completo, o que aconteceu e fotos, quando houver avaria.</p>''' % (WA % 'trocas')),
 'privacidade': dict(tipo='WebPage', nome='Privacidade', titulo='Política de privacidade | Drip Coffee Label',
   desc='Como a Drip Coffee Label trata os seus dados: o que coletamos no site e no atendimento, para que usamos, cookies e Pixel da Meta, e como exercer os seus direitos.',
   olho='Políticas', h1='Política de privacidade',
   corpo='''<p>Esta política explica como a Drip Coffee Label, marca da Blooming Club Cafés Especiais Ltda (CNPJ 62.660.408/0001-47, Rua Hermínio Dal Mas, 241, Sala 01, Erechim/RS), trata os dados de quem visita este site e fala com a gente. A compra é finalizada na loja Blooming Club, que segue a <a href="https://www.bloomingclub.com.br/politica-de-privacidade" target="_blank" rel="noopener">política de privacidade da Blooming Club</a>.</p>
<h2>O que coletamos</h2>
<ul class="lst"><li>No site: páginas visitadas, origem do acesso, tipo de aparelho e ações como tocar em Comprar ou no WhatsApp, registrados por cookies e pelo Pixel da Meta (Facebook e Instagram).</li><li>No atendimento: nome, telefone, e-mail e o que você nos enviar, como logo, frases e dados para a arte.</li><li>Na compra, pela loja Blooming Club: nome, CPF ou CNPJ, endereço, contato e dados do pedido. Os dados do cartão ficam com o parceiro de pagamento.</li></ul>
<h2>Para que usamos</h2>
<ul class="lst"><li>Produzir o seu pedido, criar a arte com a logo e os dados que você enviar e entregar.</li><li>Responder mensagens e enviar avisos do pedido.</li><li>Entender o uso do site, melhorar a experiência e medir e direcionar anúncios.</li></ul>
<p>Não vendemos dados pessoais.</p>
<h2>Com quem compartilhamos</h2>
<p>Só quando necessário para prestar o serviço ou cumprir a lei: operadores de pagamento, transportadoras, sistema de notas fiscais, plataformas de loja, medição e anúncios, e autoridades públicas quando exigido.</p>
<h2>Cookies</h2>
<p>Você pode bloquear ou apagar cookies nas configurações do seu navegador. Isso não impede a compra, mas pode limitar a medição.</p>
<h2>Seus direitos</h2>
<p>Você pode pedir confirmação de tratamento, acesso, correção, exclusão quando cabível, informação sobre compartilhamento e revogação do consentimento quando cabível, pelo e-mail cafes@bloomingclub.com.br.</p>
<p class="atual">Atualizada em %s.</p>''' % ATUAL),
 'condicoes-de-compra': dict(tipo='WebPage', nome='Condições de compra', titulo='Condições de compra | Drip Coffee Label',
   desc='Condições de compra do drip coffee personalizado: pedido mínimo, preços por quantidade, pagamento, arte, prazo de produção, frete e entrega.',
   olho='Políticas', h1='Condições de compra',
   corpo='''<p>O resumo abaixo vale para os pedidos feitos por este site. A compra é finalizada na loja Blooming Club e segue também os <a href="https://www.bloomingclub.com.br/termos-e-condicoes-gerais" target="_blank" rel="noopener">termos e condições gerais da Blooming Club</a>.</p>
<h2>Pedido e preço</h2>
<ul class="lst"><li>Pedido mínimo de 50 sachês, em kits de 50.</li><li>O preço por sachê cai a partir de 150 e de 300 sachês, com o desconto aplicado no carrinho.</li><li>Pagamento por Pix, boleto ou cartão, na loja.</li></ul>
<h2>Arte</h2>
<ul class="lst"><li>Criamos a arte sem custo, inclusive para quem não tem logo.</li><li>A logo é enviada em vetor (AI, EPS, SVG ou PDF vetorial), pelo WhatsApp, depois da compra.</li><li>Mandamos a prova digital, com 2 ajustes incluídos. Só produzimos depois da sua aprovação.</li><li>Cada kit de 50 sai com uma arte. Não fazemos fundo colorido nem foto cobrindo o sachê.</li><li>Kraft Clássico: impressão em preto. Kraft Premium e Branco Premium: preto ou colorido, pelo mesmo preço.</li></ul>
<h2>Produção e entrega</h2>
<ul class="lst"><li>Produção em 5 dias úteis depois da aprovação da arte.</li><li>Frete e prazo da transportadora calculados pelo CEP no carrinho, antes do pagamento. Enviamos para todo o Brasil.</li><li>Os 50 sachês de cada kit seguem em caixa.</li></ul>
<h2>Trocas</h2>
<p>Veja a nossa <a href="../trocas-e-devolucoes/">política de trocas e devoluções</a>.</p>'''),
}

CSS = '''<style>
.inst-pg{max-width:760px;margin:0 auto;padding:56px 20px 90px}
.inst-pg h1{font-size:clamp(38px,5vw,56px);line-height:1.06;margin:12px 0 26px}
.inst-pg h2{font-size:28px;margin:38px 0 12px}
.inst-pg p{font-size:16.5px;margin:0 0 14px}.inst-pg a{text-decoration:underline;text-underline-offset:3px}
.inst-pg .btn{text-decoration:none}.inst-pg .fim{margin-top:34px}
.inst-pg .atual{margin-top:30px;color:var(--apoio);font-size:14px}
.lst{list-style:none;margin:0 0 14px;padding:0;display:grid;gap:9px}
.lst li{position:relative;padding-left:20px;font-size:16px}.lst li:before{content:"";position:absolute;left:0;top:.75em;width:8px;height:1px;background:var(--cafe)}
.contatos{display:grid;gap:14px}@media(min-width:700px){.contatos{grid-template-columns:1fr 1fr}}
.contatos div{border:1px solid var(--borda);padding:20px 22px}
.contatos span{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--apoio);margin-bottom:6px}
.contatos b{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:22px;margin-bottom:6px}
.contatos p{font-size:14.5px;color:var(--apoio);margin:0}
.migalha{font-size:13px;color:var(--apoio)}.migalha a{text-decoration:none}
</style>'''

for sl, d in P.items():
    url = B + sl + '/'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": d['tipo'], "@id": url + "#pagina", "url": url, "name": d['titulo'], "description": d['desc'], "inLanguage": "pt-BR",
         "isPartOf": {"@id": B + "#website"}, "about": {"@id": B + "#organization"}},
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
<link rel="icon" href="../favicon.ico">
{fontes}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{estilo}
{CSS}
{pixel}
</head>
<body>
{topo}
<main class="inst-pg">
  <nav class="migalha" aria-label="Você está em"><a href="../">Início</a> / {d['nome']}</nav>
  <span class="olho" style="display:block;margin-top:26px">{d['olho']}</span>
  <h1>{d['h1']}</h1>
  {d['corpo']}
</main>
{rodape}
{zap}
<script>
(function(){{
  var ZAP='https://wa.me/5554997081666?text='+encodeURIComponent('Olá! Vim pelo site da Drip Coffee Label e quero falar com vocês.');
  document.querySelectorAll('.js-zap').forEach(function(a){{a.href=ZAP;a.target='_blank';a.rel='noopener'}});
  document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a.js-zap');if(a&&window.fbq)try{{fbq('track','Contact',{{content_name:a.getAttribute('data-origem')||'whatsapp'}})}}catch(x){{}}}},true);
}})();
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(RAIZ, sl), exist_ok=True)
    open(os.path.join(RAIZ, sl, 'index.html'), 'w', encoding='utf-8').write(pg)
    print(sl + '/', len(d['desc']))
