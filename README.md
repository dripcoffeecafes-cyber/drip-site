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
- Número do WhatsApp e links dos produtos: bloco `<script>` no fim do index.html (constantes ZAP e MODELOS).
- Preços da calculadora: arrays `precos` em MODELOS (faixas 50, 100, 150, 200, 250 e 300+).
- Todos os links para o site levam UTM (`utm_source=drip-landing`) para separar as vendas vindas da página no relatório da loja.

## Imagens
- `fotos/`: originais enviados pelo Adriano em 17/10/2026 (mockups "sua marca aqui", fotos da Blooming Club, cenas de IA e fotos reais).
- `assets/img/`: versões otimizadas em WebP usadas na página. Os mockups dos modelos tiveram o fundo branco removido e foram aplicados no fundo de estúdio da marca.
- Nenhuma imagem com marca de cliente. Cenas de IA sinalizadas no rodapé como ilustrativas.

## Medição (Meta)
- Dois pixels durante a troca: Pixel_DripCoffee (1636404041306148, portfólio Drip Coffee Label) e Pixel_Nuvem (29552796950978987, Grupo Blooming), o pixel único do grupo, o mesmo da loja Nuvemshop.
- O clique para a loja vai como InitiateCheckout só no Pixel_DripCoffee; no Pixel_Nuvem vira o evento próprio IrParaLoja, porque o checkout da Nuvemshop já envia o InitiateCheckout.
- O Pixel_DripCoffee sai 2 a 3 semanas depois de as compras da Drip aparecerem no Pixel_Nuvem.
