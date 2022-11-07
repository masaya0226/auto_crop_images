

.PHONY: run

run:
	docker-compose run --rm auto_crop_images python main.py ${dir}