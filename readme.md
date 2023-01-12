# League of data ingestion

Projeto para a pratica de criação de data pipelines. Buscando os dados dos desafiantes do Brasil, e suas ultimas partidas, armazenando em um data lake local. A ideia é coletar dados dos jogadores de league of legends e analisar, um exemplo é entender nossos jogares challengers, quem sabe não só do Brasil mas de outros servers.

Link para o post explicando [post](https://www.linkedin.com/pulse/criei-um-pipeline-de-dados-com-api-do-jogo-league-legends-raimundi/?published=t&trackingId=5OFjQqrVSz2pcQ0DstwORA%3D%3D)

## Arquitetura
![image info](./images/arquitetura.png)

<br>
<br>

## Utilizando o projeto

Para rodar o projeto, você precisa de um token da api da riot, neste link: [riot_api](https://developer.riotgames.com/) você pode criar seu app e solicitar o token de desenvolvimento, caso ja tenha algum, só colocar nos .env ao longo dos diretórios e tudo certo. Por que não é somente um .env, você pode rodar a aplicação data_colector isoladamente do ETL, ou no jupyter também.

Verifique se as portas utilizadas pelos docker-compose estão livres, ou então substitua pelas portas de sua preferência.
<br>
<br>

## Comandos com Make

Você pode utilizar o make para iniciar a aplicação facilmente.

### Instalando dependências

```bash
make install_dependencies
```

### Iniciando containers
```bash
make start_all
```

### Parando os containers
```bash
make stop
```

### Removendo os container com volumes
*Este comando ira remover todos os dados, até mesmo os dados coletados*
```bash
make remove
```

### Make commands
Caso tenha alguma duvida de quais comandos podem ser utilizados utilize:
```bash
make help
```
<br>

### Url das aplicações

**Caso não tenho mudado as portas dos containers**

### 

Spark UI: http://localhost:8080 <br>
Airflow UI: http://localhost:8088 <br>
Minio UI: http://localhost:9001 <br>
Metabase: http://localhost:3000 <br>
Jupyter: http://localhost:8888

Fique a vontade para clonar o projeto ou contribuir.
