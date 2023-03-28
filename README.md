# CRUD

Essa aplicação tem como objetivo simular a inscrição de usuário no BBB 24 via uso de API Rest. Foi usada a linguagem Python na versão 3.10 e a framework web Django-rest-framework (DRF).

Para usá-la localmente siga os passos abaixo:

  1. Clone o projeto atual:
  
    git clone https://github.com/douglasnotfunny/crud.git
  
  2. Crie o ambiente virtual
  
    python3.10 -m venv venv
    
  3.1. Ative o ambiente, caso seja Windows com o comando abaixo:
    
    source venv/Scripts/activate
   
  3.2. Ative o ambiente, caso seja Linux com o comando abaixo:
    
    source venv/bin/activate
  
  4. Instale as bibliotecas utilizadas no projeto
  
    pip install -r requirements.txt
    
  5. Crie o banco de dados utilizado no projeto
  
    python manage.py makemigrations

  6. Realize a migração da tabela de cadastro
    
    python manage.py migrate
  
  7.1. Criação do superusuário para acessar a página de administração do banco de dados
    
    python manage.py createsuperuser
  
  7.2. Caso a criação do superusuário com o comando acima não funcione, utilize o seguinte comando:
    
    winpty python manage.py createsuperuser
  
  8. Execute o servidor local da aplicação
    
    python manage.py runserver
  
  9. Acesse a página principal do Django-rest-framework http://localhost:8000/
  
  9.1. Para testar o CRUD dos candidatos do BBB 24 pode ser usada a tela http://localhost:8000/api/usuarios/ 
  
  9.2. Como a aplicação foi criada em Django Rest, também pode ser usado o POSTMAN para envio das informações. Nesse repositório contém a collection usada para testes locais. Basta importar o arquivo de nome CRUD_BBB.postman_collection.json que se encontra na raiz do projeto.
  
  10. A API também foi deployada no link com os mesmos path http://douglassg10.pythonanywhere.com/api/usuarios/ a collection da aplicação deployada está no arquivo CRUD_BBB_DEPLOY.postman_collection.json que se encontra na raiz do projeto.
