import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Create JSON file contain metadata from YouTube video. Accepts either a URL or video ID as an argument",
  args: {
    video_id: tool.schema.string().describe("YouTube URL or video ID"),
  },
  async execute(args) {
    const result = await Bun.$`uv run ~/.config/opencode/tool/youtube_metadata.py ${args.video_id}`.text()
    return result.trim()
  }
})
