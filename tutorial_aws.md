# EB CONFIG

ES_2425: cd banco
ES_2425/banco:

pip install -r requirements.txt

pip freeze > requirements.txt

eb init

eb create banco-env --service-role LabRole --keyname vockey --instance_profile LabInstanceProfile

eb deploy



NÃO FAZER ISTO AINDA
# Cognito
- Amazon Cognito
- Get started for free in less than 5 min
- Define your application 
    - NÃO MUDAR NADA!
- Configure options
    - Por agora
        - Email como "options for sign-in identifiers"
    - Required attributes for sign-up
        - Email
        - Name
        - phone_number
    - Add a return URL
        - Será a nossa home page com o log in feito, dps tratamos disso
        - Eu meto "https://127.0.0.1:8000/test/", visto que serve para test