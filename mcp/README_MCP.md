MCP Integration Notes (Minimal Demo)

In this demo repo, MCP is treated as the control plane that:
- exposes tools (rag_search, schema_validate, rubric_score)
- orchestrates the sequence: route -> rag -> llm -> validate -> score -> (human gate)

For a first test, it's OK to run everything inside `engine.py` as a single process.
Then, migrate tool functions into an MCP server when you're ready.

Suggested MCP tools:
- rag.search(paths, query, k) -> list[{doc_id,title,text}]
- validate.schema(output, schema_path) -> {ok: bool, errors: []}
- validate.rubric(domain, output, rubric_path) -> {scores, total, flags, passed, needs_human_review}

Claude Agent SDK should call these tools via MCP rather than importing them directly.
