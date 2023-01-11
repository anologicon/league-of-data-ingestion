status: ## Status dos containers
	docker ps

install_dependencies: ## Instala dependências para o projeto
	docker compose -f docker-compose.yaml pull
	docker compose -f docker-compose.yaml build
	docker compose -f docker-compose-airflow.yml pull
	docker compose -f docker-compose-airflow.yml build

start_all: ##inicia todo o projeto
	@echo 'Start All Services: Spark, Airflow, Minio, PostgreSql, Metabase'
	@make start_airflow
	@make start_spark_and_minio

start_airflow: ## Inicia os containers do airflow
	@echo 'Start Airflow'
	docker-compose -f docker-compose-airflow.yaml up -d

start_spark_and_minio: ## Inicia os containers do minio, spark, metabase e posgresql
	@echo 'Start Spark, Minio and Metabase'
	docker-compose -f docker-compose.yaml up -d

stop: ## Para todos os containers
	docker-compose -f docker-compose-airflow.yaml down
	docker-compose -f docker-compose.yaml stop

remove: ## Remove os containers e os volumes. Este comando ira deletar todos os dados
	docker-compose -f docker-compose-airflow.yaml down --volumes
	docker-compose -f docker-compose.yaml down --volumes

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'