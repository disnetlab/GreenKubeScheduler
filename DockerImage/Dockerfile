# Use Debian as the base image
FROM debian:latest

# Install necessary tools
RUN apt-get update && apt-get install -y \
    stress-ng \
    bc \
    coreutils && apt-get clean

