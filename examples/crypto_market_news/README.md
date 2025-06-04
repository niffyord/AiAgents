# Crypto Market News Example

This example demonstrates using the Agents SDK to gather the latest market news on
Ethereum (ETH) and Bitcoin (BTC). It performs two web searches in parallel and
then compiles a short report. The workflow now runs every ten minutes and
overwrites a `crypto_news.json` file in the `outputs` directory with the latest report.

Run it with:

```bash
python -m examples.crypto_market_news.main
```
