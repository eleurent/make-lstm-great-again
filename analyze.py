import matplotlib.pyplot as plt
import re
from collections import Counter

def analyze(filename):
    with open(filename) as f:
        data = f.read()
    get_words = lambda t: re.sub("[^\w]", " ",  t).split()
    is_upper_word = lambda w:w.isupper() and len(w) > 2
    analysis = {}
    analysis['tweets'] = data.split('\EOT\n')
    analysis['tweet_lengths'] = [len(t) for t in analysis['tweets']]
    analysis['exclamation_tweets'] = [t for t in analysis['tweets'] if '!' in t]
    analysis['exclamation_end_tweets'] = [t for t in analysis['tweets'] if t.endswith('!')]
    analysis['tweet_upper'] = [t for t in analysis['tweets'] if any(map(is_upper_word, get_words(t)))]
    analysis['upper_words'] = Counter(re.findall(r'\b(?<!\\)[A-Z]{3,}(?!\\)\b', data))
    return analysis

def print_analysis(analysis, name):
    print '{0} exclamation points out of {1} tweets ({2:.2g}%) in {3} data'.format(
        len(analysis['exclamation_tweets']),
        len(analysis['tweets']),
        float(100*len(analysis['exclamation_tweets']))/len(analysis['tweets']),
        name)
    print '{0} exclamation points ending the tweet out of {1} tweets ({2:.2g}%) in {3} data'.format(
        len(analysis['exclamation_end_tweets']),
        len(analysis['tweets']),
        float(100*len(analysis['exclamation_end_tweets']))/len(analysis['tweets']),
        name)
    print '{0} tweets containing an uppercase word out of {1} tweets ({2:.2g}%) in {3} data'.format(
        len(analysis['tweet_upper']),
        len(analysis['tweets']),
        float(100*len(analysis['tweet_upper']))/len(analysis['tweets']),
        name)
    print '25 most common uppercase words in {} dataset:'.format(name)
    for (w, count) in analysis['upper_words'].most_common(25):
        print '{}: {}'.format(w, count)

in_analysis = analyze('input.txt')
out_analysis = analyze('output.txt')

print_analysis(in_analysis, 'input')
print_analysis(out_analysis, 'generated')

fig, ax = plt.subplots()
plt.hold(True)
plt.grid(True)
bins = range(0, 600, 14)
ax.set_xticks(range(0, 600, 100)+[140], minor=False)
plt.hist(in_analysis['tweet_lengths'], bins=bins, normed=True, fc=(0, 0, 1, 0.5), label='input tweets')
plt.hist(out_analysis['tweet_lengths'], bins=bins, normed=True, fc=(0, 1, 0, 0.5), label='generated tweets')
plt.legend()
plt.title('Tweet length distribution')
plt.xlabel('Characters count')
plt.ylabel('Frequency')
plt.show()
