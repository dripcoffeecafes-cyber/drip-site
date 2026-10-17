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
