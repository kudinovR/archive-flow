# Stage 1 – Build
FROM node:22-alpine AS builder

WORKDIR /app

# First copy package.json to utilize Docker Layer Cache

COPY package.json package-lock.json ./

RUN npm ci

# Then copy the rest of the code and build
COPY . .

RUN npm run build

# Stage 2 – Serve
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]