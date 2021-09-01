# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY src ./src
COPY public ./public
COPY *.js .
COPY .env* .
COPY .eslint* .

RUN npm run build

# production stage
FROM ubuntu:20.04 as production-stage
RUN apt-get update && apt-get --no-install-recommends install -y python3.9 unzip xxd cgpt unzip openjdk-16-jre-headless zip less

WORKDIR /app
VOLUME [ "/app/target", "/app/output"]
COPY otatools.zip .
COPY --from=build-stage /app/dist ./dist
COPY *.py .

EXPOSE 8000
CMD ["python3.9", "web_server.py"]