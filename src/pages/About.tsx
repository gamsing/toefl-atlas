import { ArrowUpRight, Database, Github, Heart } from "lucide-react";
import { useAtlas } from "../atlas/context";
import { REPO_URL } from "../config";

const BASE = import.meta.env.BASE_URL;

export function About() {
  const atlas = useAtlas();
  return (
    <div className="page about">
      <header className="about-hero">
        <img src={`${BASE}brand/og.webp`} alt="" />
        <div>
          <p className="eyebrow">关于托词</p>
          <h1 className="display">一词一画，点亮托福。</h1>
          <p className="lede">
            托词是面向托福备考的学术词汇图鉴，共 {atlas.count.toLocaleString()} 个词条。每个词有插画、中英释义、一条校园听力例句、一条学术阅读例句，以及美音和英音。学会一个，就在星图上点亮一颗星。
          </p>
          <p className="lede">它免费、本地优先、无需注册。代码改编自词光 Word Atlas（MIT），词库在 CC BY 4.0 下提供。这不是 ETS 或托福的官方产品。</p>
          <div className="about-actions">
            <a className="btn btn-primary" href={REPO_URL} target="_blank" rel="noreferrer">
              <Github size={18} /> 上游词光 Word Atlas
            </a>
            <a className="btn btn-ghost" href="#/atlas">
              <Database size={18} /> 在图鉴里浏览词库
            </a>
          </div>
        </div>
      </header>

      <div className="about-grid">
        <section className="panel">
          <h3 className="eyebrow">为什么记得住</h3>
          <ul className="feature-list">
            <li>
              <b>先看见。</b>每个词都有一幅画，画的就是第一句例句里发生的事。
            </li>
            <li>
              <b>再想起。</b>选义、看图补句、听音辨词、拼写，从认得走到会写。
            </li>
            <li>
              <b>刚好在快忘时重逢。</b>FSRS 是新版 Anki 用的开源记忆算法，只在你快要遗忘时安排复习。
            </li>
            <li>
              <b>分数诚实。</b>只算第一次作答。答错的词会换个题型再见一面，但不会抬高正确率。
            </li>
            <li>
              <b>进度只属于你。</b>没有账号，没有服务器，数据存在你的浏览器里，随时能导出。
            </li>
          </ul>
        </section>

        <section className="panel">
          <h3 className="eyebrow">快捷键</h3>
          <dl className="keys">
            <div>
              <dt>
                <kbd>⌘</kbd>
                <kbd>K</kbd> 或 <kbd>/</kbd>
              </dt>
              <dd>搜索任何词</dd>
            </div>
            <div>
              <dt>
                <kbd>1</kbd>–<kbd>4</kbd>
              </dt>
              <dd>选择答案</dd>
            </div>
            <div>
              <dt>
                <kbd>Enter</kbd>
              </dt>
              <dd>确认 / 继续</dd>
            </div>
            <div>
              <dt>
                <kbd>←</kbd> <kbd>→</kbd>
              </dt>
              <dd>词卡里切换上一个、下一个</dd>
            </div>
            <div>
              <dt>
                <kbd>Esc</kbd>
              </dt>
              <dd>关闭弹窗</dd>
            </div>
          </dl>
        </section>

        <section className="panel">
          <h3 className="eyebrow">内容从哪里来</h3>
          <p className="muted">
            与词光重合的词条：释义、音标、搭配和词族改编自 Word Atlas contributors（词光）的 CC BY 4.0 词库；插画和单词发音录音在这些词上直接沿用，名单见 <code>data/reused-from-word-atlas.json</code>。例句是为托福的校园听力与学术阅读新写的。补入的词使用本地生成的插画，单词和例句朗读可用 edge-tts 重新合成。内容经过结构校验，没有逐条人工审校。
          </p>
          <p className="muted">托词不是官方托福词表，与 ETS 无关，也不承诺提分。TOEFL 是 ETS 的注册商标，这里只用来说明学习目标。</p>
        </section>

        <section className="panel">
          <h3 className="eyebrow">给开发者</h3>
          <p className="muted">
            <code>data/toefl-atlas.json</code> 和 <code>.csv</code> 是完整词库；<code>public/atlas</code> 里是网页用的分块数据、插画和音频。拿去做自己的练习工具时，请保留对 Word Atlas contributors（词光）和本词库的署名。
          </p>
          <a className="link" href={`${REPO_URL}#readme`} target="_blank" rel="noreferrer">
            阅读文档 <ArrowUpRight size={14} />
          </a>
        </section>
      </div>
      <p className="colophon">
        <Heart size={14} /> 做给每一个在背单词的人。
      </p>
    </div>
  );
}
