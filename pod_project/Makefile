###########################################
# Run rabbitmq and celeri for development #
###########################################

RABBITMQ-NAME := rabbitmq-pod
CELERY-NAME := pod_project

run-rabbitmq:
	docker ps -aq --filter name=$(RABBITMQ-NAME) | xargs -r docker rm -f -v && docker run -d --hostname $(RABBITMQ-NAME) --name $(RABBITMQ-NAME) -p 5672:5672 rabbitmq:3

# run-celery: run-rabbitmq
# 	celery -A $(CELERY-NAME) worker -l info

run-celery:
	celery -A $(CELERY-NAME) worker -l info

.PHONY: all build deploy clean run-rabbitmq run-celery
