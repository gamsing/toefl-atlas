# 托词 · TOEFL Atlas

**一词一画，点亮托福。**

面向托福备考的学术词汇图鉴：插画、中英释义、校园听力与学术阅读例句、美音和英音、FSRS 间隔复习。进度只存在你的浏览器里。

**这不是 ETS 或 TOEFL 的官方产品。** TOEFL 是 Educational Testing Service 的注册商标，这里只表示学习目标，与 ETS 没有附属、背书或合作关系，也不承诺提分。

代码改编自 [词光 Word Atlas](https://github.com/designfuchen/word-atlas)（designfuchen 与 Word Atlas contributors，MIT）。重合词条的插画和单词录音沿用该项目（CC BY 4.0）。

[English](#english)

## 这版有多大

| | |
| --- | --- |
| 词条 | **4429** |
| 例句 | **8858**（每词一条校园听力、一条学术阅读） |
| 插画 | **4429**（其中 4399 幅沿用词光，30 幅为补词占位图） |
| 录音 | **4429** 美音、**4429** 英音、**4429** 条第一条例句朗读 |
| 话题 | **13** 个托福向学术 / 校园主题 |
| 难度 | CEFR A1–C2，只用于筛选和安排起点 |

话题：校园生活、学术讲座、社会科学、自然科学、人文艺术、技术工程、环境生态、健康医学、商业经济、历史文明、心理认知、政府法律、媒体传播。

学习路线开头是一批高频学术词和校园词（lecture、research、analyze、evidence 等），例句是写好的。其余词的例句用该词自己的搭配嵌进校园或学术句架，**没有逐条人工审校**。

## 本地运行

需要 Node.js 20+。

```bash
npm ci
npm run dev
```

打开 **http://localhost:5471**。

```bash
npm test
npm run check:atlas
npm run build
```

## 和词光的差别

| | 词光 Word Atlas | 托词 TOEFL Atlas |
| --- | --- | --- |
| 考试取向 | 雅思 | 托福（美式学术英语优先，仍保留英音） |
| 词条 | 约 7300，含大量生活词 | 4429，偏学术、讲座和校园 |
| 话题 | 19 个雅思话题 | 13 个托福向话题 |
| 例句 | 日常短句 + 雅思长句 | 校园听力 + 学术阅读，新写 |
| 单词发音 | ElevenLabs | 重合词沿用词光录音；补词用 edge-tts |
| 例句朗读 | ElevenLabs | edge-tts 美式语音 |
| 开屏 | 「欢迎打开雅思大门」 | 「欢迎来到托词」 |

界面、FSRS、星图、练习模式、本地导入导出和环境声沿用词光的结构。

## 开放数据

```python
import json
from pathlib import Path

words = json.loads(Path("data/toefl-atlas.json").read_text(encoding="utf-8"))
lectures = [w for w in words if w["topic"] == "lecture" and w["cefr"] == "B2"]
```

字段说明见 [docs/dataset.md](docs/dataset.md)。沿用名单见 [data/reused-from-word-atlas.json](data/reused-from-word-atlas.json)。

## 补全或重做媒体

```bash
pip install edge-tts pillow
python3 scripts/toefl/build_dataset.py --upstream /path/to/word-atlas
python3 scripts/toefl/gen_audio_edge.py
npm run check:atlas
```

没有词光检出时，不要重跑 `build_dataset.py`，否则会丢掉已链好的插画。只刷新媒体标记：

```bash
python3 scripts/toefl/build_dataset.py --flags-only
```

细节见 [docs/pipeline.md](docs/pipeline.md)。

## 授权

| 范围 | 许可 |
| --- | --- |
| 应用代码 | [MIT](LICENSE)，上游版权归 Word Atlas contributors |
| 词库文本、沿用的插画与单词录音 | [CC BY 4.0](CONTENT_LICENSE.md)，署名 Word Atlas contributors（词光）/ designfuchen，并说明做过修改 |
| 新写例句、补词、占位图、edge-tts 录音 | 同样以 CC BY 4.0 提供；edge-tts 语音不表示微软为本项目背书 |
| 环境声与界面音效 | 沿用词光 `public/sfx/`，开屏和星图中文配音已替换 |

## English

TOEFL Atlas (托词) is a local-first vocabulary app for the TOEFL iBT: illustrated entries, bilingual senses, a short campus-listening example, a longer academic-reading example, US and UK pronunciation, and FSRS review. It is a fork of [Word Atlas](https://github.com/designfuchen/word-atlas).

It is **not** an official ETS or TOEFL product and does not claim a score gain. TOEFL is a trademark of Educational Testing Service.

The shipped set has **4429** lemmas and **8858** examples across 13 academic and campus topics. Illustrations and lemma audio for overlapping Word Atlas ids are reused under CC BY 4.0 and listed in `data/reused-from-word-atlas.json`. Examples are new and have not been proofread line by line.

```bash
npm ci
npm run dev    # http://localhost:5471
npm test && npm run check:atlas && npm run build
```

Regenerate missing audio with `pip install edge-tts pillow` and `python3 scripts/toefl/gen_audio_edge.py`. See [docs/pipeline.md](docs/pipeline.md).
