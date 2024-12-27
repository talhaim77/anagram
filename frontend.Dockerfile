FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy only package.json and lock files to cache dependencies
COPY similar-words-app/package.json similar-words-app/yarn.lock ./

# Install dependencies using Yarn
RUN yarn install

# Copy the rest of the frontend code
COPY similar-words-app/ ./

# Expose the React development server port
EXPOSE 3000

# Use wait-for-it.sh to wait for the backend before starting
CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh app:8000 -- yarn start"]
