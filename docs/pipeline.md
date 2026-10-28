# 内容生成流程 / Content pipeline

托词的应用结构来自词光。词条编译不走上游的 ElevenLabs / 图像接口，而是：

1. 从一份词光检出中筛选学术与校园词条（`scripts/toefl/build_dataset.py`）。
2. 重映射话题，重写例句（学习路线开头为手写，其余用该词自己的搭配嵌进校园 / 学术句架）。
3. 硬链接或复制已有插画与英美单词录音；没有插画的补词用 Pillow 画一张占位图。
4. 用 edge-tts 补全缺的单词发音，并为每条第一条例句合成美式朗读。
5. `npm run check:atlas` 核对结构、顺序和文件。

```bash
# 需要本机已有词光检出，默认 /tmp/word-atlas
python3 scripts/toefl/build_dataset.py --upstream /tmp/word-atlas
pip install edge-tts pillow
python3 scripts/toefl/gen_audio_edge.py          # 可断点续跑
python3 scripts/toefl/build_dataset.py --flags-only
npm run check:atlas
```

只改了例句、想保留已经链好的媒体时，直接再跑 `build_dataset.py` 即可：已存在且大小相同的媒体文件不会重写。

## 继续扩词

- 新词头写进 `scripts/toefl/supplements.py`（完整释义和例句），或放进上游词库后再筛选。
- 占位图可以日后换成统一画风的插画。`scripts/atlas/gen_images.py` 仍是词光的图像脚本：它读取 `.local/forge` 里的 `scene` 字段。把补词的 `scene` 写进 forge 后，可以用同一脚本生成，再覆盖 `public/atlas/img/<id>.webp` 与 `thumb/<id>.webp`，然后 `--flags-only`。
- 若有 ElevenLabs 密钥，`scripts/atlas/gen_word_audio.py` 与 `gen_sentence_audio.py` 仍可用。没有密钥时用 `gen_audio_edge.py`。
- 从零写新词条（不改编词光）时，用改过话题列表的 `scripts/atlas/gen_text.py`。它需要 OpenAI 兼容接口的 `SUB2_BASE_URL` 与 `SUB2_API_KEY`，凭据只放在环境变量或仓库外的目录，见 [SECURITY.md](../SECURITY.md)。

## 质量边界

`check:atlas` 检查结构、词头是否出现在第一条例句、媒体文件是否存在。它不判断释义和例句是否地道。当前例句没有逐条人工审校。
