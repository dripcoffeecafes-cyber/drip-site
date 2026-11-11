# Landing page Drip Coffee Label

Página estática (HTML, CSS e JS puros), pronta para GitHub Pages com domínio próprio.

## Publicar no GitHub Pages
1. Suba o conteúdo desta pasta na raiz de um repositório (index.html, assets/, .nojekyll).
2. No repositório: Settings > Pages > Source: Deploy from a branch > main / (root).
3. Em Custom domain, informe driplabel.bloomingclub.com.br (o arquivo CNAME já está na raiz do repositório).
4. No DNS do domínio bloomingclub.com.br, crie um registro CNAME:
   - Nome: driplabel
   - Valor: dripcoffeecafes-cyber.github.io
5. Depois que o DNS propagar, marque Enforce HTTPS.

## Onde mudar as coisas
- Número do WhatsApp e produtos: bloco `<script>` no fim do index.html (constantes ZAP e M). Cada modelo tem em `v` o número do produto na loja da Betalabs (www.bloomingclub.com.br): Kraft Clássico 33, Branco Premium 278, Kraft Premium 281. Os botões "Comprar" abrem `https://www.bloomingclub.com.br/checkout/cart/item/add/NÚMERO?quantity=KITS`; conta e carrinho do topo também vão para o www (desde 11/11/2026; antes era a loja Nuvemshop).
- Preços: arrays `p` em M (faixas 50, 100, 150, 200, 250 e 300+). A tabela de preços é montada a partir deles.
- Todos os links para a loja levam UTM (`utm_source=drip-landing`) para separar as vendas vindas da página no relatório da loja.
- Cabeçalho: logo da Drip, "by" e logo do Blooming Club (assets/img/blooming.webp, feito do blooming.png); ícones de conta (www.bloomingclub.com.br/contato?entrar=1, abre o login da loja) e carrinho (/checkout/cart) da loja Betalabs.

## Imagens
- `fotos/`: originais enviados pelo Adriano em 17/10/2026.
- `assets/img/`: versões otimizadas em WebP usadas na página. Sachês do topo e dos produtos (hero-drips, p-*-cut) saem dos mockups oficiais do acervo (drip-acervo, ilustracoes/claude-mockup_sua-marca-kraft_v3, branco_v3 e kraft-premium_v5). Clientes (cli-*) saem dos recortes reais do acervo (fotos/2026-11_*_fundo-transparente.png; Termolar e GL Fibra com a cor do kraft corrigida só aqui). Todos os clientes autorizaram o uso.
- `assets/video/momentos-marcas.mp4`: montagem de bastidores (impressão e selagem de várias marcas) feita dos vídeos do acervo.
- Cenas de IA com "sua marca aqui" sinalizadas no rodapé como ilustrativas.

## Medição (Meta)
- Dois pixels durante a troca: Pixel_DripCoffee (1636404041306148, portfólio Drip Coffee Label) e Pixel_Nuvem (29552796950978987, Grupo Blooming), o pixel único do grupo, o mesmo da loja Nuvemshop.
- O clique para a loja vai como InitiateCheckout só no Pixel_DripCoffee; no Pixel_Nuvem vira o evento próprio IrParaLoja, porque o checkout da Nuvemshop já envia o InitiateCheckout.
- Lead (só no Pixel_Nuvem): enviado no primeiro clique de interesse da visita, num botão de WhatsApp (content_name whatsapp-<origem>) ou num Comprar (loja-<modelo>), uma vez por sessão. É a base da conversão personalizada "Lead Drip" (evento Lead, URL contém driplabel), na qual a campanha DripNuvem otimiza. Contact e IrParaLoja continuam como antes.
- O Pixel_DripCoffee sai 2 a 3 semanas depois de as compras da Drip aparecerem no Pixel_Nuvem.
