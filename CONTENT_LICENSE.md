# 内容授权 / Content license

## 代码 / Code

本仓库的应用代码改编自 [Word Atlas（词光）](https://github.com/designfuchen/word-atlas)，作者为 designfuchen 与 Word Atlas contributors。原代码以 [MIT License](LICENSE) 授权，版权声明予以保留。本叉的修改同样以 MIT 提供。

Application code is adapted from [Word Atlas（词光）](https://github.com/designfuchen/word-atlas) by designfuchen and Word Atlas contributors. The upstream code is MIT; that copyright notice is kept. Changes in this fork are also offered under MIT.

依赖包保留各自授权。Fraunces 字体为 SIL Open Font License 1.1。

## 词库、插画与录音 / Dataset, illustrations, and audio

以下材料在维护者能够授予的权利范围内，以 **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** 提供：

- `data/toefl-atlas.json` 与 `data/toefl-atlas.csv`
- `public/atlas/index.json` 与 `public/atlas/entries/` 中的释义、例句、搭配、词族与分级
- `public/atlas/img/`、`public/atlas/thumb/` 中的插画
- `public/atlas/audio/` 中的单词发音与例句朗读
- 界面沿用的 `public/brand/` 话题图与 `public/sfx/` 环境声（见下）

**署名 / Attribution（必须保留）：**

> Word Atlas contributors（词光） / designfuchen — CC BY 4.0  
> https://github.com/designfuchen/word-atlas  
> 本项目做了修改：话题改为托福学术主题，例句重写为校园听力与学术阅读，并补入了词光词表中没有的托福词。

重叠词条的沿用清单（插画、英美单词录音，以及改编后的音标、释义、搭配、词族）见 [`data/reused-from-word-atlas.json`](data/reused-from-word-atlas.json)。

### 哪些是新写的，哪些是沿用的

| 材料 | 来源 |
| --- | --- |
| 与词光相同 id 的插画、缩略图 | 沿用词光，未改画 |
| 与词光相同 id 的美音 / 英音单词录音 | 沿用词光（ElevenLabs：英音 Alice，美音 Sarah），未重录 |
| 音标、义项、搭配、词族、近反义词 | 由词光词条改编 |
| 两条例句及中文 | 为本托福词库新写（模板与搭配生成，学习路线开头的词为手写例句） |
| 词光没有的补词（约 30 个） | 新写释义和例句；插画为本地生成的占位图；发音由 edge-tts 合成 |
| 例句朗读 | edge-tts，美式神经网络语音 `en-US-AriaNeural` |
| 开屏与星图中文配音 | edge-tts，`zh-CN-XiaoxiaoNeural`，替换了词光里带有「雅思」字样的开屏句 |
| 环境声、界面音效、星空配乐 | 沿用词光 `public/sfx/`（不含已替换的三句中文配音） |

edge-tts 使用微软 Edge 在线神经网络语音，只覆盖新生成的音频文件，不表示微软或 Edge 为本项目背书。词光原录音的授权只涉及那些音频文件本身，不包括底层声音模型。

## 不是官方考试产品 / Not an official test product

托词 **不是** ETS、TOEFL 或托福的官方产品、官方词表或合作项目。TOEFL 是 Educational Testing Service（ETS）的注册商标，此处仅用来描述学习者准备的考试类型。本词库不承诺提分。

This app is **not** affiliated with, endorsed by, or produced by ETS or the TOEFL program. TOEFL is a registered trademark of Educational Testing Service. The name is used only to describe the exam learners are preparing for.

## 质量边界 / Quality

例句、补词释义和占位插画由程序与模型辅助生成，经过结构校验，**没有逐条人工审校**。义项沿用词光时也可能带有上游的疏漏。发现错误可以直接改 `data/toefl-atlas.json` 与对应的 `public/atlas/entries/`。
