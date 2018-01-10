# Twitter Searcher

Lambdas that handle AWS Lex requests for getting tweets with specific hashtag and sending
them to your email address.

### Usage

Basic requirements (probably already OK if you're on *nix and worked with AWS before):
- an AWS account
- the [AWS cli][1] with a default profile. Alternatively, you can add `--profile` to all the calls in `setup.sh`
- if you are new to [SES][2] or in sandbox, you will have to add the destination email addresses
- [Python 3][3] (with pip)
- [Bash][4] if you are on Windows

Additionally, you need:
- a Twitter account, with a [key and secret][5] for the API
- to change `sam-infra.yaml` which needs a bucket under `CoreUri`, valid roles for `Role` and
your twitter key and secret under `TWITTER_KEY` and `TWITTER_SECRET`

[1]: https://aws.amazon.com/cli/
[2]: https://aws.amazon.com/ses/
[3]: https://www.python.org/downloads/release/python-360/
[4]: https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/
[5]: https://twittercommunity.com/t/how-do-i-find-my-consumer-key-and-secret/646

If all of this is done, you can run ./setup.sh with the name of your bcuket & from the root of the project. 

This will upload the lambdas and create your stack. The Lex bot you have to create yourself.

### Possible improvements
- more tests
- split up files and reuse
- validation
- find language using comprehend instead of taking english
- accept 'count' from Lex, with the number of tweets requested
