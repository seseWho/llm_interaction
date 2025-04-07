# LLM Interaction Client

## Project Description

This project provides a flexible client for interacting with Large Language Models (LLM), designed to facilitate information extraction, response generation, and comprehensive testing.

## Key Features

- 🚀 Configurable LLM client
- 🧪 Complete unit test suite
- 🔒 Secure credential management
- 📊 Model performance analysis
- 🌐 Multilingual support

## Prerequisites

- Python 3.8+
- Account with an LLM API provider (OpenAI, Anthropic, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/seseWho/llm-interaction-client.git
cd llm-interaction-client
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory:
```
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=model_name
```

## Basic Usage

### Initialize Client
```python
from llm_client import LLMClient
from config import API_KEY, BASE_URL, MODEL_NAME

# Create LLM client
client = LLMClient(API_KEY, BASE_URL, MODEL_NAME)

# Generate response
response = client.generate_response("Hello, how are you?")
print(response)
```

### Run Tests
```bash
python test_suite.py
```

## Test Suite Features

The test suite includes:
- Initial connection test
- Response generation
- Response time measurement
- Context length limit
- Multilingual support
- Temperature variation
- JSON generation
- Code generation
- Logical reasoning tests

## Project Structure

```
llm_interaction/
│
├── src/
│   ├── llm_client.py       # Main LLM client
│   ├── test_suite.py       # Test battery
│   └── config.py           # Configurations and constants
│
├── tests/                  # Additional tests
│   └── test_llm_client.py  
│
├── main.py                 # Program entry point
└── requirements.txt        # Project dependencies
```

## Customization

- Modify `config.py` to change configurations
- Adjust `llm_client.py` to adapt to different APIs
- Extend `test_suite.py` with specific use case tests

## Security Considerations

- Never commit your API credentials
- Use environment variables
- Limit access to configuration files

## Contributions

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - sergio.sesena@gmail.com

Project Link: [https://github.com/seseWho/llm-interaction-client](https://github.com/seseWho/llm-interaction-client)

## Acknowledgments

- [Requests](https://docs.python-requests.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

**Note:** This project is under continuous development. Contributions and suggestions are welcome.