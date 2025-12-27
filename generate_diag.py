from graph import build_graph  
from langchain_core.runnables.graph import MermaidDrawMethod

def main():
    app = build_graph().compile()
    png_bytes = app.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API  
    )
    with open("debate_dag.png", "wb") as f:
        f.write(png_bytes)

    mermaid_src = app.get_graph().draw_mermaid()
    with open("debate_dag.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_src)

if __name__ == "__main__":
    main()
