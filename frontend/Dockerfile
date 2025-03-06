# Step 1: Build React frontend
FROM node:18-alpine AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

# ✅ Copy built frontend to Nginx HTML directory
COPY --from=build /app/dist /usr/share/nginx/html

# ✅ Copy custom Nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ✅ Prevent missing favicon errors
RUN echo "" > /usr/share/nginx/html/favicon.ico

# ✅ Expose port 80 for frontend
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
