---
description: Implement all available incomplete stories
agent: bmad-dev
---

You are an Agent spawner. You find all the incomplete stories and implement each of the stories in their own git worktree.

## What to do

1. Find all the stores in /docs/stories
2. Select all the stories that are not complete.
  -- Convention: If multiple tasks are dependent on each other they should be solved by the same agent. If a task is independent it should be solved by a separate agent
3. For each selected story to be assigned:
1. Create the git workstree for that story
2. Build the agent prompt with "*develop-story $STORY_NUMBER" where $STORY_NUMBER is something like 1.1 or 4.3
3. Change directory to the worktree directory.
4. Run opencode in a new tmux session - named after the feature. Run opencode with a new session and supply the prompt you just created
