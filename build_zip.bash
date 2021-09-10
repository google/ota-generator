#!/bin/bash
zip otatools.zip -d bin/sign_apex bin/aapt2 \
	bin/merge_target_files bin/sign_target_files_apks \
	bin/add_img_to_target_files bin/build_image \
	bin/validate_target_files bin/img_from_target_files \
	bin/check_target_files_vintf bin/build_super_image \
	bin/mkuserimg_mke2fs bin/mk_combined_img bin/apexer \
	bin/build_verity_metadata bin/fc_sort "*.pyc" || true

image_id=$(docker build -q .)
container_id=$(docker run -d --entrypoint /usr/bin/sleep ${image_id} 120)
docker container exec ${container_id} zip /app.zip -r /app
docker container cp ${container_id}:/app.zip .
docker container stop ${container_id}
docker container rm ${container_id}
