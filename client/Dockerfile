# BASE
FROM node:23.11.1 AS base
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# DEV
FROM base AS dev
COPY . .
CMD ["npm", "run", "dev", "--", "--host"]

# BUILD
FROM base AS build
COPY . .
RUN npm run build

# PROD
FROM nginx:alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
