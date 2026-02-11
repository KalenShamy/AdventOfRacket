# Advent of Racket

[![Live Site](https://img.shields.io/badge/play_now-adventofracket.com-maroon?style=for-the-badge)](https://adventofracket.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

An [Advent of Code](https://adventofcode.com/) spinoff created as a personal project applying WPI's [CS 1102](https://wpi.cleancatalog.net/computer-science/cs-1102) course introducing functional programming with Racket.

## Overview

Players solve 25 days of functional programming challenges in Racket using an in-browser code editor with syntax highlighting. Each problem is timed with a 30-second reading period letting you read the problem before the stopwatch starts. Solutions are validated against both public and hidden test cases, so you'll need to write good solutions that address the applicable edge cases. A competitive leaderboard ranks the fastest solvers across all days.

**[Play now at AdventOfRacket.com!](https://adventofracket.com/)**

## How It Works

Advent of Racket is built with **Django** and **MongoDB**, with a separate **[Problem Manager](https://github.com/KalenShamy/AOR-Problem-Manager)** API that stores all problem content.

### Architecture

<ul>
  <li style="list-style:none; position: relative;">
    <img src="https://cdn.simpleicons.org/django/000/fff" alt="Django" width=19 height=19 style="position: absolute; left: -27px; top:3px">
    <b>Frontend</b> — Django templates with the <a href="https://microsoft.github.io/monaco-editor/">Monaco Editor</a> (the engine behind VS Code) with custom Racket syntax highlighting providing an in-browser programming interface.
  </li>

  <li style="list-style:none; position: relative;">
    <img src="https://cdn.simpleicons.org/django/000/fff" alt="Django" width=19 height=19 style="position: absolute; left: -27px; top:3px">
    <b>Backend</b> — Django views handle authentication, leaderboard logic, problem loading from the API, submission processing, and test case validation.
  </li>

  <li style="list-style:none; position: relative;">
    <img src="https://cdn.simpleicons.org/racket/000/fff" alt="Racket" width=19 height=19 style="position: absolute; left: -27px; top:3px">
    <b>Code Execution</b> — A bundled <a href="https://racket-lang.org/">Racket</a> runtime running on backend executes user submissions in a <a href="https://docs.racket-lang.org/reference/Sandboxed_Evaluation.html">sandboxed</a> environment, blocking filesystem and network access with a 15-second timeout.
  </li>

  <li style="list-style:none; position: relative;">
    <img src="https://cdn.simpleicons.org/mongodb/000/fff" alt="MongoDB" width=19 height=19 style="position: absolute; left: -27px; top:3px">
    <b>Database</b> — MongoDB Atlas stores user accounts, problem sessions, submission history, and leaderboard data via <a href="https://mongoengine.org/">MongoEngine</a>.
  </li>

  <li style="list-style:none; position: relative;">
    <img src="https://cdn.simpleicons.org/flask/000/fff" alt="Flask" width=19 height=19 style="position: absolute; left: -27px; top:3px">
    <b>Problem Manager API</b> — A separate API serving test cases, starter code, and Markdown problem descriptions exclusively to requests using a valid authentication token - designed only to be accessed by this program's backend.
  </li>

  <li style="list-style:none; position: relative;">
    <img src="https://cdn.simpleicons.org/railway/000/fff" alt="Railway" width=19 height=19 style="position: absolute; left: -27px; top:2px">
    <b>Hosting</b> — Deployed on <a href="https://railway.app/">Railway</a> with Gunicorn as the WSGI server and WhiteNoise for static file serving.
  </li>
</ul>

### Usage Flow

1. **Login** — Players log in with their GitHub account and are redirected back to the site.
2. **Select a Problem** — Users choose one of the available days on the advent calendar, opening a page displaying the problem description, starter code, and test cases fetched from the Problem Manager API.
3. **Reading Period** — Each problem starts with a 30-second reading window where the editor is locked, giving the user time to read before the timer starts.
4. **Code & Submit** — Users write their Racket solution and click Run. The backend wraps the code in Racket's [built-in sandbox](https://docs.racket-lang.org/reference/Sandboxed_Evaluation.html), connects test cases, and executes it with a 15-second timeout.
5. **Validation** — Outputs are compared against expected values for both public and hidden test cases. The tests window displays the result of each test as pass/fail (and any errors that might have occurred) without page reloads.
6. **Completion** — When all tests pass, their solve time is recorded, they earn a star, and they advance to Part 2. After completing the Part 2 problem (earning a second star), they are returned back to the main page to see their progress on the advent calendar.

### Scoring

The AoR leaderboard system is modeled after AoC's:

Problems award one star per part solved. The daily leaderboard ranks players by solve time. For each problem and part, players earn **10 points** for ranking 1st place, **9 points** for 2nd, and so on down to **1 point** for 10th. Players score **0 points** for ranking below 10th on any part. The overall leaderboard sums each user's total points across all days and displays the top 20 sorted in descending order.

## Screenshots

<details open>
<summary><strong>Homepage</strong></summary>
<br>
<img src="images/AoR-Home.png" width="600" alt="Advent of Racket Homepage">
</details>

<details>
<summary><strong>Problem View</strong></summary>
<br>
<img src="images/Day1-Start.png" width="600" alt="Day 1 Part 1 - Problem started">
</details>

<details open>
<summary><strong>Submitting a Solution</strong></summary>
<br>
<img src="images/Day1-Submit.png" width="600" alt="Day 1 Part 1 - Initial submission">
</details>

<details>
<summary><strong>Completed Problem</strong></summary>
<br>
<img src="images/Day1-Complete.png" width="600" alt="Day 1 Part 1 - Completed">
</details>

## Contact

Have questions or feedback? Reach out through any of these channels:

- [GitHub Issues](https://github.com/KalenShamy/AdventOfRacket/issues)
- [Email](mailto:kalen.shamy@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/kalen-shamy/)

## Local Development

> [!WARNING]
> Advent of Racket requires the [AoR Problem Manager](https://github.com/KalenShamy/AOR-Problem-Manager) service to run properly. Set that up first.

### Prerequisites

- Python 3.12+
- MongoDB cluster ([setup guide](https://www.mongodb.com/resources/products/fundamentals/clusters))
- GitHub OAuth app ([setup guide](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app))

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Racket

Choose your platform below, or see [Manual Installation](#manual-installation) for other systems.

<details>
<summary><strong>macOS (Apple Silicon)</strong></summary>

```bash
curl -L https://mirror.racket-lang.org/installers/8.13/racket-8.13-aarch64-macosx-cs.dmg -o racket.dmg && \
  hdiutil attach racket.dmg && \
  rm -rf ./RacketInstalls && mkdir RacketInstalls && \
  mv "/Volumes/Racket v8.13/Racket v8.13" ./RacketInstalls/racket && \
  hdiutil detach "/Volumes/Racket v8.13" && \
  rm racket.dmg && \
  python manage.py collectstatic --noinput
```
</details>

<details>
<summary><strong>Linux (x86_64)</strong></summary>

```bash
curl -L https://mirror.racket-lang.org/installers/8.13/racket-8.13-x86_64-linux.sh -o racket.sh && \
  bash racket.sh --in-place --dest RacketInstalls/racket --create-dir && \
  rm racket.sh && \
  python manage.py collectstatic --noinput
```
</details>

<details>
<summary><strong>Windows</strong></summary>

```bash
curl -L https://mirror.racket-lang.org/installers/8.13/racket-8.13-x86_64-win32-cs.exe -o racket.exe && \
  racket.exe /S /D=%CD%\RacketInstalls\racket && \
  del racket.exe && \
  python manage.py collectstatic --noinput
```
</details>

<details>
<summary><strong>Manual Installation</strong></summary>

1. Download the appropriate installer from [mirror.racket-lang.org/installers/8.13](https://mirror.racket-lang.org/installers/8.13/)
2. Install Racket into `./RacketInstalls` so that the following paths exist from the project root:
    ```
    ├─ AdventOfRacket/
    ├─ application/
    ├─ images/
    ├─ RacketInstalls/racket/
    │  ├─ bin
    │  ├─ collects
    │  │ ...
    ```
3. Run:
   ```bash
   python manage.py collectstatic --noinput
   ```
</details>

### 3. Setup .env

Fill this env template with your GitHub OAuth app and MongoDB Cluster information. `AOR_MANAGER_ACCESS_TOKEN` can be any random string matching the token in your setup of the Problem Manager API.

```
AOR_MANAGER_ACCESS_TOKEN="YOUR-TOKEN-1"
DJANGO_SECRET_KEY="django_secure_YOUR_SECRET_KEY"
GITHUB_OAUTH_CLIENT_ID="YOUR_CLIENT_ID"
GITHUB_OAUTH_CLIENT_SECRET="YOUR_CLIENT_SECRET"
MONGODB_NAME="db_local"
MONGODB_URI="mongodb+srv://YOUR_USER:YOUR_PASSWORD@cluster0.example.mongodb.net/"
```

### 4. Setup AoR Problem Manager

Clone and setup [AoR Problem Manager](https://github.com/KalenShamy/AOR-Problem-Manager) using the README found in that repository.

Modify views.py on [line 20](https://github.com/KalenShamy/AdventOfRacket/blob/a085a2cbede6957fd4e8bad4bafa51303831245e/application/views.py#L20) to use:
```py
API_URL = "http://127.0.0.1:5000"
```

### 5. Run Server

First, run the Problem Manager API using this command wherever you downloaded that repository:
```bash
python app.py
```

Then, run the Advent of Racket server using this command:
```bash
python manage.py runserver
```

Enjoy!

## License
All files are licensed under [MIT](LICENSE), except as clarified below.

This repository is an independent, unofficial project. No Advent of Code problem descriptions, solutions, inputs, or other proprietary materials have been intentionally copied or included.

Any content that may constitute the intellectual property of Advent of Code remains the property of Advent of Code and is not covered by the MIT License.