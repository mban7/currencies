FROM node:18 as build

WORKDIR /app

COPY . .
RUN npm install
RUN npm run build --configuration production

FROM nginx:alpine
COPY --from=build /app/dist/frontend /usr/share/nginx/html

