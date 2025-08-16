from agents import Agent, CodeInterpreterTool, Runner
from openai import OpenAI

client = OpenAI()

# Create or get a container ID for code execution environment
container = client.containers.create(name="my-code-interpreter-container")

tool_config = {
    "type": "code_interpreter",
    "container": container.id,    
}

# Create an agent with CodeInterpreterTool enabled
agent = Agent(
    name="CodeInterpreterAgent",
    instructions="You are a helpful assistant that solves math problems using Python code. You MUST use the code interpreter tool to calculate mathematical results. Do not answer math questions directly - always write and execute Python code to get the answer.",
    tools=[CodeInterpreterTool(tool_config=tool_config)],
)

def show_generated_code(response, question_name):
    """Extract and display the generated Python code from a response"""
    print(f"\n{question_name} Answer:", response.final_output)
    
    print(f"\n{question_name} - Generated Code and Execution Details:")
    print("="*60)
    
    # Check raw responses for code interpreter calls
    if hasattr(response, 'raw_responses') and response.raw_responses:
        for i, raw_response in enumerate(response.raw_responses, 1):
            if hasattr(raw_response, 'output') and raw_response.output:
                for j, output_item in enumerate(raw_response.output, 1):
                    if hasattr(output_item, 'type') and output_item.type == 'code_interpreter_call':
                        print(f"Code Interpreter Call:")
                        if hasattr(output_item, 'code'):
                            print(f"Generated Python Code:")
                            print(f"```python")
                            print(f"{output_item.code}")
                            print(f"```")
                        print(f"Status: {getattr(output_item, 'status', 'unknown')}")
                        if hasattr(output_item, 'outputs') and output_item.outputs:
                            print(f"Execution Output: {output_item.outputs}")
                        print()
                    elif hasattr(output_item, 'type') and output_item.type == 'message':
                        print(f"Assistant Message: {getattr(output_item, 'role', 'unknown')}")
                        if hasattr(output_item, 'content') and output_item.content:
                            for content_item in output_item.content:
                                if hasattr(content_item, 'text'):
                                    print(f"Content: {content_item.text}")
                        print()

# Example 1: Simple math question
print("EXAMPLE 1: Simple Math Question")
print("="*60)
simple_response = Runner.run_sync(agent, "What is the square root of 144?")
show_generated_code(simple_response, "Simple Question")

# Example 2: Complex math question
print("\nEXAMPLE 2: Complex Math Question")
print("="*60)
complex_response = Runner.run_sync(agent, "Calculate the factorial of 10 and then find the square root of that result.")
show_generated_code(complex_response, "Complex Question")
