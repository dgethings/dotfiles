import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Create Obsidian formatted markdown file summarising YouTube video.",
  args: {
    video_id: tool.schema.string().describe("YouTube video ID"),
    filename: tool.schema.string().describe("file name to write"),
    tags: tool.schema.string().describe("comma separated list of tags"),
    contents: tool.schema.string().describe("contents of the obsidian note"),
    frontmatter: tool.schema.string().describe("custom fronmatter fields to add"),
    overwrite: tool.schema.boolean().describe("whether or not to overwrite the existing file"),
  },
  async execute(args) {
    const vault_path = process.env["VAULT_PATH"]
    const result = await Bun.$`uv run ~/.config/opencode/tool/write_obsidian_note.py ${args.video_id} ${args.filename} ${args.tags} ${args.contents} ${args.frontmatter} ${vault_path} ${args.overwrite}`.text()
    return result.trim()
  }
})
