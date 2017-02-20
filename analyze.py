import matplotlib.pyplot as plt

def analyze(filename):
    with open(filename) as f:
        data = f.read()
    analysis = {}
    analysis['tweets'] = data.split('\EOT\n')
    analysis['tweet_lengths'] = [len(t) for t in analysis['tweets']]
    analysis['exclamation_tweets'] = [t for t in analysis['tweets'] if '!' in t]
    analysis['exclamation_end_tweets'] = [t for t in analysis['tweets'] if t.endswith('!')]
    return analysis

in_analysis = analyze('input.txt')
out_analysis = analyze('output.txt')

print '{0} exclamation points out of {1} tweets ({2:.2}%) in input data'.format(
    len(in_analysis['exclamation_tweets']), len(in_analysis['tweets']), float(len(in_analysis['exclamation_tweets']))/len(in_analysis['tweets']))
print '{0} exclamation points out of {1} tweets ({2:.2}%)  in generated data'.format(
    len(out_analysis['exclamation_tweets']), len(out_analysis['tweets']), float(len(out_analysis['exclamation_tweets']))/len(out_analysis['tweets']))

print '{0} exclamation points ending the tweet out of {1} tweets ({2:.2}%) in input data'.format(
    len(in_analysis['exclamation_end_tweets']), len(in_analysis['tweets']), float(len(in_analysis['exclamation_end_tweets']))/len(in_analysis['tweets']))
print '{0} exclamation points ending the tweet out of {1} tweets ({2:.2}%)  in generated data'.format(
    len(out_analysis['exclamation_end_tweets']), len(out_analysis['tweets']), float(len(out_analysis['exclamation_end_tweets']))/len(out_analysis['tweets']))


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
