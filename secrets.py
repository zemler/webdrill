import argparse
import requests
import re
from typing import List
from dataclasses import dataclass


@dataclass
class Secret:
    name: str
    content: str


@dataclass
class SecretMatcher:
    name: str
    r: str


@dataclass
class SecretsResult:
    url: str
    secret: Secret


class WebdrillSecrets:
    secret_matchers = [
        SecretMatcher(
            "ssh private key",
            r"BEGIN OPENSSH PRIVATE KEY-----[\nA-Za-z0-9/+=]+-----END OPENSSH PRIVATE KEY",
        )
    ]

    def __init__(self, urls: List[str]):
        self.urls = urls
        self.results: List[SecretsResult] = []

    def start(self):
        for url in self.urls:
            self.process_url(url)

    def process_url(self, url: str):
        r = requests.get(url)
        secrets = self.find_secrets(r.text)
        for secret in secrets:
            result = SecretsResult(url, secret)
            self.results.append(result)

    def find_secrets(self, content: str) -> List[Secret]:
        ret = []
        for matcher in self.secret_matchers:
            pattern = re.compile(matcher.r)
            matches = pattern.findall(content)
            for match in matches:
                ret.append(Secret(matcher.name, match))
        return ret

    def get_results_raw(self):
        return self.results

    def print_results_pretty(self):
        print(f"Found {len(self.results)} secrets")
        for result in self.results:
            print(f"Url: {result.url}, Type: {result.secret.name}")


def main():
    parser = argparse.ArgumentParser(description="Searches for secrets in given urls")
    parser.add_argument(
        "-u", "--urls-file", required=True, help="file with urls to check"
    )

    args = parser.parse_args()

    # get urls from file
    urls = []
    with open(args.urls_file, "r") as f:
        urls = [u for u in f.read().strip().split("\n")]

    w = WebdrillSecrets(urls)
    w.start()

    w.print_results_pretty()


if __name__ == "__main__":
    main()
