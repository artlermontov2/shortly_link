#!/bin/bash

celery -A app.tasks.celery:celery worker -B --loglevel=info