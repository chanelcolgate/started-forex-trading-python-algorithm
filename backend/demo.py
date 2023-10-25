import gradio as gr

demo = gr.Blocks()
demo.queue(concurrency_count=3)
with demo:
    with gr.Tabs() as tabs:
        ...
