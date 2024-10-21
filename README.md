## Instruções para Configuração e Execução do Aplicativo

### Configuração do Ambiente Virtual

Crie um ambiente virtual utilizando o comando: 
   
```bash
python3 -m venv venv
```

### Ativação do Ambiente Virtual

Ative o ambiente virtual (se criado) usando o comando: 

```bash
source venv/bin/activate
```

### Instalação das Dependências

Instale as bibliotecas necessárias executando o comando: 

```bash
python3 -m pip install -r requirements.txt
pre-commit install
```

### Criar o banco de dados
```bash
python3
from src.infra import *
db_conn = DBConnectionHandler()
engine = db_conn.get_engine()
Base.metadata.create_all(engine)
```

### Env
export FLASK_APP=run
flask run