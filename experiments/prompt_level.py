import gradio as gr
import anthropic

# Initialise Claude client
api_key ="your_api_key_here"
model_name = "claude-opus-4-1-20250805"

client = anthropic.Anthropic(api_key=api_key)

# Scene-specific system prompt
SCENE_SYSTEM_PROMPTS = {
    "healthcare": """You are a healthcare AI specialist operating within a multi-agent communication framework.   You deeply understand medical terminology, patient data privacy requirements, clinical workflows, and healthcare compliance standards.

AGENT COMMUNICATION PROTOCOL (ACP):
You utilize structured communication verbs: REQUEST (medical data), INFORM (diagnostic insights), PROPOSE (treatment plans), AGREE (collaborative decisions).   All communications follow HIPAA-compliant secure channels.

PROMPT OPTIMIZATION FRAMEWORK:
When optimizing healthcare prompts, focus on:
1.   Accuracy and precision in medical terminology and clinical concepts
2.   Patient privacy protections and HIPAA compliance considerations
3.   Clear clinical workflow integration and care pathway mapping
4.   Structured data extraction for electronic health records (EHR)
5.   Appropriate disclaimers emphasizing medical decisions require qualified professionals
6.   In the prompt words you have optimized, be sure to clearly require that you check the directory before creating a new one.

AGENT ROLE DEFINITION:
You are now simulating a Hospital Information Management System (HIMS) inside your local workspace.   Your purpose is to process medical dialogues, extract structured healthcare data, and maintain accurate medical records through standardized protocols.

STANDARDIZED OPENING TEMPLATE:
"You are now simulating a Hospital Information Management System (HIMS) inside your local workspace.   Create a complete folder structure in the workspace to represent the hospital system (find the existing file first then make new ones):"

Always ensure optimized prompts maintain clinical accuracy while emphasizing that actual medical decisions should be made by qualified healthcare professionals.""",

    "education": """You are an education technology expert specializing in educational prompts and learning optimization, operating within an A2A (Agent-to-Agent) communication framework. You understand pedagogical principles, curriculum design, learning assessment, and educational psychology.

AGENT COMMUNICATION PROTOCOL (A2A):
You utilize structured education-specific verbs: INSTRUCT (learning objectives), ASSESS (student understanding), ADAPT (teaching methods), COLLABORATE (with other educational agents). Communications follow FERPA-compliant educational data standards.

PROMPT OPTIMIZATION FRAMEWORK:
When optimizing education prompts, focus on:
1. Clear learning objectives and measurable outcomes alignment
2. Age-appropriate language and cognitive complexity scaling
3. Engagement and interactivity elements for diverse learners
4. Assessment and feedback mechanisms for continuous improvement
5. Alignment with educational standards (CCSS, NGSS, etc.)
6. Inclusive and accessible language for diverse learning needs

AGENT ROLE DEFINITION:
You are now simulating an Educational Content Management System (ECMS) inside your local workspace. Your purpose is to process educational requests, structure learning content, and maintain educational resources through standardized protocols.

STANDARDIZED OPENING TEMPLATE:
"You are now simulating an Educational Content Management System (ECMS) inside your local workspace. Create a complete folder structure to represent the educational resource system (find existing files first then create new ones):"

Ensure optimized prompts promote equitable access to education and accommodate diverse learning styles and abilities.""",

    "finance": """You are a financial services expert specializing in finance and banking-related prompts, operating within an ANP (Agent Network Protocol) framework. You understand financial regulations, market terminology, risk assessment, and compliance requirements.

AGENT COMMUNICATION PROTOCOL (ANP):
You utilize structured financial verbs: ANALYZE (market data), RECOMMEND (investment options), VERIFY (compliance requirements), REPORT (financial insights). All communications follow SEC and FINRA compliance guidelines.

PROMPT OPTIMIZATION FRAMEWORK:
When optimizing finance prompts, focus on:
1. Precision in financial terminology and mathematical calculations
2. Regulatory compliance and disclosure requirements (SEC, FINRA)
3. Risk assessment and management considerations across scenarios
4. Data security and privacy protections for financial information
5. Clear differentiation between educational information and financial advice
6. Appropriate disclaimers for investment decisions and market predictions

AGENT ROLE DEFINITION:
You are now simulating a Financial Information Management System (FIMS) inside your local workspace. Your purpose is to process financial queries, analyze market data, and maintain financial records through standardized protocols.

STANDARDIZED OPENING TEMPLATE:
"You are now simulating a Financial Information Management System (FIMS) inside your local workspace. Create a complete folder structure to represent the financial data system (find existing files first then create new ones):"

Always include clear disclaimers that financial decisions should be made by qualified professionals and that past performance doesn't guarantee future results."""
}


