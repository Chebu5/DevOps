FROM nginx:1.27-alpine

# Пути относительно контекста сборки (frontend/)
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY static/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]