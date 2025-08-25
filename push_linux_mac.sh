
#!/bin/bash
echo "======= Automação de push Git ======="
read -p "Digite o link do repositório GitHub: " REPO
git add .
git commit -m "Atualização do protótipo Saúde Conectada"
git branch -M main
git remote add origin $REPO
git push -u origin main
