# make-lstm-great-again
This project aims to artificially recreate Donald Trump's very unique and peculiar tweeting style.
It uses the Twitter API to fetch the aforementioned tweets, and a LSTM recurrent neural network to generate new content matching the style of this dataset.

## Twitter Scraper
Fetch the tweets from a given twitter handle.

## Installation

```
pip install -r requirements.txt
```

### Usage

```
Usage:
  twitter_scraper.py <handle> [-o <file>] [-c <n>]
                              [--include_retweets]
                              [--delay <seconds>]
                              [--token <t>]
                              [--encoding <e>]
  twitter_scraper.py -h | --help

Options:
  -h --help
  -o <file> --output <file>  Output file [default: tweets.txt]
  -c <n> --count <n>         Number of tweets fetched [default: 500]
  --include_retweets         Include retweets in the result
  --delay <seconds>          Delay between two API calls [default: 30]
  --token <t>                Token appended at the end of each tweet [default: \EOT]
  --encoding <e>             Encoding used when saving the tweets [default: utf-8]
```

### Configuration
The Twitter API authentification step has to be configured via a `config.json` file
holding the following dictionary:
```
{
    "consumer_key":"<consumer_key>",
    "consumer_secret":"<consumer_secret>",
    "access_token":"<access_token>",
    "access_token_secret":"<access_token_secret>"
}
```
### Example

```bash
# Quickly fetch most of Donald Trump's tweets
$ python twitter_scraper.py realDonaldTrump -c 34000 --delay 2
```

## LSTM
Automatic generation of text similar to a given input document.

### Usage

```
Usage:
  lstm.py train [-i <file>] [--maxlen <l>]
                [--checkpoint_path <p>] [--no_autoload]
  lstm.py generate [-o <file>]
                   [-c <n>] [--maxlen <l>] [--temperature <T>]
  lstm.py -h | --help

Options:
  -h --help
  -i <file> --input <file>   Input text file [default: input.txt]
  -o <file> --output <file>  Output generated file [default: output.txt]
  -c <n> --count <n>         Number of characters generated [default: 1000]
  --maxlen <l>               Maximum length of sequences [default: 20]
  --temperature <T>          Novelty in the generation, usually between 0. and 2.
                             If not provided, output will be generated with
                             several temperatures [default: 1.0]
  --checkpoint_path <p>      Name of the model snapshots that will be saved at
                             each checkpoint. [default: model-save]
  --no_autoload              Do not load the last saved checkpoint model even
                             if it exists
```

### Example

```bash
# Train a LSTM on previously fetched tweets
$ python lstm.py train -i tweets.txt
```

```bash
# Generate about 100 brand new Donald Trump's tweets from trained model
$ python lstm.py generate -i tweets.txt -c 14000
```
