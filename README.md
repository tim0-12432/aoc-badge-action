# Advent of Code Badge GitHub Action

<div align="center">
  <a href="https://adventofcode.com/">
    <img width="50%" alt="AoC Badge" src="./aoc-badge.svg"/>
  </a>
</div>

## README adjustments

```html
<!-- START_AOC_BADGE -->

<!-- END_AOC_BADGE -->
```

## Example workflow

```yaml
name: Update AoC Badges
on:
  schedule: # runs scheduled
    - cron: '6 5 1-25 12 *' # 1. Dec - 25. Dec
    
  workflow_dispatch: # runs on manual dispatch 
  
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
          
      - uses: tim0-12432/aoc-badge-action@v0.1.3
        with:
          userid: 123456 # The user to track
          session: ${{ secrets.AOC_SESSION }} # secret containing the session cookie
          
#         Optional inputs:
#         
#         leaderboard: 123456 # The leaderboard to track; defaults to the users private leaderboard
#         file: './README.md' # The file to add the badges to; defaults to ./README.md
#         width: '30%'        # The width of the badge in the file; defaults to 50%

      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: Update AoC badge
          file_pattern: './README.md ./*.svg'
```
