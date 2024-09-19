# Início
Este projeto é uma API de uma aplicação que visa, através de PDFs de multas de trânsito, extrair seus dados e armazená-los no site, onde é possível ter maior controle sobre eles. Este projeto é um trabalho de [Universidade](https://unimar.br/), que tem como foco a empresa [DSIN](https://www.dsin.com.br/), crida em Marília e que atua em mais de 100 munícipios. </br>
> Para ver o frontend do projeto, [clique aqui](https://github.com/MuriWolf/pdf-reader).

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
fastapi dev src/main.py
```
# Rodar testes 
```bash
python -m pytest
```
> Talvez seja necessário usar 'python3' ao invés de 'python'
