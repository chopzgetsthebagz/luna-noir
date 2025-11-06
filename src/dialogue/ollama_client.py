"""
Ollama Client for Luna Noir Bot
Handles AI response generation using local Ollama models
"""

import os
import logging
import requests
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Client for interacting with Ollama API for AI-powered responses
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1:8b",
        temperature: float = 0.8,
        max_tokens: int = 500
    ):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama API base URL (default: http://localhost:11434)
            model: Model name to use (default: llama3.1:8b)
            temperature: Response randomness 0.0-1.0 (default: 0.8)
            max_tokens: Maximum response length (default: 500)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"
        
        logger.info(f"Ollama client initialized: {self.base_url} | model: {self.model}")
    
    def is_available(self) -> bool:
        """
        Check if Ollama server is running and accessible
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama server not available: {e}")
            return False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """
        Generate a response using Ollama
        
        Args:
            prompt: User's message/prompt
            system_prompt: Optional system prompt to set context
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated response text or None if failed
        """
        try:
            # Build the full prompt with system context if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens
                }
            }
            
            logger.debug(f"Sending request to Ollama: {prompt[:50]}...")
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                logger.info(f"Ollama response generated: {len(generated_text)} chars")
                return generated_text
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return None
        except Exception as e:
            logger.error(f"Error generating Ollama response: {e}", exc_info=True)
            return None
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """
        Generate a response using Ollama's chat endpoint with conversation history
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello"}]
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated response text or None if failed
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens
                }
            }
            
            logger.debug(f"Sending chat request to Ollama with {len(messages)} messages")
            
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result.get("message", {})
                generated_text = message.get("content", "").strip()
                logger.info(f"Ollama chat response generated: {len(generated_text)} chars")
                return generated_text
            else:
                logger.error(f"Ollama chat API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Ollama chat request timed out")
            return None
        except Exception as e:
            logger.error(f"Error generating Ollama chat response: {e}", exc_info=True)
            return None
    
    def list_models(self) -> List[str]:
        """
        List available Ollama models
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model.get("name") for model in data.get("models", [])]
                logger.info(f"Available Ollama models: {models}")
                return models
            return []
        except Exception as e:
            logger.error(f"Error listing Ollama models: {e}")
            return []


def create_ollama_client(
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None
) -> OllamaClient:
    """
    Factory function to create OllamaClient from environment variables
    
    Args:
        base_url: Override OLLAMA_BASE_URL env var
        model: Override OLLAMA_MODEL env var
        temperature: Override OLLAMA_TEMPERATURE env var
        
    Returns:
        Configured OllamaClient instance
    """
    return OllamaClient(
        base_url=base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        model=model or os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        temperature=temperature or float(os.getenv("OLLAMA_TEMPERATURE", "0.8"))
    )


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create client
    client = create_ollama_client()
    
    # Check availability
    if client.is_available():
        print("✓ Ollama server is running")
        
        # List models
        models = client.list_models()
        print(f"Available models: {models}")
        
        # Test generation
        response = client.generate(
            prompt="Say hi in one sentence.",
            system_prompt="You are Luna Noir, a witty and mysterious AI companion."
        )
        print(f"\nResponse: {response}")
    else:
        print("✗ Ollama server is not running. Start it with: ollama serve")

