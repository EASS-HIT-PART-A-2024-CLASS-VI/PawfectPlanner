# Step 1: Build the React frontend
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Build the app
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

# Copy build output to Nginx directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 inside the container (will be mapped to 3000 in docker-compose)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]