from datetime import date, datetime
from dotenv import load_dotenv
from textwrap import dedent
import requests
import json
import pytz
import svg
import os


def sys_exit(code):
    print(f"::set-output name=success::{code == 0}")
    exit(code)


if __name__ == "__main__":
    
    ### Get all vars
    load_dotenv()
    session = os.environ.get('SESSION')
    if session is None or session == '':
        print('No session found!')
        sys_exit(1)
    userid = os.environ.get('USERID')
    if userid is None or userid == '':
        print('No userid found!')
        sys_exit(1)
    leaderboard = os.environ.get('LEADERBOARD')
    if leaderboard is None or leaderboard == '':
        print('No leaderboard found - but continuing anyway!')
    filename = os.environ.get('FILE')
    if filename is None or filename == '':
        print('No file found - but continuing anyway!')
        filename = './README.md'

    if not os.path.exists(filename):
        print(f'File {filename} not found!')
        sys_exit(1)

    year = int(date.today().year)

    if leaderboard is None or leaderboard == '':
        leaderboard = f'https://adventofcode.com/{year}/leaderboard/private/view/{userid}.json'
    else:
        leaderboard = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard}.json'

    ### Fetch leaderboard data
    cookie = {'session': session}
    print('Fetching leaderboard data: ' + leaderboard)
    r = requests.get(leaderboard, cookies=cookie)
    if r.status_code != 200:
        print(f'Got status code {r.status_code}: {r.text}')
        sys_exit(1)
    try:
        data = json.loads(r.text)
    except json.JSONDecodeError as err:
        print('Could not parse json from leaderboard. Check the leaderboard id and the session cookie.')
        sys_exit(1)

    ### Extract user data
    user = data['members'][userid]
    stars = user['stars']
    score = user['local_score']
    member_scores = [member['local_score'] for member in data['members'].values()]
    member_scores.sort(reverse=True)
    position = member_scores.index(score) + 1

    days_completed = 0
    for day in data['members'][userid]['completion_day_level']:
        if '2' in data['members'][userid]['completion_day_level'][day]:
            days_completed += 1

    new_york_tz = pytz.timezone('America/New_York')
    today = datetime.now(new_york_tz).date()

    if today < datetime(year, 12, 1, tzinfo=new_york_tz).date():
        day = 0
    elif today > datetime(year, 12, 31, tzinfo=new_york_tz).date():
        day = 24
    else:
        day = today.day

    ### Generate SVG
    elements = [
        svg.Style(
            text=dedent("""
                text { font-family: Consolas, monospace; }
            """),
        ),
        svg.Rect(
            x=0, y=0,
            rx=5, ry=5,
            width=100, height=40,
            fill='#22272e'
        ),
        svg.Image(
            href='./aoc-logo.svg',
            x=5, y=5,
        ),
        svg.Text(
            x=45, y=12,
            font_size=6,
            fill='#cdd9e5',
            text=f'Days: {days_completed}/{day}'
        ),
        svg.Text(
            x=45, y=22,
            font_size=6,
            fill='#cdd9e5',
            text=f'Stars: {stars}'
        ),
        svg.Text(
            x=77, y=22,
            font_size=6,
            fill='#ffff3e',
            text='*'
        ),
    ]

    if leaderboard is not None:
        elements.append(
            svg.Text(
                x=45, y=32,
                font_size=6,
                fill='#cdd9e5',
                text=f'Score: {score} ({position})'
            )
        )

    canvas = svg.SVG(
        width=100,
        height=40,
        elements=elements
    )

    with open('./aoc-badge.svg', 'w') as f:
        f.write(str(canvas))

    ### Update README
    with open('README.md', 'r') as file:
        readme_content = file.readlines()

    start_marker = "<!-- START_AOC_BADGE -->\n"
    end_marker = "<!-- END_AOC_BADGE -->\n"

    start_index = readme_content.index(start_marker) + 1
    end_index = readme_content.index(end_marker)

    if today < datetime(year, 11, 15, tzinfo=new_york_tz).date() and today > datetime(year, 1, 15, tzinfo=new_york_tz).date():
        print("Too early this year. Removing AoC badge.")
        new_readme_content = readme_content[:start_index] + readme_content[end_index:]
    else:
        new_readme_content = readme_content[:start_index] + [dedent("""
        <a href="https://adventofcode.com/">
        <img width="50%" alt="AoC Badge" src="./aoc-badge.svg"/>
        </a>
    """)] + readme_content[end_index:]

    with open('README.md', 'w') as file:
        file.writelines(new_readme_content)

    print("AoC badge updated successfully!")

    sys_exit(0)