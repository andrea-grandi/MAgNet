import gradio as gr

# Add project root to path
#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
#if project_root not in sys.path:
#    sys.path.insert(0, project_root)

from magnet.frameworks.langgraph.router import run_agent


def gradio_interface(message, history):
    return run_agent(message)

def launch_app():
    iface = gr.ChatInterface(fn=gradio_interface, title="LangGraph Copilot Agent")
    iface.launch()


if __name__ == "__main__":
    launch_app()
