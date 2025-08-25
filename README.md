
# Saúde Conectada – Protótipo (Flask + HTML)

Protótipo acadêmico para a Atividade Extensionista II (UNINTER): plataforma web simples para **monitoramento de saúde e bem-estar**, com:
- Cadastro de perfil
- Registro de atividades (exercício, alimentação)
- Registro de humor
- Dashboard com recomendações e gamificação (pontuação)
- Comunidade (mural de mensagens)

## 1️⃣ Instalação e execução local

Requisitos: Python 3.10+

```bash
# 1) Crie ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Instale dependências
pip install -r requirements.txt

# 3) Inicialize o banco e rode a aplicação
python app.py

# 4) Acesse no navegador
http://127.0.0.1:5000
```

### Telas do protótipo

1. **Index / Home** – visão geral e links rápidos  
2. **Perfil** – cadastro de informações pessoais e meta  
3. **Registrar Atividade** – registrar exercício ou alimentação  
4. **Registrar Humor** – registrar humor diário  
5. **Dashboard** – recomendações, pontos gamificação, atalhos  
6. **Comunidade** – postar dicas, motivação ou experiências

## 2️⃣ Publicação no GitHub

1. Crie um repositório chamado `saude_conectada`
2. Dentro da pasta do projeto, execute:

```bash
git init
git add .
git commit -m "Protótipo Saúde Conectada (Flask)"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/saude_conectada.git
git push -u origin main
```

## 3️⃣ Script de push automático

- **Windows:** `push_windows.bat`
- **Linux/macOS:** `push_linux_mac.sh`

Basta informar o link do repositório quando solicitado.

## 4️⃣ Roteiro para vídeo demo (YouTube)

1. **Introdução**: "Olá, este é o protótipo acadêmico Saúde Conectada..."  
2. **Perfil**: mostrar cadastro/edição do perfil e meta  
3. **Registro de Atividades**: registrar exercício e alimentação, mostrar gamificação  
4. **Registro de Humor**: registrar humor diário  
5. **Dashboard**: mostrar recomendações automáticas e pontos de gamificação  
6. **Comunidade**: postar mensagem de exemplo e mostrar mural atualizado  
7. **Conclusão**: reforçar objetivos do protótipo e aprendizado

> Observação: Protótipo acadêmico; não substitui orientação profissional em saúde.
"# saude_conectada_completa" 
