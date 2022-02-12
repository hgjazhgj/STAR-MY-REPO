import os
import time

import requests


class Repository:
    def __init__(self, user, repo):
        self.data = requests.get(
            f'https://api.github.com/repos/{user}/{repo}'
        ).json()

    def stargazers(self):
        return {
            j['login']
            for i in range(1, (self.data['stargazers_count']-1)//100+2)
            for j in requests.get(
                f'{self.data["stargazers_url"]}?per_page=100&page={i}'
            ).json()
        }

    def forks(self):
        return {
            j['owner']['login']
            for i in range(1, (self.data['forks']-1)//100+2)
            for j in requests.get(
                f'{self.data["forks_url"]}?per_page=100&page={i}'
            ).json()
        }


def main(user, repo):
    if os.path.isfile(f'{user}_{repo}.dat'):
        with open(f'{user}_{repo}.dat') as f:
            star_old = set(f.read().splitlines())
    else:
        star_old = set()
    repository = Repository(user, repo)
    star_new = repository.stargazers()
    forks = repository.forks()
    with open(f'{user}_{repo}.dat', 'w') as f:
        f.write('\n'.join(star_new))
    with open(time.strftime(f'%Y-%m-%d_%H.%M.%S.md', time.localtime()), 'a') as f:
        CRLF = '  \n'
        f.write(f'''# Reoprt - {user}/{repo} - STAR MY REPO!
## Add ({len(star_new-star_old)}):
{CRLF.join(star_new-star_old)}
## Remove ({len(star_old-star_new)}):
{CRLF.join(star_old-star_new)}
## Fork Without Star ({len(forks-star_new)}):
{CRLF.join(forks-star_new)}
''')


if __name__ == '__main__':
    main('<user>', '<repo>')