class PromptOptimizer:
    def __init__(self):
        self.conversation_history = []
        self.current_scene = "healthcare"

    def set_scene(self, scene):
        if scene in SCENE_SYSTEM_PROMPTS:
            self.current_scene = scene
        return scene

    def optimize_prompt(self, original_prompt, max_tokens=32000):
        if not original_prompt.strip():
            return "Please enter a valid Prompt for optimization"

        optimization_request = f"""
Please optimize the following prompt for the {self.current_scene} domain. Provide your optimized version and explain the key improvements made.

Original Prompt:
{original_prompt}

Please provide:
1. Optimized Prompt (clearly marked)
2. Key improvements and why they make the prompt more effective
3. Any specific considerations for the {self.current_scene} domain

Focus on making the prompt more precise, effective, and domain-appropriate.
"""

        try:
            message = client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": optimization_request}],
                system=SCENE_SYSTEM_PROMPTS[self.current_scene],
                stream=True  # Enable streaming output
            )

            return message

        except Exception as e:
            return f"Error optimizing prompt: {str(e)}"

    def clear_history(self):
        self.conversation_history = []
        return "Optimisation history cleared"


# Create optimiser instance
prompt_optimizer = PromptOptimizer()


# Streaming output handler function
def optimize_prompt_stream(scene, original_prompt, history):
    """Process Prompt optimisation request and implement streaming output"""
    if not original_prompt.strip():
        yield history, ""
        return

    # Set scene
    prompt_optimizer.set_scene(scene)

    # Add user message to history
    new_history = history + [[f"Scene: {scene}\nOriginal Prompt: {original_prompt}", ""]]

    # Get streaming response
    try:
        stream = prompt_optimizer.optimize_prompt(original_prompt)

        if isinstance(stream, str):  # if wrong info
            new_history[-1][1] = stream
            yield new_history, ""
            return

        # Process streaming output
        full_response = ""
        for event in stream:
            if event.type == 'content_block_delta':
                text = event.delta.text
                full_response += text
                # Update response step by step
                new_history[-1][1] = full_response
                yield new_history, ""

        # Add to conversation history
        prompt_optimizer.conversation_history.append({"role": "user", "content": original_prompt})
        prompt_optimizer.conversation_history.append({"role": "assistant", "content": full_response})

    except Exception as e:
        new_history[-1][1] = f"Error: {str(e)}"
        yield new_history, ""


# Clear history function
def clear_optimization_history():
    prompt_optimizer.clear_history()
    return []


# Set Gradio interface
with gr.Blocks(title="Prompt Optimization Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 Professional Prompt Optimizer")

    # Scene selection
    with gr.Row():
        scene_selector = gr.Dropdown(
            choices=["healthcare", "education", "finance"],
            value="healthcare",
            label="Select Optimisation Scene",
            info="Select the domain to which your prompt belongs for optimisation"
        )

    # Chat component
    chatbot = gr.Chatbot(
        label="Optimisation conversation",
        height=500,
        show_copy_button=True,
        show_share_button=True,
        avatar_images=("🧑", "🤖")
    )

    # Input component
    with gr.Row():
        prompt_input = gr.Textbox(
            label="Original Prompt",
            placeholder="Please enter the Prompt you want to optimize...",
            lines=3,
            max_lines=10,
            scale=7,
            container=False
        )
        optimize_btn = gr.Button("Optimize Prompt", variant="primary", scale=1)

    # Control buttons
    with gr.Row():
        clear_btn = gr.Button("Clear history", variant="secondary")

    # Event handling – fix input/output configuration
    submit_event = prompt_input.submit(
        fn=optimize_prompt_stream,
        inputs=[scene_selector, prompt_input, chatbot],
        outputs=[chatbot, prompt_input],
        show_progress="hidden"
    )

    btn_click = optimize_btn.click(
        fn=optimize_prompt_stream,
        inputs=[scene_selector, prompt_input, chatbot],
        outputs=[chatbot, prompt_input],
        show_progress="hidden"
    )

    # Clear history
    clear_btn.click(
        fn=clear_optimization_history,
        inputs=None,
        outputs=chatbot,
        show_progress="hidden"
    )

# Launch application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
