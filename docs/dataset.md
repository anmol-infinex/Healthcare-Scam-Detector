# Dataset Notes

## Public Dataset Research

The most accessible public baseline is the UCI SMS Spam Collection. It contains 5,574 English SMS messages labeled as ham or spam and is widely used for SMS spam research.

Additional sources reviewed:

- Mendeley SMS Phishing Dataset: includes ham, spam, and smishing labels, but automated redistribution/download may require manual acceptance.
- Nazario Phishing Corpus: useful for email phishing, but message format and licensing require careful handling before redistribution.
- Healthcare-specific phishing datasets referenced in recent papers and Kaggle pages: relevant, but not reliably available through unauthenticated download.

## Included Data

`data/processed/healthcare_seed_messages.csv` contains small, original healthcare-themed examples for portfolio demonstration and offline training. It is not a substitute for a large production dataset.

## Label Mapping

`legit`: routine appointments, billing notices, portal reminders, pharmacy updates.

`scam`: spam, smishing, phishing, identity theft, fake refund, credential theft, payment-pressure messages.

## Preprocessing

- Normalize whitespace.
- Remove exact duplicate messages.
- Validate text and label columns.
- Map compatible public labels into the binary target.

## Source Links

- UCI SMS Spam Collection: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- Mendeley SMS Phishing Dataset: https://data.mendeley.com/datasets/f45bkkt8pr/1
- Nazario Phishing Corpus: https://monkey.org/~jose/phishing/
