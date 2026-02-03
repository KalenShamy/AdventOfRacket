# Advent of Racket

An Advent of Code spinoff created as a closure piece for WPI's [CS 1102](https://wpi.cleancatalog.net/computer-science/cs-1102) course introducing functional programming with Racket.

To enforce the usage of Racket, users must submit their code in the browser (LeetCode style) and fix any problems until their solution passes all test cases.

Feel free to play at https://adventofracket.com/! You might even find it fun?

Built with Django, MongoDB, and hosted on Railway.

Homepage:<br>
<img src="images/AoR-Home.png" width=500>
<br><br>
Day 1 Part 1 Started:<br>
<img src="images/Day1-Start.png" width=500>
<br><br>
Day 1 Part 1 Initial Submit:
<br>
<img src="images/Day1-Submit.png" width=500>

Day 1 Part 1 Completed:
<br>
<img src="images/Day1-Complete.png" width=500>

## Help / Feedback

If you have any questions or want to get in touch, reach out:
- [GitHub Issues](https://github.com/KalenShamy/AdventOfRacket/issues)
- [Email](mailto:kalen.shamy@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/kalen-shamy/)
- [Discord](https://discord.com/users/835842638501511188)

## Local Installation Setup

If you want to get this up and running on your local machine, these instructions are as comprehensive as I can muster. No need to read all this if you know what you're doing.

> [!WARNING]
> Advent of Racket requires the [AoR Problem Manager](https://github.com/KalenShamy/AOR-Problem-Manager) service to run properly.

### Install dependencies
```bash
# python >= 3.12
pip install -r requirements.txt
```

### Build Command

You can also do this manually with the instructions for [Other](#Other) if you don't like the one-liner :)

#### MacOS (Arm)
```bash
curl -L https://mirror.racket-lang.org/installers/8.13/racket-8.13-aarch64-macosx-cs.dmg -o racket.dmg ; hdiutil attach racket.dmg ; hdiutil detach racket.dmg ; rm -rf ./RacketInstalls ; mkdir RacketInstalls ; mv "/Volumes/Racket v8.13/Racket v8.13" ./RacketInstalls/racket ; python manage.py collectstatic --noinput
```

#### Linux
```bash
curl -L https://mirror.racket-lang.org/installers/8.13/racket-8.13-x86_64-linux.sh -o racket.sh ; bash racket.sh --in-place --dest RacketInstalls/racket --create-dir ; python manage.py collectstatic --noinput
```

#### Windows
```bash
curl -L https://mirror.racket-lang.org/installers/8.13/racket-8.13-x86_64-win32-cs.exe -o racket.exe && racket.exe /S /D=%CD%\RacketInstalls\racket && python manage.py collectstatic --noinput
```

#### Other
1. Find the install right for your computer at https://mirror.racket-lang.org/installers/8.13/.
2. Move the contents to `./RacketInstalls/racket` such that `./RacketInstalls/racket/bin` and `./RacketInstalls/racket/collects` are accessible from the project root. 
3. Then, run:
```bash
python manage.py collectstatic --noinput
```

### Setup .env

1. Create your own random token for `AOR_MANAGER_ACCESS_TOKEN` to match the token in the AoR Problem Manager.
2. Create your own random token for `DJANGO_SECRET_KEY` as well for session token encryption.
3. Create a GitHub OAuth app using [these instructions](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) and paste your Client ID and Client Secret in `GITHUB_OAUTH_CLIENT_ID` and `GITHUB_OAUTH_CLIENT_SECRET`.
4. Create a MongoDB Cluster using [these instructions](https://www.mongodb.com/resources/products/fundamentals/clusters) and paste your connection string into `MONGODB_URI`. Make sure to create a database named `db_local` or change the value of `MONGODB_NAME`.

```
AOR_MANAGER_ACCESS_TOKEN="YOUR-TOKEN-1"
DJANGO_SECRET_KEY="django_secure_YOUR_SECRET_KEY"
GITHUB_OAUTH_CLIENT_ID="YOUR_CLIENT_ID"
GITHUB_OAUTH_CLIENT_SECRET="YOUR_CLIENT_SECRET"
MONGODB_NAME="db_local"
MONGODB_URI="mongodb+srv://YOUR_USER:YOUR_PASSWORD@cluster0.example.mongodb.net/"
```

### Setup AoR Problem Manager

Clone and setup [AoR Problem Manager](https://github.com/KalenShamy/AOR-Problem-Manager) using the README found in that repository.

Modify views.py on [line 20](https://github.com/KalenShamy/AdventOfRacket/blob/a085a2cbede6957fd4e8bad4bafa51303831245e/application/views.py#L20) to use:
```py
API_URL = "http://127.0.0.1:5000"
```

## Run Server

First, run the AoR Problem Manager using this command wherever you downloaded that repository:
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