"""TOEFL lemmas missing from Word Atlas. New text; illustrations and audio are generated locally."""

from __future__ import annotations


def _e(**kw):
    kw.setdefault("syn", [])
    kw.setdefault("ant", [])
    kw.setdefault("note", "")
    kw["id"] = kw["w"].lower().replace(" ", "-")
    return kw


SUPPLEMENTS = [
    _e(
        w="phenomenon", uk="/fəˈnɒmɪnən/", us="/fəˈnɑːmɪnən/", cefr="B2", topic="lecture",
        senses=[{"pos": "n.", "zh": "现象", "en": "A fact or event that can be observed and studied."}],
        ex=[
            {"en": "The lab treats the flicker as a phenomenon, not as a broken lamp.", "zh": "实验室把这种闪烁当作一种现象，而不是坏掉的灯。"},
            {"en": "The lecture asked which phenomenon the graph was actually measuring.", "zh": "讲座问这张图实际上在测量哪一种现象。"},
        ],
        col=["a natural phenomenon｜自然现象", "explain a phenomenon｜解释一种现象"],
        fam=["phenomena (n.)", "phenomenal (adj.)"],
        syn=["occurrence"], tip="复数是 phenomena，不是 phenomenons。",
    ),
    _e(
        w="biodiversity", uk="/ˌbaɪəʊdaɪˈvɜːsəti/", us="/ˌbaɪoʊdaɪˈvɜːrsəti/", cefr="B2", topic="environment",
        senses=[{"pos": "n.", "zh": "生物多样性", "en": "The variety of living things in a habitat or on Earth."}],
        ex=[
            {"en": "The field course measured biodiversity along the campus stream.", "zh": "野外课测量了校园溪流一带的生物多样性。"},
            {"en": "The reading links biodiversity to how well a forest recovers after a fire.", "zh": "这篇阅读把生物多样性和火灾后森林的恢复能力联系起来。"},
        ],
        col=["biodiversity loss｜生物多样性丧失", "protect biodiversity｜保护生物多样性"],
        fam=[], syn=["biological diversity"], tip="不可数名词，前面通常不加 a。",
    ),
    _e(
        w="infrastructure", uk="/ˈɪnfrəstrʌktʃə/", us="/ˈɪnfrəstrʌktʃər/", cefr="B2", topic="business",
        senses=[{"pos": "n.", "zh": "基础设施", "en": "Basic systems such as transport, power, and water that a place needs."}],
        ex=[
            {"en": "Aging infrastructure delayed the new lab's opening.", "zh": "老化的基础设施推迟了新实验室的启用。"},
            {"en": "The lecture compared spending on infrastructure with spending on short-term repairs.", "zh": "讲座比较了基础设施开支和短期维修开支。"},
        ],
        col=["public infrastructure｜公共基础设施", "transport infrastructure｜交通基础设施"],
        fam=[], syn=["public works"], tip="通常不可数；指具体系统时偶尔用复数。",
    ),
    _e(
        w="paradigm", uk="/ˈpærədaɪm/", us="/ˈpærədaɪm/", cefr="C1", topic="lecture",
        senses=[{"pos": "n.", "zh": "范式；典范", "en": "A widely accepted model of how a field understands its subject."}],
        ex=[
            {"en": "The seminar called the old textbook a fading paradigm.", "zh": "研讨课把那本旧教材称为正在消退的范式。"},
            {"en": "A paradigm shift happens when evidence no longer fits the model everyone uses.", "zh": "当证据不再符合人人都在用的模型时，就会发生范式转移。"},
        ],
        col=["paradigm shift｜范式转移", "a dominant paradigm｜主导范式"],
        fam=["paradigmatic (adj.)"], syn=["model", "framework"], tip="重音在第一音节。学术阅读里常与 shift 搭配。",
    ),
    _e(
        w="perception", uk="/pəˈsepʃn/", us="/pərˈsepʃn/", cefr="B2", topic="psychology",
        senses=[{"pos": "n.", "zh": "感知；看法", "en": "The way someone notices or understands something."}],
        ex=[
            {"en": "Lighting in the lab can change visual perception.", "zh": "实验室的光线会改变视觉感知。"},
            {"en": "The study measured perception of risk, not the risk itself.", "zh": "这项研究测量的是对风险的感知，而不是风险本身。"},
        ],
        col=["visual perception｜视觉感知", "public perception｜公众看法"],
        fam=["perceive (v.)", "perceptive (adj.)"], syn=["awareness"], ant=["misperception"],
        tip="作“看法”时，后面常用 of。",
    ),
    _e(
        w="demographic", uk="/ˌdeməˈɡræfɪk/", us="/ˌdeməˈɡræfɪk/", cefr="B2", topic="social",
        senses=[{"pos": "adj.", "zh": "人口统计的", "en": "Relating to the structure of a population."}, {"pos": "n.", "zh": "人群划分", "en": "A group in a population defined by age, income, or similar facts."}],
        ex=[
            {"en": "The report includes a demographic table in the appendix.", "zh": "报告在附录里放了一张人口统计表。"},
            {"en": "A demographic shift on campus can change which courses fill up first.", "zh": "校园里的人口结构变化会改变哪些课最先报满。"},
        ],
        col=["demographic change｜人口结构变化", "demographic data｜人口数据"],
        fam=["demography (n.)", "demographics (n.)"], tip="作名词时，demographics 更常表示各类人口数据。",
    ),
    _e(
        w="revenue", uk="/ˈrevənjuː/", us="/ˈrevənuː/", cefr="B2", topic="business",
        senses=[{"pos": "n.", "zh": "收入；收益", "en": "Money a government or organization receives."}],
        ex=[
            {"en": "Ticket sales are a small part of the museum's revenue.", "zh": "门票只占博物馆收入的一小部分。"},
            {"en": "The case study separates revenue from profit so students do not treat them as the same number.", "zh": "案例研究把收入和利润分开，以免学生把它们当成同一个数字。"},
        ],
        col=["tax revenue｜税收", "annual revenue｜年收入"],
        fam=[], syn=["income"], tip="收入是 revenue，利润是 profit。美式读音更接近 /ˈrevənuː/。",
    ),
    _e(
        w="inequality", uk="/ˌɪnɪˈkwɒləti/", us="/ˌɪnɪˈkwɑːləti/", cefr="B2", topic="social",
        senses=[{"pos": "n.", "zh": "不平等", "en": "An unfair difference in wealth, opportunity, or treatment."}],
        ex=[
            {"en": "The seminar traced inequality in who can afford unpaid internships.", "zh": "研讨课追溯了谁负担得起无薪实习这一问题中的不平等。"},
            {"en": "The reading asks whether the policy reduced inequality or only moved it.", "zh": "这篇阅读问这项政策是减少了不平等，还是只是把它转移了。"},
        ],
        col=["income inequality｜收入不平等", "social inequality｜社会不平等"],
        fam=["unequal (adj.)", "equality (n.)"], syn=["disparity"], ant=["equality"],
        tip="常用 income / social / gender inequality。",
    ),
    _e(
        w="legislation", uk="/ˌledʒɪsˈleɪʃn/", us="/ˌledʒɪsˈleɪʃn/", cefr="B2", topic="government",
        senses=[{"pos": "n.", "zh": "法律；立法", "en": "Laws, or the process of making laws."}],
        ex=[
            {"en": "New legislation changed what the lab may pour down the drain.", "zh": "新法规改变了实验室可以把什么倒进下水道。"},
            {"en": "The lecture separated legislation from the court cases that later interpreted it.", "zh": "讲座把立法和后来解释它的法院案件区分开来。"},
        ],
        col=["pass legislation｜通过法律", "environmental legislation｜环境法规"],
        fam=["legislate (v.)", "legislative (adj.)", "legislator (n.)"],
        tip="统称法律时通常不可数。",
    ),
    _e(
        w="commodity", uk="/kəˈmɒdəti/", us="/kəˈmɑːdəti/", cefr="B2", topic="business",
        senses=[{"pos": "n.", "zh": "商品；大宗货物", "en": "A raw material or basic product that can be bought and sold."}],
        ex=[
            {"en": "Coffee is both a campus habit and a traded commodity.", "zh": "咖啡既是校园习惯，也是被交易的大宗商品。"},
            {"en": "The article explains how a commodity price can fall even when local shops stay expensive.", "zh": "文章解释了为什么大宗商品价格下跌时，本地商店仍可能很贵。"},
        ],
        col=["a commodity price｜大宗商品价格", "commodity market｜商品市场"],
        fam=["commodities (n.)"], tip="复数 commodities 常指整类大宗商品。",
    ),
    _e(
        w="cognition", uk="/kɒɡˈnɪʃn/", us="/kɑːɡˈnɪʃn/", cefr="C1", topic="psychology",
        senses=[{"pos": "n.", "zh": "认知", "en": "The mental processes of knowing, remembering, and reasoning."}],
        ex=[
            {"en": "Sleep loss slows cognition on timed quizzes.", "zh": "睡眠不足会让限时小测中的认知变慢。"},
            {"en": "The lecture treated language and memory as related parts of cognition.", "zh": "讲座把语言和记忆视为认知中相关的部分。"},
        ],
        col=["human cognition｜人类认知", "social cognition｜社会认知"],
        fam=["cognitive (adj.)"], syn=["mental processing"], tip="形容词是 cognitive，重音在第二音节。",
    ),
    _e(
        w="emphasize", uk="/ˈemfəsaɪz/", us="/ˈemfəsaɪz/", cefr="B2", topic="lecture",
        senses=[{"pos": "v.", "zh": "强调；着重", "en": "To give special importance to something."}],
        ex=[
            {"en": "The professor emphasized the definition, not the anecdote.", "zh": "教授强调的是定义，不是那个轶事。"},
            {"en": "Writers emphasize a contrast by placing the two claims in neighboring sentences.", "zh": "作者把两个主张放在相邻的句子里，以强调对比。"},
        ],
        col=["emphasize the importance of｜强调…的重要性", "emphasize that｜强调说"],
        fam=["emphasis (n.)", "emphatic (adj.)"], syn=["stress", "highlight"],
        tip="美式拼写 emphasize；英式常用 emphasise。托福写作用美式即可。",
    ),
    _e(
        w="consistent", uk="/kənˈsɪstənt/", us="/kənˈsɪstənt/", cefr="B2", topic="lecture",
        senses=[{"pos": "adj.", "zh": "一致的；一贯的", "en": "Always acting or happening in the same way, or in agreement with something."}],
        ex=[
            {"en": "Her lab notes were consistent from week to week.", "zh": "她的实验笔记一周又一周都保持一致。"},
            {"en": "The result is consistent with the hypothesis, but it does not prove it.", "zh": "结果与假说一致，但并不能证明假说。"},
        ],
        col=["consistent with｜与…一致", "a consistent pattern｜一贯的模式"],
        fam=["consistency (n.)", "consistently (adv.)"], syn=["steady"], ant=["inconsistent"],
        tip="表示“与…相符”用 consistent with，不是 consistent to。",
    ),
    _e(
        w="contrast", uk="/ˈkɒntrɑːst/", us="/ˈkɑːntræst/", cefr="B2", topic="lecture",
        senses=[{"pos": "n.", "zh": "对比；差异", "en": "A clear difference between two people or things."}, {"pos": "v.", "zh": "对比", "en": "To compare in order to show differences."}],
        ex=[
            {"en": "The slide put the two maps in contrast.", "zh": "这张幻灯片把两张地图放在一起对比。"},
            {"en": "The passage draws a contrast between a short lab task and a semester-long study.", "zh": "文章对比了短时实验任务和长达一学期的研究。"},
        ],
        col=["in contrast to｜与…对比", "a sharp contrast｜鲜明对比"],
        fam=["contrasting (adj.)"], syn=["difference"], tip="名词重音常在前；动词重音常在后：contrast the two claims。",
    ),
    _e(
        w="qualitative", uk="/ˈkwɒlɪtətɪv/", us="/ˈkwɑːləteɪtɪv/", cefr="B2", topic="lecture",
        senses=[{"pos": "adj.", "zh": "定性的；性质的", "en": "Concerned with qualities and descriptions rather than numbers."}],
        ex=[
            {"en": "The interview study used a qualitative method.", "zh": "这项访谈研究使用了定性方法。"},
            {"en": "A qualitative comment can explain a number that the chart leaves bare.", "zh": "一句定性评论可以解释图表上光秃秃的数字。"},
        ],
        col=["qualitative research｜定性研究", "qualitative data｜定性数据"],
        fam=["quality (n.)"], ant=["quantitative"], tip="和 quantitative（定量的）成对出现，不要看错首字母。",
    ),
    _e(
        w="validity", uk="/vəˈlɪdəti/", us="/vəˈlɪdəti/", cefr="C1", topic="lecture",
        senses=[{"pos": "n.", "zh": "效度；有效性", "en": "The quality of being logically sound or of measuring what is intended."}],
        ex=[
            {"en": "The professor questioned the validity of the online quiz.", "zh": "教授质疑这份在线小测的效度。"},
            {"en": "A large sample does not by itself guarantee the validity of a measure.", "zh": "样本大本身并不能保证测量的效度。"},
        ],
        col=["validity of a test｜测验的效度", "external validity｜外部效度"],
        fam=["valid (adj.)", "validate (v.)"], syn=["soundness"], tip="效度是 validity，信度是 reliability。",
    ),
    _e(
        w="plagiarism", uk="/ˈpleɪdʒərɪzəm/", us="/ˈpleɪdʒərɪzəm/", cefr="B2", topic="campus",
        senses=[{"pos": "n.", "zh": "抄袭；剽窃", "en": "Using someone else's words or ideas as your own without credit."}],
        ex=[
            {"en": "The syllabus says plagiarism can mean a failing grade.", "zh": "教学大纲写明抄袭可能导致课程不及格。"},
            {"en": "Changing a few words does not prevent plagiarism if the structure is still copied.", "zh": "如果结构仍是抄来的，只改几个词也不能避免抄袭。"},
        ],
        col=["commit plagiarism｜抄袭", "plagiarism policy｜抄袭处理规定"],
        fam=["plagiarize (v.)"], tip="学术写作里，引用是 citation，抄袭是 plagiarism。",
    ),
    _e(
        w="syllabus", uk="/ˈsɪləbəs/", us="/ˈsɪləbəs/", cefr="B1", topic="campus",
        senses=[{"pos": "n.", "zh": "教学大纲", "en": "A document that lists the plan, readings, and rules for a course."}],
        ex=[
            {"en": "Check the syllabus before you email the professor.", "zh": "给教授发邮件之前先看教学大纲。"},
            {"en": "The syllabus states the grading scale and the policy on late work.", "zh": "教学大纲写明了评分标准和迟交作业的规定。"},
        ],
        col=["course syllabus｜课程大纲", "on the syllabus｜在大纲上"],
        fam=["syllabi (n.)", "syllabuses (n.)"], tip="复数 syllabi 或 syllabuses 都可以。",
    ),
    _e(
        w="citation", uk="/saɪˈteɪʃn/", us="/saɪˈteɪʃn/", cefr="B2", topic="campus",
        senses=[{"pos": "n.", "zh": "引用；引文", "en": "A note that tells the reader where a fact or quotation came from."}],
        ex=[
            {"en": "Every chart in the paper needs a citation.", "zh": "论文里的每张图都需要引用出处。"},
            {"en": "A missing citation makes it hard to check whether the claim is fair.", "zh": "缺少引用会让人难以核对这个主张是否公允。"},
        ],
        col=["a citation style｜引文格式", "in-text citation｜文内引用"],
        fam=["cite (v.)"], tip="cite 是动词，citation 是名词。",
    ),
    _e(
        w="sustainability", uk="/səˌsteɪnəˈbɪləti/", us="/səˌsteɪnəˈbɪləti/", cefr="B2", topic="environment",
        senses=[{"pos": "n.", "zh": "可持续性", "en": "The ability to continue without using up resources or causing serious harm."}],
        ex=[
            {"en": "The campus plan lists sustainability next to new construction.", "zh": "校园规划把可持续性和新建工程放在一起。"},
            {"en": "The reading asks whether sustainability is a technical problem or also a social one.", "zh": "这篇阅读问可持续性究竟只是技术问题，还是同时也是社会问题。"},
        ],
        col=["environmental sustainability｜环境可持续性", "sustainability report｜可持续发展报告"],
        fam=["sustainable (adj.)", "sustain (v.)"], tip="形容词 sustainable 在托福阅读里更常见。",
    ),
    _e(
        w="roommate", uk="/ˈruːmmeɪt/", us="/ˈruːmmeɪt/", cefr="A2", topic="campus",
        senses=[{"pos": "n.", "zh": "室友", "en": "A person who shares a room or apartment."}],
        ex=[
            {"en": "My roommate and I split the grocery list.", "zh": "我和室友分开列了购物清单。"},
            {"en": "A noisy roommate can affect sleep and, with it, attention in morning lectures.", "zh": "吵闹的室友会影响睡眠，进而影响早课的注意力。"},
        ],
        col=["college roommate｜大学室友", "roommate agreement｜室友公约"],
        fam=[], tip="美式校园听力里极常见；英式也说 flatmate。",
    ),
    _e(
        w="midterm", uk="/ˌmɪdˈtɜːm/", us="/ˈmɪdtɜːrm/", cefr="B1", topic="campus",
        senses=[{"pos": "n.", "zh": "期中考试", "en": "An exam given about halfway through a course."}, {"pos": "adj.", "zh": "期中的", "en": "Happening in the middle of a term."}],
        ex=[
            {"en": "The midterm covers the first six lectures.", "zh": "期中考试涵盖前六次讲座。"},
            {"en": "Students who review a little each week usually find the midterm less rushed.", "zh": "每周复习一点的学生，通常不会把期中考试复习得太赶。"},
        ],
        col=["midterm exam｜期中考试", "before the midterm｜期中考试前"],
        fam=[], syn=["midterm examination"], tip="也可写作 mid-term。托福听力里多指考试，不是政治上的中期选举，除非语境如此。",
    ),
    _e(
        w="freshman", uk="/ˈfreʃmən/", us="/ˈfreʃmən/", cefr="B1", topic="campus",
        senses=[{"pos": "n.", "zh": "大学一年级学生", "en": "A student in the first year of high school or college."}],
        ex=[
            {"en": "Every freshman attends the library tour.", "zh": "每位大一学生都要参加图书馆参观。"},
            {"en": "The study followed one freshman cohort from orientation to the end of spring.", "zh": "这项研究跟踪了一届大一学生，从迎新一直到春季学期结束。"},
        ],
        col=["freshman year｜大一学年", "a freshman seminar｜新生研讨课"],
        fam=["freshmen (n.)"], tip="复数是 freshmen。指大二到大四常用 sophomore, junior, senior。",
    ),
    _e(
        w="notion", uk="/ˈnəʊʃn/", us="/ˈnoʊʃn/", cefr="B2", topic="lecture",
        senses=[{"pos": "n.", "zh": "概念；看法", "en": "An idea or belief about something."}],
        ex=[
            {"en": "The notion sounds simple until you try to measure it.", "zh": "这个概念听起来简单，直到你试图测量它。"},
            {"en": "The author rejects the notion that one test can capture a whole ability.", "zh": "作者拒绝“一次测验就能抓住全部能力”这种看法。"},
        ],
        col=["the notion that｜认为…的看法", "a vague notion｜模糊的概念"],
        fam=[], syn=["idea", "concept"], tip="notion that 后面接完整从句。",
    ),
    _e(
        w="substantial", uk="/səbˈstænʃl/", us="/səbˈstænʃl/", cefr="B2", topic="lecture",
        senses=[{"pos": "adj.", "zh": "大量的；重大的", "en": "Large in amount or importance."}],
        ex=[
            {"en": "There was a substantial gap between the two groups.", "zh": "两组之间有很大的差距。"},
            {"en": "The lecture called the improvement substantial, not merely statistically detectable.", "zh": "讲座称这一改进是实质性的，而不只是统计上能检测出来。"},
        ],
        col=["a substantial increase｜大幅增加", "substantial evidence｜大量证据"],
        fam=["substantially (adv.)"], syn=["considerable"], ant=["negligible"],
        tip="不要和 substantive（实质的、有内容的）混淆。",
    ),
    _e(
        w="subsequent", uk="/ˈsʌbsɪkwənt/", us="/ˈsʌbsɪkwənt/", cefr="B2", topic="lecture",
        senses=[{"pos": "adj.", "zh": "随后的", "en": "Happening or coming after something else."}],
        ex=[
            {"en": "Subsequent lectures built on that first definition.", "zh": "随后的讲座都建立在第一个定义之上。"},
            {"en": "A subsequent study used a larger sample and found a smaller effect.", "zh": "随后的一项研究使用了更大的样本，发现的效应更小。"},
        ],
        col=["subsequent research｜后续研究", "in subsequent years｜在随后几年"],
        fam=["subsequently (adv.)"], syn=["later", "following"], ant=["previous"],
        tip="subsequent 是形容词；副词是 subsequently。",
    ),
    _e(
        w="preliminary", uk="/prɪˈlɪmɪnəri/", us="/prɪˈlɪmɪneri/", cefr="B2", topic="lecture",
        senses=[{"pos": "adj.", "zh": "初步的", "en": "Coming before a fuller study or a final result."}],
        ex=[
            {"en": "These preliminary results may change after we add more data.", "zh": "补充更多数据后，这些初步结果可能会变。"},
            {"en": "The speaker labeled the finding preliminary and asked the class not to overstate it.", "zh": "讲者把这一发现标为初步结果，并请全班不要夸大。"},
        ],
        col=["preliminary results｜初步结果", "a preliminary study｜初步研究"],
        fam=["preliminarily (adv.)"], syn=["initial"], tip="美式读音末尾更接近 /neri/。",
    ),
    _e(
        w="whereas", uk="/ˌweərˈæz/", us="/ˌwerˈæz/", cefr="B2", topic="lecture",
        senses=[{"pos": "conj.", "zh": "然而；尽管", "en": "Used to compare two facts that differ."}],
        ex=[
            {"en": "The first group improved, whereas the second did not.", "zh": "第一组有进步，而第二组没有。"},
            {"en": "The lecture uses whereas to contrast a lab task with a real semester of study.", "zh": "讲座用 whereas 对比实验室任务和真实的一学期学习。"},
        ],
        col=["whereas others｜而其他人"],
        fam=[], syn=["while"], tip="whereas 连接两个完整分句，前面常用逗号。",
    ),
    _e(
        w="nonetheless", uk="/ˌnʌnðəˈles/", us="/ˌnʌnðəˈles/", cefr="C1", topic="lecture",
        senses=[{"pos": "adv.", "zh": "尽管如此", "en": "In spite of what has just been said."}],
        ex=[
            {"en": "The sample was small; the pattern was clear nonetheless.", "zh": "样本很小，尽管如此，模式仍然清楚。"},
            {"en": "Nonetheless, the author treats the result as a reason to repeat the study.", "zh": "尽管如此，作者仍把这一结果视为重复研究的理由。"},
        ],
        col=["nonetheless important｜尽管如此仍然重要"],
        fam=[], syn=["nevertheless", "however"], tip="语气比 however 更书面，阅读里很常见。",
    ),
    _e(
        w="prevalent", uk="/ˈprevələnt/", us="/ˈprevələnt/", cefr="C1", topic="social",
        senses=[{"pos": "adj.", "zh": "普遍的；流行的", "en": "Common at a particular time or in a particular place."}],
        ex=[
            {"en": "The habit is prevalent in first-year dorms.", "zh": "这个习惯在大一宿舍里很普遍。"},
            {"en": "The passage asks why the belief became prevalent even though the evidence was thin.", "zh": "文章问为什么证据薄弱时，这种看法仍然变得普遍。"},
        ],
        col=["prevalent among｜在…中普遍", "widely prevalent｜广泛流行"],
        fam=["prevalence (n.)"], syn=["widespread", "common"], tip="名词是 prevalence，常用于流行病学或社会调查。",
    ),
]
