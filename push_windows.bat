
@echo off
echo ======= Automação de push Git =======
set /p REPO="Digite o link do repositório GitHub: "
git add .
git commit -m "Atualização do protótipo Saúde Conectada"
git branch -M main
git remote add origin %REPO%
git push -u origin main
pause
