# 词库格式 / Dataset format

## `data/toefl-atlas.json`

一个数组，按学习路线排序：CEFR 由易到难；每一级里，先排一批高频学术词和校园词，其余按稳定散列打散话题。字段与词光 `word-atlas.json` 相同：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | URL 安全的唯一标识，也是媒体文件名 |
| `w` | string | 词头。美式与英式若在上游分列，这里都保留 |
| `uk` / `us` | string | 英式 / 美式 IPA，带斜杠 |
| `senses` | `{pos, zh, en}[]` | 义项。与词光重合的词改编自上游；补词为新写 |
| `ex` | `{en, zh}[]` | 两条例句：`ex[0]` 校园听力短句，`ex[1]` 学术阅读长句 |
| `col` | string[] | 搭配，`english｜中文` |
| `fam` | string[] | 词族，`word (pos)` |
| `syn` / `ant` | string[] | 近义 / 反义 |
| `tip` | string | 一条中文用法提示 |
| `cefr` | `A1`…`C2` | 估计难度，用来筛选，不是官方分数 |
| `topic` | string | 见下表 |
| `note` | string | 可选用法提醒 |

### 话题

`campus` 校园生活，`lecture` 学术讲座，`social` 社会科学，`natural` 自然科学，`arts` 人文艺术，`technology` 技术工程，`environment` 环境生态，`health` 健康医学，`business` 商业经济，`history` 历史文明，`psychology` 心理认知，`government` 政府法律，`media` 媒体传播。

## `data/toefl-atlas.csv`

同一内容的表格版。多值字段用 ` | `、` ; ` 或 `, ` 连接，UTF-8。

## `data/reused-from-word-atlas.json`

列出从词光沿用插画和单词录音的 id。补词 id 在 `placeholders` 里。

## 网页数据 `public/atlas/`

- `index.json`：`words` 每行是 `[id, word, zh, ipa, cefrIndex, topicIndex, media]`。`media` 位标记：`1` 插画、`2` 英音、`4` 美音、`8` 例句朗读、`16` 第二条例句朗读。
- `entries/<n>.json`：每块 100 条，顺序与索引一致。
- `img/<id>.webp`（约 512px）、`thumb/<id>.webp`（256px）。
- `audio/uk/<id>.mp3`、`audio/us/<id>.mp3`、`audio/ex/<id>.mp3`（`ex[0]`）。

媒体以位标记为准。缺文件时，应用会退回设备自带的语音合成。

## 授权

CC BY 4.0。沿用部分请署名 “Word Atlas contributors（词光）”。见 [CONTENT_LICENSE.md](../CONTENT_LICENSE.md)。
