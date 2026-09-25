# AI and agent interfaces

The surfaces an agent product needs — streaming text, reasoning, tool calls, approvals, citations, artifacts, voice, workflow canvas — are now solved by several competing kits. Pick **one** and stay in it; these overlap heavily and mixing them produces inconsistent chrome.

## Choosing

| Situation | Take |
|---|---|
| Using the Vercel AI SDK, or want the widest component surface | **AI Elements** |
| Need runtime/backend plumbing as well as components (LangGraph, MCP, threads, persistence) | **assistant-ui** |
| Want small, tasteful primitives you fully own, no framework opinion | **prompt-kit** |
| Voice or audio agent | **ElevenLabs UI** or **@agents-ui** (LiveKit) |
| Building a ChatGPT App | **Manifest UI** |

## AI Elements (Vercel) — `@ai-elements`

77 registry items, built on shadcn/ui conventions. The broadest coverage of the four:

- **Chatbot** — Attachments, Chain of Thought, Checkpoint, Confirmation, Context, Conversation, Inline Citation, Message, Model Selector, Plan, Prompt Input, Queue, Reasoning, Shimmer, Sources, Suggestion, Task, Tool
- **Code** — Agent, Artifact, Code Block, Commit, Environment Variables, File Tree, JSX Preview, Package Info, Sandbox, Schema Display, Snippet, Stack Trace, Terminal, Test Results, Web Preview
- **Voice** — Audio Player, Mic Selector, Persona, Speech Input, Transcription, Voice Selector
- **Workflow** — Canvas, Connection, Controls, Edge, Node, Panel, Toolbar

Docs at `elements.ai-sdk.dev`. Advertises deep AI SDK integration: streaming, status states, type safety.

## assistant-ui — `@assistant-ui`

148 registry items, and the only one that also gives you the runtime layer. Pre-1.0 (v0.x) but has a published deprecation policy and migration guides.

Primitives: Thread / ThreadList (multi-thread switching), Message / MessagePart (text, tool calls, reasoning, data parts), Composer (attachments, mentions, slash commands, model picker, dictation), ActionBar (copy, edit, reload, speech, feedback), BranchPicker (navigating regenerated responses), ChainOfThought, AssistantModal (floating popover), Attachment, Suggestion, Error, SelectionToolbar.

Runtimes: Vercel AI SDK (v4–v7), LangGraph (streaming, interrupts, agent state, generative UI), LangChain, Google ADK, A2A, AG-UI, Mastra, Cloudflare Agents, OpenCode, Claude managed agents, plus custom (LocalRuntime, ExternalStoreRuntime). Non-web targets: React Native, **React Ink (terminal)**, Vue, Electron.

Also: MCP support including MCP Apps in sandboxed iframes, and renderers that convert generative UI into Slack Block Kit and Teams Adaptive Cards.

## prompt-kit — [prompt-kit.com](https://www.prompt-kit.com)

AI-interface primitives by ibelick (the author of Motion Primitives): prompt box, thinking steps, message parts. Small, no runtime opinion. The right choice when you want to own the code rather than adopt a framework.

## Voice and realtime

- **`@elevenlabs-ui`** — orbs, waveforms, audio and agent UI
- **`@agents-ui`** (LiveKit) — control bar, voice and video agent interfaces, 17 items

## Others worth knowing

`@manifest` (32 items, components for ChatGPT Apps) · `@agentcn` (agent recipes) · `21st.dev Agent Elements` (chat shell, tool-call cards) · `LocalMode` (147 items, local-first: chat, RAG) · `@aicanvas` (126 items) · [Balsa UI](https://balsa-ui.com) (agent-native library) · [aicss.dev](https://www.aicss.dev) (14 copy-paste blocks for thinking states, tool calls, approval cards).

## Design notes specific to agent UIs

- **Streaming needs a shape, not just text.** Reasoning, tool calls and final answers must be visually distinct or the user cannot tell what the agent is doing versus what it concluded.
- **Approval and confirmation cards are the safety surface.** They must state what will happen, and be impossible to trigger by reflex.
- **Latency is the interface.** Thinking states, shimmer and progressive disclosure are not decoration; they are what makes a slow agent feel alive. [FeralUI](https://feralui.dev) exists specifically for this "handfeel".
- **Tool output is arbitrary content.** Budget for code blocks, diffs, tables, file trees, terminals and images from the start — retrofitting them is worse than building them in.
