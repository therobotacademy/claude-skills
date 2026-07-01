@echo off
set ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
set ANTHROPIC_AUTH_TOKEN=sk-cp-Mk7b15k6Hu85YVe-UKRL8-PBFyLQ6uaS67K5wtsX4FD5mqDvUqhN_Kw4fRkkGeIi0U7TAsWe0Ayo6XT1_2prHKmF-AMrVIZi071FtHBUEVcHUJ7P65-XVV0

set ANTHROPIC_DEFAULT_HAIKU_MODEL=minimax/minimax-m2.5-lightning
set ANTHROPIC_DEFAULT_SONNET_MODEL=minimax/minimax-m2.7

set ANTHROPIC_DEFAULT_OPUS_MODEL=MiniMax-M3[1m]
set ANTHROPIC_MODEL=MiniMax-M3[1m]
set CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000

echo Claude Code con MiniMax-M3
echo.

claude --model MiniMax-M3[1m]
