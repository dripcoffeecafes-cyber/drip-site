# Landing page Drip Coffee Label

Página estática (HTML, CSS e JS puros), pronta para GitHub Pages com domínio próprio.

## Publicar no GitHub Pages
1. Suba o conteúdo desta pasta na raiz de um repositório (index.html, assets/, .nojekyll).
2. No repositório: Settings > Pages > Source: Deploy from a branch > main / (root).
3. Em Custom domain, informe o subdomínio (ex.: drip.bloomingclub.com.br). O GitHub cria o arquivo CNAME.
4. No DNS do domínio bloomingclub.com.br, crie um registro CNAME:
   - Nome: drip (ou o subdomínio escolhido)
   - Valor: dripcoffeecafes-cyber.github.io
5. Depois que o DNS propagar, marque Enforce HTTPS.

## Onde mudar as coisas
- Número do WhatsApp e links dos produtos: bloco `<script>` no fim do index.html (constantes ZAP e MODELOS).
- Preços da calculadora: arrays `precos` em MODELOS (faixas 50, 100, 150, 200, 250 e 300+).
- Aviso de fim de ano (27/11): primeira linha do `<body>`, div `.aviso`.
- Todos os links para o site levam UTM (`utm_source=drip-landing`) para separar as vendas vindas da página no relatório da loja.

## Imagens
Fotos reais do acervo (drip-acervo), convertidas para WebP. Sem a Termolar (não autorizou uso de imagem) e sem nome de cliente nas legendas.
