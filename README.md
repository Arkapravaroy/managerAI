# Manager AI

An intelligent conversational assistant designed specifically for CEOs, product managers, and executive managers. Built with LangGraph and LangChain, Manager AI helps with project management, research, task tracking, and strategic decision-making.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/manager-ai/blob/main/ManagerAIV1.ipynb)

## 🚀 Features

### Product Management Capabilities
- **Market Research and Analysis**: Automatically gather and analyze market data, competitor information, and industry trends
- **User Feedback Analysis**: Process and categorize customer feedback from various channels
- **User Story and Requirement Drafting**: Assist in creating user stories and acceptance criteria
- **Product Roadmap Management**: Help create and manage product roadmaps with intelligent prioritization
- **Feature Prioritization**: Data-driven feature prioritization based on business value and effort
- **Performance Tracking**: Monitor key product metrics and identify improvement areas

### Project Management Capabilities
- **Project Planning**: Create detailed project plans with timelines and dependencies
- **Task Management**: Automated task creation, assignment, and progress tracking
- **Resource Allocation**: Optimize resource allocation and identify potential conflicts
- **Risk Management**: Proactively identify and suggest mitigation strategies for project risks
- **Progress Monitoring**: Real-time project progress tracking and stakeholder reporting
- **Communication Management**: Draft updates, notifications, and meeting summaries

### AI-Powered Features
- **Intelligent Memory**: Remembers user preferences, project context, and historical decisions
- **Multi-Source Research**: Integrates web search, Wikipedia, and academic papers (arXiv)
- **Context-Aware Responses**: Provides personalized recommendations based on user profile and history
- **Automated Documentation**: Generates and maintains project documentation and reports

## 📋 Prerequisites

- Python 3.8+
- API Keys for:
  - [Groq](https://groq.com/) (Required)
  - [Tavily](https://tavily.com/) (Required)
  - [LangSmith](https://langsmith.langchain.com/) (Optional, for tracing)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/manager-ai.git
   cd manager-ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
   ```

## 🚀 Quick Start

### Command Line Interface
```bash
python main.py
```

### Run Example Demo
```bash
python main.py --example
```

### Run Specific Examples
```bash
python examples/example_usage.py
```

## 💬 Usage Examples

### Personal Information Management
```
User: "My name is Sarah, and I work for the product team in London."
AI: "Your profile has been successfully updated! I now have your details on file..."
```

### Task Creation and Management
```
User: "Please create a ticket to investigate new CRM options."
AI: "The ticket 'Investigate new CRM options' has been created with estimated time: 120 minutes..."
```

### Research and Information Gathering
```
User: "Can you find recent articles on AI in project management?"
AI: "Here's a summary of recent findings on AI in project management..."
```

### Memory and Context Management
```
User: "Add the point about AI-driven risk assessment to our research notes."
AI: "Research notes have been updated with the AI-driven risk assessment information..."
```

## 🏗️ Project Structure

```
manager-ai/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py                    # Main entry point
├── src/
│   ├── config/
│   │   └── settings.py        # Configuration and environment setup
│   ├── models/
│   │   └── schemas.py         # Pydantic models and type definitions
│   ├── tools/
│   │   └── search_tools.py    # Web, Wikipedia, and arXiv search tools
│   ├── memory/
│   │   └── memory_manager.py  # Memory management utilities
│   ├── nodes/
│   │   ├── action_nodes.py    # Main action and routing nodes
│   │   └── update_nodes.py    # Memory update nodes
│   ├── prompts/
│   │   └── system_prompts.py  # System prompts and templates
│   └── graph/
│       └── manager_graph.py   # Main graph construction and management
└── examples/
    └── example_usage.py       # Usage examples and demonstrations
```

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Required for the main language model
- `TAVILY_API_KEY`: Required for web search functionality
- `LANGSMITH_API_KEY`: Optional, for conversation tracing and debugging
- `LANGSMITH_TRACING`: Set to "true" to enable tracing
- `LANGSMITH_PROJECT`: Project name for LangSmith (default: "manager-ai")

### Model Configuration
The system uses Groq's `qwen-qwq-32b` model by default. You can modify this in `src/config/settings.py`:

```python
MODEL_NAME = "qwen-qwq-32b"
MODEL_TEMPERATURE = 0
```

## 🧠 How It Works

Manager AI uses a **state graph** architecture built with LangGraph:

1. **Input Processing**: User messages are analyzed to determine intent
2. **Action Decision**: The system decides whether to search for information, update memory, or respond directly
3. **Tool Execution**: Appropriate tools are called (search, memory updates, etc.)
4. **Memory Management**: Information is stored and retrieved from different memory types:
   - User Profile
   - Tickets/Tasks
   - Instructions
   - User Feedback
   - Product Research Notes
5. **Response Generation**: Contextual responses are generated based on available information

## 🔍 Memory System

Manager AI maintains several types of persistent memory:

- **User Profile**: Personal information, role, location, preferences
- **Tickets**: Tasks, deadlines, status, and solutions
- **Instructions**: User preferences for task management
- **User Feedback**: Collected opinions and sentiment
- **Product Research**: Market insights and competitive analysis

## 🛡️ Error Handling

The system includes robust error handling for:
- API failures and timeouts
- Invalid user inputs
- Missing environment variables
- Network connectivity issues
- Memory corruption or inconsistencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Groq](https://groq.com/) for fast inference
- Search capabilities provided by [Tavily](https://tavily.com/)
- Academic research integration via [arXiv](https://arxiv.org/)

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the [examples](examples/) directory for usage patterns
- Review the [documentation](docs/) for detailed information

---

**Manager AI** - Empowering leaders with intelligent assistance for better decision-making and project management.
