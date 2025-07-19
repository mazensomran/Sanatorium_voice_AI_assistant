# Sanatorium AI Assistant - Complete Documentation

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![LLM Backend](https://img.shields.io/badge/LLM-GigaChat-free)
![License](https://img.shields.io/badge/license-MIT-green)

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technical Architecture](#technical-architecture)
4. [Installation Guide](#installation-guide)
5. [License](#license)

## Project Overview <a name="project-overview"></a>

AI-powered virtual assistant for sanatorium bookings using Sberbank's GigaChat language model. The system provides:

- Natural language understanding
- Multi-stage booking workflows
- CRM data formatting
- Personalized conversational experiences

## Key Features <a name="key-features"></a>

### Conversation Management
- Intent recognition
- Context-aware dialogues
- Multi-turn conversation handling
- Error recovery mechanisms

### Technical Capabilities
- GigaChat API integration
- Session persistence
- Input validation
- Response caching
- Modular prompt templates

## Technical Architecture <a name="technical-architecture"></a>

```mermaid
graph LR
    A[User Input] --> B(Dialog Manager)
    B --> C{GigaChat API}
    C --> D[Response Generation]
    D --> E[Output Formatting]
    E --> F[User Response]
    B --> G[CRM Data Formatter]
    G --> H[External Systems]  


## Installation Guide <a name="installation-guide"></a>
### Prerequisites
- Python 3.8+
- [GigaChat developer account](https://developers.sber.ru/)
- Basic server environment

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sanatorium-ai-assistant.git
cd sanatorium-ai-assistant

## 📜 License 

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for full details.

### Permissions ✅
- Commercial use
- Modification
- Distribution  
- Private use

### Limitations ❌
- Liability
- Warranty

### Requirements 📝
- Include original license and copyright notice
- State all significant changes

```text
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted...
