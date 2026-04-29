FROM nginx:alpine 
RUN echo "custom nginx image created"
WORKDIR /usr/share/nginx/html
COPY index.html .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

