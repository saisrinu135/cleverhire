FROM node:22-alpine


WORKDIR /app

RUN apk add --no-cache python3 make g++ libc6-compat

COPY package.json ./

RUN npm install

COPY . .

RUN npm run build


# for production (no need of code after building)
FROM node:22-alpine

# Copy built application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

# Set environment
ENV NODE_ENV=production

EXPOSE 3000

CMD ["npm", "start"]