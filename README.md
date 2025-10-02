aphorism-exporter
===

Prometheus exporter for [名言集.com](http://www.meigensyu.com/quotations/index/random).

## Usage

### docker

```sh
docker run -d -p 8000:8000 legnoh/aphorism-exporter

# wait 60s and get request
curl http://localhost:8000/metrics
```

### local

```sh
# clone
git clone https://github.com/legnoh/aphorism-exporter.git && cd aphorism-exporter
uv sync

# execute
uv run main.py
```

## Metrics(example)

```
# HELP aphorism_info 格言をランダムに表示
# TYPE aphorism_info gauge
aphorism_info{aphorism="ここに格言が表示されます",by="ここに格言の発言者名が表示されます"} 1.0
```

## Disclaim / 免責事項

- 当スクリプトは、goo 辞書 本家からは非公認のものです。
  - これらを利用したことによるいかなる損害についても当方では責任を負いかねます。
- 当スクリプトはこれらのサイトに対し、負荷をかけることを目的として制作したものではありません。
  - 利用の際は常識的な範囲でのアクセス頻度に抑えてください。
- 先方に迷惑をかけない範囲での利用を強く推奨します。
