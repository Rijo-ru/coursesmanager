FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/nginx/courses_manager.conf /etc/nginx/conf.d/courses_manager.conf