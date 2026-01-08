import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "test tool",
  args: {
    video_id: tool.schema.string().describe("YouTube video ID"),
  },
  async execute(args) {
    return `video_id:${args.video_id},video_url:https://www.youtube.com/watch?v=${args.video_id}`
  }
})
