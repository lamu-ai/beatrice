# Uses yarn instead of npm because of
# https://github.com/vitejs/vite/issues/6767

FROM node:lts-alpine as base
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .

FROM base as build
COPY --from=base /app /app
WORKDIR /app
RUN npm run build

from base as development
COPY --from=base /app /frontend
WORKDIR /frontend
CMD ["yarn", "dev"]

FROM nginx:stable-alpine as production
COPY --from=build /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
