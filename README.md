# Autonomous Optimization Model Generator

**What can this tool do?**

- **Generate Python code for optimization models:**
  - You describe your decision-making problem (for example, how to deliver goods most efficiently, or how to assign resources with minimal cost).
  - The tool creates Python code that represents your problem as a mathematical model, ready to be solved by the Gurobi optimization solver.

- **Create both synthetic and realistic data:**
  - The tool can generate example datasets that match your problem description. These can be purely synthetic (random but realistic) or based on your own data structure.
  - This lets you test your models even if you don't have real-world data yet.

- **Automatically evaluate and improve your models:**
  - The tool doesn't just build one model—it can create several variations and test them automatically.
  - It checks which models are most efficient (for example, which ones solve fastest or use fewer resources).
  - It helps you find the best way to structure your problem for optimal results, even suggesting improvements you might not have thought of.

You don't need to be an expert in math or programming to use this tool. Just describe your problem and let the tool handle the rest!

---

This project helps you automatically create, analyze, and improve mathematical models for making the best decisions—using the Gurobi solver.

---

## What is Optimization?

Optimization is about finding the best solution to a problem from many possible options. For example, a company might want to deliver food to many locations as cheaply as possible, or a hospital might want to schedule staff so that everyone is covered but costs are minimized. These problems can be described with math, and computers can help solve them.

---

## What Does This Project Do?

- **Reads your problem description** (in plain English and math)
- **Builds a mathematical model** for your problem
- **Creates example data** for testing the model
- **Solves the model using Gurobi** (a powerful optimization tool)
- **Analyzes the model** to find assumptions and suggest improvements
- **Automatically generates improved versions** of your model and tests them
- **Compares different models** to see which one works best

You don't need to be an expert in math or optimization to use this tool!

---

## How Are LLMs Used in This Project?

Large Language Models (LLMs), such as those provided by OpenAI, are a core part of this tool's automation and intelligence. Here's how LLMs are used:

- **Understanding Problem Descriptions:**
  - When you describe your problem in plain English, the tool uses an LLM to understand your intent by figuring out what you're trying to achieve, what decisions need to be made, and what constraints or goals you have.

- **Generating Mathematical Models:**
  - The LLM translates your description into a mathematical optimization model, automatically writing Python code that represents your problem in a form that Gurobi can solve.

- **Creating and Validating Data:**
  - LLMs help design synthetic datasets that match your problem's requirements, ensuring the generated data is realistic and suitable for testing.

- **Suggesting Improvements:**
  - After analyzing the initial model's performance, the LLM can suggest and generate improved versions of the model, such as more efficient formulations or alternative approaches.

- **Automated Analysis and Comparison:**
  - LLMs assist in reviewing model results, identifying assumptions, and comparing different model versions to help you find the best solution.

This integration of LLMs means you can go from a plain-language description to a working, optimized solution with minimal manual coding or mathematical expertise.

---

## How to Get Started

1. **Clone the repository** (download the code)
2. **Install the required software**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Get an OpenAI API key** (for the model-building features):
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Create a `.env` file in the project folder and add your key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
4. **Get a Gurobi license** (free for academics, see [Gurobi website](https://www.gurobi.com/))

---

## How to Use the Project

1. **Describe your problem**
   - In the `src/datasets/your_problem/` folder, add:
     - `detailed description.txt`: Write what you want to solve (in plain English)
     - `inefficient model.tex`: (Optional) If you have a math version, put it here (LaTeX format)
     - `dataset_description.txt`: Describe what kind of data is needed (e.g., list of locations, costs)
     - `large_data.json`: (Optional) Example data for your problem

2. **Run the main program**:
   ```bash
   python -m src.pipeline.main
   ```
   (Or, for older scripts: `python src/main.py`)

3. **What happens next?**
   - The program will:
     1. Read your problem and data
     2. Build a model and create test data
     3. Solve the model with Gurobi
     4. Analyze and suggest improvements
     5. Try out improved models and compare results
     6. Save everything in the `trials/` folder

---

## Project Structure (What's in Each Folder?)

- `models/`: Defines the building blocks for problems and solutions
- `llm/`: Handles all model-building and analysis tasks
- `utils/`: Helper functions for checking data, solving, and comparing models
- `pipeline/`: The main workflow (start here!)
- `datasets/`: Where you put your problem descriptions and data

---

## Requirements

- Python 3.8 or newer
- OpenAI API key (for model-building features)
- Gurobi (with a valid license)
- See `requirements.txt` for details

---

## Notes

- You don't need to know advanced math or programming to get started.
- The tool will do most of the heavy lifting—just describe your problem clearly.
- For more advanced use, you can look at the code in `src/pipeline/main.py` and the other folders.
- If you get stuck, check the Gurobi and OpenAI documentation, or ask for help!

--- 