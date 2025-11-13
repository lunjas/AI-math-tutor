# Quick Start Guide

Get started with AI Math Tutor in 5 minutes!

## Setup (First Time)

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# Edit .env and add your OpenAI API key
nano .env

# Activate virtual environment
source venv/bin/activate

# Run the tutor
python main.py
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
nano .env  # Add: OPENAI_API_KEY=sk-your-key-here

# Run the tutor
python main.py
```

## Your First Session

1. **Start the tutor:**
```bash
python main.py
```

2. **Ingest sample notes:**
```
📚 You: ingest sample_notes.md
```

3. **Ask a question:**
```
📚 You: What is the chain rule?
```

4. **Try symbolic math:**
```
📚 You: compute derivative x**3 + 2*x**2
```

5. **Generate practice problems:**
```
📚 You: quiz derivatives 3
```

## Essential Commands

| Command | Example | Purpose |
|---------|---------|---------|
| `ask` | `ask What is integration?` | Ask the tutor a question |
| `compute` | `compute solve x**2 - 4 = 0` | Symbolic math computation |
| `quiz` | `quiz calculus 5` | Generate practice problems |
| `ingest` | `ingest notes.pdf` | Add course materials |
| `stats` | `stats` | View knowledge base info |
| `help` | `help` | Show all commands |

## Example Workflow

```
# Start the tutor
python main.py

# Load your calculus notes
📚 You: ingest ~/Documents/calc_notes.pdf

# Ask conceptual questions
📚 You: Explain the fundamental theorem of calculus

# Verify calculations
📚 You: compute integral sin(x)

# Practice
📚 You: quiz integration by substitution 3

# Get help on a specific problem
📚 You: How do I find the derivative of sin(x^2)?

# Exit when done
📚 You: exit
```

## Tips

✅ **Do:**
- Ingest your course materials first for best results
- Ask follow-up questions to deepen understanding
- Use compute for exact mathematical verification
- Generate quizzes to practice

❌ **Avoid:**
- Running without setting OPENAI_API_KEY
- Asking questions before ingesting any documents
- Using incorrect SymPy syntax in compute commands

## Troubleshooting

**"OPENAI_API_KEY not set"**
→ Edit `.env` file and add your API key

**"No relevant materials found"**
→ Use `ingest` command to add documents first

**Virtual environment issues**
→ Make sure it's activated: `source venv/bin/activate`

**Import errors**
→ Reinstall dependencies: `pip install -r requirements.txt`

## What's Next?

1. Ingest your actual course materials (PDFs, notes)
2. Explore different types of questions
3. Use the quiz feature to test your knowledge
4. Try different symbolic math operations

## Need Help?

- Type `help` in the tutor for command reference
- Check `README.md` for detailed documentation
- Review `sample_notes.md` for example content

---

**Happy Learning! 🎓**

