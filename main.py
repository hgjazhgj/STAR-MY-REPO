import requests
import time


class Repo:
    def __init__(self, user, repo):
        self.data = requests.get(
            f'https://api.github.com/repos/{user}/{repo}'
        ).json()

    def stargazers(self):
        return {
            j['login']
            for i in range(1, self.data['stargazers_count']//100+2)
            for j in requests.get(
                f'{self.data["stargazers_url"]}?per_page=100&page={i}'
            ).json()
        }

    def forks(self):
        return {
            j['owner']['login']
            for i in range(1, self.data['forks']//100+2)
            for j in requests.get(
                f'{self.data["forks_url"]}?per_page=100&page={i}'
            ).json()
        }


def main(user, repo):
    with open('stargazers.dat') as f:
        star_old = set(f.read().splitlines())
    repo = Repo(user, repo)
    star_new = repo.stargazers()
    forks = repo.forks()
    with open('stargazers.dat', 'w') as f:
        f.write('\n'.join(star_new))
    with open(time.strftime(f'%Y-%m-%d_%H.%M.%S.md', time.localtime()), 'a') as f:
        CRLF = '  \n'
        f.write(f'''# Reoprt - STAR MY REPO!
## Add ({len(star_new-star_old)}):
{CRLF.join(star_new-star_old)}
## Remove ({len(star_old-star_new)}):
{CRLF.join(star_old-star_new)}
## Fork Without Star ({len(forks-star_new)}):
{CRLF.join(forks-star_new)}
''')


if __name__ == '__main__':
    main('hgjazhgj', 'FGO-py')
