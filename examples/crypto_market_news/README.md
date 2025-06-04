# Crypto Market News Example

This example demonstrates using the Agents SDK to gather the latest market news on
Ethereum (ETH) and Bitcoin (BTC). It performs two web searches in parallel,
compiles a concise report, saves it to a markdown file and repeats the process
every 10 minutes.

Each run writes the report to `latest_crypto_report.md` (or a timestamped
filename if you include `{timestamp}` in the path when instantiating
`CryptoNewsManager`).

Run it with:

```bash
python -m examples.crypto_market_news.main
```
