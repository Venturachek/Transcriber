docker network create newNetwork

docker run --name ollama_reviewer \
  -p 11434:11434 \
  --network=newNetwork \
  -v ollama_data:/root/.ollama \
  -d ollama/ollama:latest

docker exec -it ollama_reviewer ollama pull qwen2.5:7b

docker compose --network=newNetwork up --build