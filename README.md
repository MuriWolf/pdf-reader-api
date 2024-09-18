# Início
Faça o clone do projeto e vá para sua pasta.

# Baixar dependencias
```bash
pip install -r requirements.txt
```

# Banco de Dados
## Instalação (Linux)
Instalação MariaDB, no Linux Mint, baixei o arquivo .deb e executei.</br>
**fonte:** https://pssp.app.br/infraestrutura/linux/banco_de_dados/mariadb/instalar.html

Use o DBeaver para mexer no Banco.</br>
**fonte:** https://dbeaver.io/download/

Antes de logar no MySQL 
```bash
sudo mysql_secure_installation
```
e mude a senha para root. <br>

**fonte:** https://www.youtube.com/watch?v=CnRRCTMvs8Q

## Configuração Banco de Dados
### Criar banco
Dentro do SQL (após o login com `mysql -u root -p`), rodar o script de criação do banco e das tabelas. O arquivo se chama '[criar_banco.txt](https://github.com/MuriWolf/pdf-reader-api/blob/main/criar_banco.txt)' e se encontra na base deste repositório. 
### Fazer conexão através de um cliente SQL (DBeaver, exemplo)
- Nome banco: trabalho_douglas
- Senha: root
- porta: 3306 (normalmente é o default)

# Rodar a API
```bash
fastapi dev main.py
```
caso der erro no código acima, tente esse:
```bash
python -m uvicorn main:app 
```
# Rodar testes 
```bash
python -m pytest
```
> Talvez seja necessário usar 'python3' ao invés de 'python'
