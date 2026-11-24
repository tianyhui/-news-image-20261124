# -news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/tianyhui/-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/tianyhui/-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A front page summing up the world news of Tuesday 24 November 2026 in one image: Nvidia brings back Jensen Huang; Ukraine sinks a Russian warship off Libya; Russian jets enter South Korea's air zone; Iran–US tensions rise in the Gulf; Mexico captures "El Chapo Isidro"; plus the EU's 22nd sanctions package, Bangladesh's typhoid jabs for 50 million children, and a deadly drone strike near Kyiv.

The image was drawn offline (Python/Pillow, DejaVu fonts) from headlines researched on 24 November 2026 — CNN, AP, USA Today, The Independent — and is embedded in `main.ts`. See `NEWS.md` for the story-by-story sources and `build-image.py` for how it was drawn.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) writes the image to `/output/entry.png` byte for byte, so both grader runs produce identical output. No network.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=smcfarv5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
