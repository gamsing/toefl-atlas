"""TOEFL topic map, example frames, hand-written path entries, and gap lemmas.

Example sentences for the learning-path head are written out in full.
The rest are assembled from part-of-speech frames so every lemma stays
grammatical and in a campus or academic setting.
"""

from __future__ import annotations

import hashlib
import re

# (id, zh label) — order is the galaxy arm order.
TOPICS: list[tuple[str, str]] = [
    ("campus", "校园生活"),
    ("lecture", "学术讲座"),
    ("social", "社会科学"),
    ("natural", "自然科学"),
    ("arts", "人文艺术"),
    ("technology", "技术工程"),
    ("environment", "环境生态"),
    ("health", "健康医学"),
    ("business", "商业经济"),
    ("history", "历史文明"),
    ("psychology", "心理认知"),
    ("government", "政府法律"),
    ("media", "媒体传播"),
]

TOPIC_FIELD = {
    "campus": ("student life", "校园生活"),
    "lecture": ("academic research", "学术研究"),
    "social": ("social change", "社会变迁"),
    "natural": ("the natural sciences", "自然科学"),
    "arts": ("the humanities", "人文学科"),
    "technology": ("technological change", "技术变革"),
    "environment": ("environmental policy", "环境政策"),
    "health": ("public health", "公共卫生"),
    "business": ("economic policy", "经济政策"),
    "history": ("historical change", "历史变迁"),
    "psychology": ("human behavior", "人类行为"),
    "government": ("public institutions", "公共制度"),
    "media": ("public communication", "公共传播"),
}

CEFR = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Pedagogical head of each level. These ids are ordered before the hashed mix.
FIRST = [
    "library", "student", "university", "course", "professor", "essay", "method",
    "environment", "behavior", "lecture", "campus", "research", "experiment",
    "semester", "assignment", "policy", "culture", "argument", "conclusion",
    "affect", "effect", "benefit", "structure", "process", "identify", "define",
    "achieve", "require", "occur", "analyze", "evidence", "significant", "context",
    "factor", "concept", "approach", "data", "assume", "interpret", "evaluate",
    "bias", "psychology", "perspective", "consequence", "abstract", "theory",
    "hypothesis", "emphasize", "consistent", "phenomenon", "perception",
    "plagiarism", "syllabus",
]

# Kept even if they sit in daily/A1, because TOEFL listening uses them.
ALLOW = {
    "library", "student", "college", "university", "course", "exam", "class",
    "homework", "notebook", "textbook", "classmate", "quiz", "canteen",
    "cafeteria", "require", "occur", "minor", "deadline", "advisor", "schedule",
    "presentation", "grade", "tutor", "dorm", "lab",
}

DENY = {
    "idiot", "damn", "dumb", "fatty", "freak", "molest", "cock", "drunkard",
    "handicap", "cripple", "queer", "savage", "maniac", "coloured", "colored",
}

CAMPUS_IDS = {
    "library", "student", "college", "university", "course", "exam", "class",
    "homework", "notebook", "textbook", "classmate", "quiz", "canteen",
    "cafeteria", "dorm", "professor", "essay", "lecture", "assignment",
    "scholarship", "tuition", "semester", "faculty", "undergraduate", "graduate",
    "transcript", "advisor", "curriculum", "workshop", "tutorial", "recitation",
    "degree", "diploma", "attendance", "absent", "registrar", "schedule",
    "laboratory", "lab", "seminar", "thesis", "bibliography", "campus",
    "presentation", "tutor", "deadline", "syllabus", "roommate", "midterm",
    "freshman", "plagiarism", "citation", "major", "minor",
}

PSYCH_IDS = {
    "cognitive", "cognition", "perception", "stimulus", "motivation", "attitude",
    "behavior", "behaviour", "bias", "memory", "emotion", "anxiety", "stress",
    "personality", "conscious", "consciousness", "mental", "psychological",
    "psychology", "instinct", "habit", "mood", "empathy", "trauma", "therapy",
    "therapist", "depression", "depressed", "intelligence", "perceive",
}

ENV_HINTS = (
    "climat", "pollut", "emiss", "sustain", "ecolog", "habitat", "carbon",
    "conserv", "recycl", "biodivers", "ozone", "ecosystem", "deforest",
)

ACADEMIC_TOPICS = {
    "education", "work", "technology", "science", "environment", "health",
    "society", "government", "economy", "media", "arts", "thinking", "history",
    "emotion", "nature",
}
A2_TOPICS = {
    "education", "science", "health", "environment", "society", "economy",
    "government", "technology", "thinking", "media", "arts", "history",
}

TIP_FIX = {
    "band": "band 作“成绩档”时与乐队无关。托福成绩一般说 score。",
    "trophy": "复数是 trophies。学术阅读里更常作名词。",
    "esthetic": "esthetic 是美式拼写，英式多为 aesthetic。托福写作用美式即可。",
    "needful": "这个词偏古旧。学术写作通常用 necessary。",
}

# Hand-written examples for the words a new learner actually meets first.
# (campus listening, zh, academic reading, zh)
OVERRIDES: dict[str, tuple[str, str, str, str]] = {
    "library": (
        "I reserved a study room at the library before the midterm.",
        "期中考试前，我在图书馆订了一间自习室。",
        "The library lends laptops so students can finish research when their own computers fail.",
        "图书馆出借笔记本电脑，方便学生在自己的电脑出故障时完成研究。",
    ),
    "student": (
        "Each student needs an ID card to enter the lab.",
        "每位学生都需要学生证才能进实验室。",
        "The survey asked every student how many hours they sleep during exam week.",
        "这项调查询问每位学生考试周睡多少小时。",
    ),
    "university": (
        "She chose the university because of its engineering program.",
        "她因为工程专业而选择了这所大学。",
        "The university requires first-year students to attend a short course on academic honesty.",
        "这所大学要求一年级学生参加一门关于学术诚信的短课。",
    ),
    "course": (
        "This course meets on Tuesdays in the science building.",
        "这门课每周二在科学楼上课。",
        "The course combines a weekly lecture with a smaller discussion section.",
        "这门课把每周一次的讲座和规模更小的讨论课结合在一起。",
    ),
    "professor": (
        "The professor posted the slides after class.",
        "教授课后上传了课件。",
        "The professor asked us to question the method before accepting the conclusion.",
        "教授让我们在接受结论之前先质疑研究方法。",
    ),
    "essay": (
        "His essay opened with a clear claim.",
        "他的文章以一个明确的主张开头。",
        "A strong essay explains the evidence before it states what the evidence implies.",
        "一篇好的文章会先解释证据，再说明证据意味着什么。",
    ),
    "method": (
        "We changed the method after the first trial failed.",
        "第一次试验失败后，我们改了方法。",
        "The passage contrasts a traditional method with a newer way to measure sleep.",
        "文章把一种传统方法和一种更新的睡眠测量方式做了对比。",
    ),
    "environment": (
        "Noise in the dorm affects the study environment.",
        "宿舍里的噪音会影响学习环境。",
        "The lecture linked a warming environment to changes in when plants flower.",
        "讲座把变暖的环境与植物开花时间的变化联系了起来。",
    ),
    "behavior": (
        "Sleep loss can change a student's behavior in class.",
        "睡眠不足会改变学生在课堂上的行为。",
        "Researchers recorded behavior during the task so they could compare the two groups.",
        "研究者记录了任务过程中的行为，以便比较两组受试者。",
    ),
    "lecture": (
        "Our morning lecture met in the science building.",
        "我们的早课讲座在科学楼进行。",
        "The lecture explained how glaciers record changes in climate over thousands of years.",
        "这场讲座解释了冰川如何记录数千年来的气候变化。",
    ),
    "campus": (
        "New students toured the campus before classes began.",
        "新生在开学前参观了校园。",
        "The reading describes how campus design can help students from different majors meet.",
        "这篇阅读描述了校园设计如何帮助不同专业的学生相遇交流。",
    ),
    "research": (
        "She joined a research group in her second year.",
        "她在二年级加入了一个研究小组。",
        "The passage compares two research methods used to study sleep in college students.",
        "文章比较了两种用于研究大学生睡眠的研究方法。",
    ),
    "experiment": (
        "The lab experiment took the whole afternoon.",
        "这次实验用了整个下午。",
        "Students had to say whether the experiment controlled every factor that could change the result.",
        "学生必须说明实验是否控制了每一个可能改变结果的因素。",
    ),
    "semester": (
        "The semester starts the last Monday in August.",
        "这学期从八月的最后一个星期一开始。",
        "Tuition for the semester is due before students can register for the next term.",
        "学生必须在注册下一学期之前缴清本学期学费。",
    ),
    "assignment": (
        "The assignment is due on Friday at noon.",
        "这份作业周五中午前截止。",
        "The assignment asks students to summarize the lecture and then challenge one claim.",
        "这份作业要求学生先概述讲座，再质疑其中一个主张。",
    ),
    "policy": (
        "The college changed its attendance policy this year.",
        "学院今年修改了出勤政策。",
        "The lecture asked whether public policy should weigh economic growth against environmental cost.",
        "讲座问到公共政策是否应当在经济增长与环境代价之间权衡。",
    ),
    "culture": (
        "The seminar compared student culture on two campuses.",
        "研讨课比较了两所学校的学生文化。",
        "Historians study how culture changes when people move and bring new customs with them.",
        "历史学者研究当人们迁徙并带去新习俗时，文化如何变化。",
    ),
    "argument": (
        "Her paper led with a clear argument.",
        "她的论文以一个清晰的论点开头。",
        "In the listening, the professor said the argument was weak because it rested on a single study.",
        "听力里，教授说这个论点站不住，因为它只依赖一项研究。",
    ),
    "conclusion": (
        "The conclusion should follow from the evidence.",
        "结论应当从证据中得出。",
        "The author reached a conclusion that later studies have only partly supported.",
        "作者得出的结论只得到了后来研究的部分支持。",
    ),
    "affect": (
        "Lack of sleep can affect your score on a quiz.",
        "睡眠不足会影响你在小测中的成绩。",
        "The study measured how screen time can affect attention during an evening lecture.",
        "这项研究测量了屏幕时间如何影响晚间讲座中的注意力。",
    ),
    "effect": (
        "We measured the effect of caffeine on focus.",
        "我们测量了咖啡因对专注力的影响。",
        "A small sample can hide the real effect and make a weak result look important.",
        "样本太小会掩盖真实影响，让一个微弱的结果看起来很重要。",
    ),
    "benefit": (
        "Office hours are a real benefit for new students.",
        "对新生来说，答疑时间是实实在在的好处。",
        "The passage weighs the benefit of the new transit line against its cost to nearby parks.",
        "文章权衡了新公交线路的好处及其对附近公园的代价。",
    ),
    "structure": (
        "Outline the structure before you draft the essay.",
        "起草文章之前，先列出结构。",
        "The lecture showed how the structure of a cell limits what can pass through its membrane.",
        "讲座说明了细胞的结构如何限制物质穿过细胞膜。",
    ),
    "process": (
        "Registration is a slow process in the first week.",
        "开学第一周，注册是一个缓慢的过程。",
        "The process described in the passage turns raw data into a chart the class can read.",
        "文章描述的过程把原始数据变成全班都能看懂的图表。",
    ),
    "identify": (
        "Identify the claim before you look at the chart.",
        "看图表之前，先识别出主张。",
        "Students learn to identify the assumption that an argument never states out loud.",
        "学生学习识别论点从未明说的那个假设。",
    ),
    "define": (
        "Define the term before you use it in the essay.",
        "在文章里使用这个术语之前，先给它下定义。",
        "Researchers define the variable so that another lab can repeat the same measurement.",
        "研究者界定变量，以便另一个实验室能重复同样的测量。",
    ),
    "achieve": (
        "She worked all term to achieve a higher grade.",
        "她整个学期都在努力，想取得更高的成绩。",
        "The city did not achieve its goal for cutting traffic during the study period.",
        "在研究期间，这座城市没有实现减少交通量的目标。",
    ),
    "require": (
        "The lab requires closed shoes and safety glasses.",
        "实验室要求穿包脚的鞋并戴护目镜。",
        "The scholarship will require students to report their progress at the end of each term.",
        "这份奖学金要求学生在每学期结束时报告进展。",
    ),
    "occur": (
        "The error can occur when the sample is too small.",
        "样本太小时，这个误差就可能出现。",
        "Such storms occur more often when ocean water stays warm later into the fall.",
        "当海水到秋末仍然偏暖时，这类风暴会更频繁地发生。",
    ),
    "analyze": (
        "We will analyze the survey before Friday's seminar.",
        "我们会在周五研讨课之前分析这份问卷。",
        "The lecture showed how to analyze a graph before trusting the speaker's conclusion.",
        "讲座演示了如何在相信讲者的结论之前先分析图表。",
    ),
    "evidence": (
        "The essay needs evidence, not just an opinion.",
        "这篇文章需要证据，不能只有观点。",
        "The professor said the evidence supports the claim but does not prove it.",
        "教授说这些证据支持该主张，但并不能证明它。",
    ),
    "significant": (
        "The difference was too small to be significant.",
        "这个差异太小，算不上显著。",
        "A significant result still needs a clear explanation of why the change happened.",
        "一个显著的结果仍然需要清楚解释变化为什么会发生。",
    ),
    "context": (
        "Read the sentence in context before you choose.",
        "选择之前，先在上下文里读这个句子。",
        "The meaning of the term shifts with the context of the discipline that uses it.",
        "这个术语的含义会随使用它的学科语境而变化。",
    ),
    "factor": (
        "Cost was the main factor in their decision.",
        "费用是他们做决定时的主要因素。",
        "The study isolated one factor so the others would not confuse the result.",
        "这项研究分离出一个因素，以免其他因素干扰结果。",
    ),
    "concept": (
        "The concept is easier with a concrete example.",
        "有了具体例子，这个概念就更容易理解。",
        "The lecture built the concept step by step from an everyday campus situation.",
        "讲座从一个日常的校园情境出发，一步步建立这个概念。",
    ),
    "approach": (
        "Her approach to the problem was simple and direct.",
        "她处理这个问题的方法简单直接。",
        "The two teams took a different approach and therefore measured different things.",
        "两组采用了不同的方法，因此测量的东西也不一样。",
    ),
    "data": (
        "Back up the data before you leave the lab.",
        "离开实验室之前先备份数据。",
        "The data in the chart come from one campus and may not describe other colleges.",
        "图表中的数据来自一所学校，未必能描述其他大学。",
    ),
    "assume": (
        "Do not assume the graph starts at zero.",
        "不要假定这张图的起点是零。",
        "Readers may assume a cause when the passage only shows that two trends happened together.",
        "文章只说明两种趋势同时出现时，读者却可能假定其中有因果关系。",
    ),
    "interpret": (
        "Interpret the result before you write the discussion.",
        "写讨论部分之前，先解释结果。",
        "Two scholars can interpret the same passage and still defend different claims.",
        "两位学者可以解释同一段文字，却仍然为不同的主张辩护。",
    ),
    "evaluate": (
        "Evaluate the source before you cite it.",
        "引用之前先评估来源。",
        "The assignment asks you to evaluate the method, not only to praise the finding.",
        "这份作业要求你评估方法，而不是只称赞研究发现。",
    ),
    "bias": (
        "A small sample can hide a serious bias.",
        "样本太小会掩盖严重的偏差。",
        "The professor warned that personal bias can shape which studies a writer chooses to cite.",
        "教授提醒，个人偏见会影响作者选择引用哪些研究。",
    ),
    "psychology": (
        "She is taking an introductory psychology course.",
        "她在上一门心理学入门课。",
        "The psychology lecture compared how memory works in the lab and in everyday life.",
        "这节心理学讲座比较了记忆在实验室和日常生活中的运作方式。",
    ),
    "perspective": (
        "The discussion added a historical perspective.",
        "这次讨论补充了一个历史视角。",
        "A second perspective can show a limit in the theory that insiders no longer notice.",
        "第二个视角能揭示圈内人已经注意不到的理论局限。",
    ),
    "consequence": (
        "One consequence of the policy is longer commutes.",
        "这项政策的一个后果是通勤时间变长。",
        "The author treats the drought as a consequence of warmer seasons, not as an isolated event.",
        "作者把这场干旱视为暖季的后果，而不是孤立事件。",
    ),
    "abstract": (
        "The idea is too abstract without an example.",
        "没有例子的话，这个想法太抽象了。",
        "An abstract of the paper states the question, the method, and the main result.",
        "论文摘要会写明问题、方法和主要结果。",
    ),
    "theory": (
        "The professor introduced the theory with a simple case.",
        "教授用一个简单案例介绍了这个理论。",
        "A useful theory lets researchers predict what a new experiment should find.",
        "一个有用的理论能让研究者预测新实验应当发现什么。",
    ),
    "hypothesis": (
        "State the hypothesis before you collect the data.",
        "收集数据之前先写明假说。",
        "The hypothesis predicted a larger effect in the group that slept less than six hours.",
        "这个假说预测，睡眠少于六小时的那一组会出现更大的效应。",
    ),
}

INTRANS = {
    "occur", "arise", "exist", "vary", "differ", "emerge", "disappear", "remain",
    "appear", "seem", "happen", "rise", "fall", "increase", "decrease", "decline",
    "grow", "shrink", "persist", "evolve", "fluctuate", "coincide", "matter",
    "continue", "cease", "proceed", "intervene", "interact", "overlap", "succeed",
    "fail", "tend", "graduate", "flourish", "diminish", "vanish", "fade",
    "intensify", "weaken", "worsen", "collapse", "recover", "thrive", "linger",
    "recur", "ensue", "prevail", "endure", "expire", "elapse", "subside",
    "stagnate", "soar", "plummet", "surge", "dwindle", "multiply", "diverge",
    "converge", "coexist", "predominate", "arise", "result",
}

VERB_PREP = {
    "depend": "on", "rely": "on", "consist": "of", "belong": "to", "respond": "to",
    "react": "to", "refer": "to", "participate": "in", "specialize": "in",
    "approve": "of", "object": "to", "insist": "on", "cope": "with", "comply": "with",
    "interfere": "with", "stem": "from", "account": "for", "relate": "to",
    "correspond": "to", "correlate": "with", "concentrate": "on", "elaborate": "on",
    "adhere": "to", "conform": "to", "resort": "to", "amount": "to", "deal": "with",
    "agree": "with", "disagree": "with", "consent": "to", "aspire": "to",
    "subscribe": "to", "confess": "to",
}

SENTENCE_ADVERBS = {
    "however", "therefore", "moreover", "thus", "consequently", "nevertheless",
    "furthermore", "instead", "otherwise", "meanwhile", "hence", "accordingly",
    "nonetheless", "conversely", "besides", "indeed", "likewise", "similarly",
    "subsequently", "ultimately", "initially", "finally", "recently", "currently",
    "previously", "traditionally", "increasingly", "meanwhile", "whereas",
}

NOUN_SHORT = [
    ("The seminar spent ten minutes on {np}.", "研讨课花了十分钟讨论{zh}。"),
    ("Our professor introduced {np} in the first week.", "教授在第一周介绍了{zh}。"),
    ("I heard {np} mentioned in yesterday's lecture.", "我在昨天的讲座里听到了{zh}。"),
    ("The assignment asks us to explain {np}.", "这次作业要求我们解释{zh}。"),
    ("Office hours began with a question about {np}.", "答疑从关于{zh}的一个问题开始。"),
    ("The textbook opens with a short section on {np}.", "教材开头有一小节讲{zh}。"),
    ("During the review session, we returned to {np}.", "复习课上我们又回到了{zh}。"),
    ("The listening passage defines {np} with a campus example.", "听力材料用一个校园例子说明{zh}。"),
    ("My study group made a note card for {np}.", "学习小组为{zh}做了一张笔记卡。"),
    ("The quiz included a short item about {np}.", "小测里有一道关于{zh}的题。"),
    ("In the lab report, we had to name {np}.", "实验报告里我们必须写出{zh}。"),
    ("The teaching assistant paused to clarify {np}.", "助教停下来澄清{zh}。"),
    ("Write one sentence that uses {np} correctly.", "写一个正确使用{zh}的句子。"),
    ("The slides listed {np} next to a simple chart.", "课件把{zh}标在一张简单的图表旁边。"),
]

NOUN_LONG = [
    ("The reading argues that {np} shapes how researchers interpret evidence in {field}.", "这篇阅读认为，{zh}会影响研究者如何解释{field_zh}中的证据。"),
    ("A recent lecture connected {np} with a broader debate about {field}.", "最近的讲座把{zh}和关于{field_zh}的更广泛讨论联系了起来。"),
    ("Students compared {np} across two studies before writing their response.", "学生在写回答之前，比较了两项研究里的{zh}。"),
    ("The passage explains why {np} remains central to discussions of {field}.", "文章解释了为什么{zh}仍然处于{field_zh}讨论的核心。"),
    ("Researchers treat {np} as a starting point when they design a new study of {field}.", "研究者设计一项关于{field_zh}的新研究时，把{zh}当作起点。"),
    ("The author uses {np} to challenge an older explanation of change in {field}.", "作者用{zh}来挑战关于{field_zh}变化的一种旧解释。"),
    ("In the sample lecture, the professor showed how {np} can alter an experimental conclusion.", "在示例讲座中，教授说明了{zh}如何改变实验结论。"),
    ("Without a clear account of {np}, the argument about {field} is difficult to follow.", "如果讲不清{zh}，关于{field_zh}的论点就很难跟上。"),
    ("The chart is meaningful only after the class has defined {np}.", "只有全班先界定了{zh}，这张图才有意义。"),
    ("A campus survey used {np} to explain a pattern the college had noticed for years.", "一项校园调查用{zh}来解释学院多年来注意到的一种模式。"),
    ("The speaker warned that ignoring {np} would weaken any policy on {field}.", "讲者警告，忽视{zh}会削弱任何关于{field_zh}的政策。"),
    ("Later studies revised what scholars thought they knew about {np}.", "后来的研究修正了学者们对{zh}的原有认识。"),
    ("The discussion section returns to {np} and asks what the finding implies for {field}.", "讨论部分回到{zh}，并追问这一发现对{field_zh}意味着什么。"),
    ("Students who can explain {np} in their own words usually follow the rest of the lecture.", "能用自己的话解释{zh}的学生，通常跟得上讲座的其余部分。"),
]

VERB_SHORT = [
    ("In the seminar, students had to {w} the author's main claim.", "研讨课上，学生必须{zh}作者的主要论点。"),
    ("The lab group will {w} the survey before Friday.", "实验小组会在周五之前{zh}这份调查。"),
    ("Our professor told us to {w} the chart first.", "教授让我们先{zh}这张图表。"),
    ("To finish the paper, Maya had to {w} two sources.", "为了完成论文，Maya 必须{zh}两个来源。"),
    ("The assignment says to {w} one example from the lecture.", "作业要求{zh}讲座中的一个例子。"),
    ("We learned how to {w} evidence without stretching it.", "我们学习如何{zh}证据，而不把它夸大。"),
    ("Before you cite the study, {w} its method.", "引用这项研究之前，先{zh}它的方法。"),
    ("The teaching assistant showed us how to {w} the result.", "助教向我们演示如何{zh}这个结果。"),
    ("In office hours, we tried to {w} the confusing paragraph.", "答疑时，我们试着{zh}那段费解的文字。"),
    ("The quiz will ask you to {w} a short passage.", "小测会要求你{zh}一段短文。"),
    ("Researchers {w} the data before they rewrite the discussion.", "研究者先{zh}数据，再改写讨论部分。"),
    ("A careful reader will {w} the claim, not just repeat it.", "细心的读者会{zh}这个主张，而不是只重复它。"),
]

VERB_LONG = [
    ("The lecture demonstrated how scholars {w} a claim when the evidence is incomplete.", "讲座演示了证据不完整时，学者如何{zh}一个主张。"),
    ("Students who can {w} the graph are less likely to accept a misleading conclusion.", "能够{zh}图表的学生，不太会接受一个误导性的结论。"),
    ("The passage asks readers to {w} the method before they trust the reported effect.", "文章要求读者在相信所报告的效应之前，先{zh}研究方法。"),
    ("A graduate seminar may spend an hour learning to {w} sources from different decades.", "研究生研讨课可能会花一小时学习{zh}来自不同年代的文献。"),
    ("The professor wanted the class to {w} the result and then say what it does not prove.", "教授希望全班{zh}这个结果，然后说明它不能证明什么。"),
    ("Good academic writing will {w} the assumption that the argument leaves unstated.", "好的学术写作会{zh}论点没有明说的那个假设。"),
    ("The lab report must {w} every unusual data point instead of hiding it in an average.", "实验报告必须{zh}每一个异常数据点，而不是把它藏进平均数里。"),
    ("Listeners in the sample talk had to {w} two explanations and choose the better one.", "示例讲话的听众必须{zh}两种解释，并选出更好的一种。"),
    ("If you cannot {w} the variable, another campus will not be able to repeat your study.", "如果你无法{zh}这个变量，另一所学校就无法重复你的研究。"),
    ("The author tries to {w} a familiar campus problem with evidence from a larger population.", "作者试图用来自更大人群的证据来{zh}一个熟悉的校园问题。"),
    ("Reviewers will {w} the paper again if the discussion ignores a competing explanation.", "如果讨论忽略了另一种竞争解释，审稿人会再次{zh}这篇论文。"),
    ("The worksheet tells you to {w} the lecture's claim in one sentence of your own.", "练习纸要求你用自己的一句话{zh}讲座中的主张。"),
]

VERB_PREP_SHORT = [
    ("Students learned to {w} {prep} the evidence in the passage.", "学生学习{zh}文章中的证据。"),
    ("The result seems to {w} {prep} the method, not the topic.", "结果似乎{zh}方法，而不是主题。"),
    ("Her paper tries to {w} {prep} a pattern the lecture only mentioned.", "她的论文试图{zh}讲座只提到过的一种模式。"),
    ("We were asked to {w} {prep} the claim with a clearer example.", "老师要求我们用更清楚的例子来{zh}这个主张。"),
    ("The seminar showed when researchers {w} {prep} a small sample.", "研讨课说明了研究者何时会{zh}小样本。"),
    ("You cannot {w} {prep} the chart until you read the caption.", "读图注之前，你无法{zh}这张图。"),
]

VERB_PREP_LONG = [
    ("The lecture explained why later studies {w} {prep} a different set of evidence.", "讲座解释了为什么后来的研究{zh}另一组证据。"),
    ("A careful discussion will {w} {prep} the limit of the data before offering advice.", "认真的讨论会在提出建议之前，先{zh}数据的局限。"),
    ("Students must {w} {prep} the theory when they design the next experiment.", "学生设计下一次实验时，必须{zh}这个理论。"),
    ("The author does not {w} {prep} one campus alone; the claim is about a wider trend.", "作者并不是只{zh}一所学校；这个主张针对的是更广泛的趋势。"),
    ("Office hours became useful once we could {w} {prep} the reading without guessing.", "一旦我们能够{zh}这篇阅读而不再猜测，答疑就有用了。"),
    ("The sample listening asks whether the policy will {w} {prep} students who work at night.", "这段示例听力问这项政策是否会{zh}夜间打工的学生。"),
]

INTRANS_SHORT = [
    ("The same pattern can {w} when the sample is too small.", "样本太小时，同样的模式就可能{zh}。"),
    ("Questions like this {w} in almost every research methods class.", "这类问题几乎在每一门研究方法课上都会{zh}。"),
    ("The problem began to {w} after the new rule took effect.", "新规定生效后，这个问题开始{zh}。"),
    ("Such results {w} across the studies cited in the lecture.", "讲座引用的各项研究里都{zh}了这样的结果。"),
    ("A gap like this will {w} if the groups are not comparable.", "如果两组无法比较，这样的缺口就会{zh}。"),
    ("The change did not {w} until the second semester.", "直到第二学期，这一变化才{zh}。"),
    ("Similar cases {w} whenever the instructions are unclear.", "说明不清楚时，类似情况就会{zh}。"),
    ("The effect can {w} even in a short lab session.", "即使在很短的实验课里，这种效应也可能{zh}。"),
]

INTRANS_LONG = [
    ("The passage explains why the pattern may {w} again if the campus repeats the survey.", "文章解释了如果学校重复这项调查，该模式为什么可能再次{zh}。"),
    ("Researchers noted that the difference did not {w} in the larger follow-up study.", "研究者指出，这一差异在规模更大的后续研究中并没有{zh}。"),
    ("The lecture asked when the trend would {w} if the college changed the deadline.", "讲座问到，如果学院更改截止日期，这一趋势何时会{zh}。"),
    ("A result that seems to {w} in one lab still needs a second test.", "一个看似会在某实验室{zh}的结果，仍然需要第二次检验。"),
    ("Students discussed why the problem continues to {w} in introductory courses.", "学生讨论了为什么这个问题在入门课程里持续{zh}。"),
    ("The author treats the shift as something that will {w} under warmer conditions.", "作者把这一转变视为在更暖的条件下会{zh}的现象。"),
    ("If the two measures {w} together, the chart should show a matching rise and fall.", "如果两种测量一起{zh}，图表就应显示出相应的升降。"),
    ("The speaker said the issue will {w} wherever class sizes stay this large.", "讲者说，只要班级规模仍然这么大，这个问题就会{zh}。"),
]

ADJ_SHORT = [
    ("She cited {art} {w} study in the first paragraph.", "她在第一段引用了一项{zh}的研究。"),
    ("The professor called the result {w} but still useful.", "教授说这个结果是{zh}的，但仍然有用。"),
    ("We need {art} {w} example before the seminar.", "研讨课之前我们需要一个{zh}的例子。"),
    ("The chart shows {art} {w} change over one semester.", "图表显示了一个学期内{zh}的变化。"),
    ("His feedback described the draft as {w}.", "他的反馈把这篇草稿描述为{zh}的。"),
    ("The quiz used {art} {w} case from campus life.", "小测用了一个来自校园生活的{zh}案例。"),
    ("A {w} finding can change the next experiment.", "一个{zh}的发现可以改变下一次实验。"),
    ("The class debated whether the effect was truly {w}.", "全班争论这个效应是否真的{zh}。"),
    ("Write {art} {w} sentence that a classmate can test.", "写一个同学可以检验的{zh}句子。"),
    ("The abstract highlights {art} {w} result from the lab.", "摘要强调了实验室里一个{zh}的结果。"),
]

ADJ_LONG = [
    ("The reading presents {art} {w} view of {field} and then tests it against new evidence.", "这篇阅读提出一种{zh}的{field_zh}观点，再用新证据加以检验。"),
    ("{art_cap} {w} result would change how the class interprets the study.", "一个{zh}的结果会改变全班对这项研究的解释。"),
    ("Students compared {art} {w} explanation with the one given in the lecture.", "学生把一种{zh}的解释和讲座中给出的解释做了比较。"),
    ("The professor asked which policy would be more {w} for students who work.", "教授问哪项政策对打工的学生更加{zh}。"),
    ("A lecture on {field} often begins with {art} {w} example the audience already knows.", "关于{field_zh}的讲座常常从一个听众已经知道的{zh}例子讲起。"),
    ("The passage warns that {art} {w} trend can be missed when the sample is small.", "文章警告，样本很小时，一种{zh}的趋势可能被漏掉。"),
    ("Reviewers wanted a more {w} account of how the data were collected.", "审稿人希望对数据收集过程有更{zh}的说明。"),
    ("The discussion became useful once someone offered {art} {w} alternative.", "有人提出一个{zh}的替代解释后，讨论才变得有用。"),
    ("Researchers described the relationship as {w} across the campuses they studied.", "研究者把他们所研究的各校之间的这一关系描述为{zh}的。"),
    ("Without {art} {w} definition, the rest of the argument is hard to grade.", "没有一个{zh}的定义，论点的其余部分就很难评分。"),
]

ADV_SHORT = [
    ("The professor explained the result {w} during the review.", "复习时，教授{zh}地解释了这个结果。"),
    ("She {w} revised the paragraph after office hours.", "答疑之后，她{zh}地修改了这一段。"),
    ("The two scores differ {w}, so the class should not ignore them.", "两个分数{zh}地不同，全班不应当忽视。"),
    ("He stated the claim {w} and then showed the chart.", "他{zh}地陈述了主张，然后展示了图表。"),
    ("The method has changed {w} since the first study.", "自第一项研究以来，这种方法已经{zh}地改变了。"),
    ("Read the caption {w} before you answer.", "作答之前先{zh}地读图注。"),
    ("The group worked {w} and still missed one variable.", "小组{zh}地工作，却仍然漏掉了一个变量。"),
    ("The author qualifies the claim {w} in the last paragraph.", "作者在最后一段{zh}地对主张做了限定。"),
]

ADV_LONG = [
    ("The lecture shows that the measure can change {w} when the instructions are rewritten.", "讲座表明，改写说明之后，这项测量会{zh}地发生变化。"),
    ("Students who prepare {w} are more likely to notice a flaw in the graph.", "{zh}准备的学生更可能发现图表中的缺陷。"),
    ("The passage says the cost rose {w}, even though enrollment stayed almost flat.", "文章说费用{zh}上升了，尽管入学人数几乎持平。"),
    ("A writer should signal {w} when a sentence is evidence and when it is only a guess.", "作者应当{zh}地标明哪一句是证据、哪一句只是猜测。"),
    ("Researchers checked the coding {w} so a second campus could repeat the study.", "研究者{zh}地检查了编码，以便另一所学校能重复这项研究。"),
    ("The speaker moved {w} from the example to the definition the quiz would require.", "讲者{zh}地从例子过渡到小测会要求的定义。"),
    ("If the groups differ {w}, the chart should make that difference visible at a glance.", "如果各组{zh}地不同，图表应当让这一差异一眼就能看见。"),
    ("The conclusion follows {w} only when every step of the method has been reported.", "只有方法的每一步都被报告出来，结论才会{zh}地成立。"),
]

SENT_SHORT = [
    ("{W}, the study reached a different conclusion.", "{zh}，这项研究得出了不同的结论。"),
    ("{W}, the class should look at the chart again.", "{zh}，全班应当再看一次图表。"),
    ("{W}, one campus is not enough to settle the question.", "{zh}，只有一所学校并不足以解决这个问题。"),
    ("{W}, the author qualifies the claim in the final paragraph.", "{zh}，作者在最后一段对主张做了限定。"),
    ("{W}, the lab report needs a clearer definition.", "{zh}，实验报告需要一个更清楚的定义。"),
    ("{W}, students asked for the slides after the lecture.", "{zh}，学生们在讲座后索要了课件。"),
]

SENT_LONG = [
    ("{W}, the evidence from a single semester cannot support a policy for the whole college.", "{zh}，仅一个学期的证据不足以支持面向全院的政策。"),
    ("{W}, a significant result still needs an explanation of why the change happened.", "{zh}，一个显著的结果仍然需要解释变化为什么发生。"),
    ("{W}, the lecture treats the two trends as related rather than identical.", "{zh}，讲座把这两种趋势视为相关，而不是同一件事。"),
    ("{W}, readers should separate what the passage proves from what it only suggests.", "{zh}，读者应当区分文章证明了什么、又仅仅暗示了什么。"),
    ("{W}, later work revised the claim without throwing out the original data.", "{zh}，后来的研究修正了主张，但没有抛弃原始数据。"),
    ("{W}, the example from campus life is there to make an abstract idea easier to test.", "{zh}，校园生活的例子是为了让一个抽象想法更容易检验。"),
]

FUNC_SHORT = [
    ("In academic prose, writers use {w} to join two ideas precisely.", "在学术写作中，作者用 {w} 把两个意思准确地连起来。"),
    ("The lecture paused on the word {w} and showed how it changes a claim.", "讲座在 {w} 这个词上停了一下，并说明它如何改变一个主张。"),
    ("Notice {w} in the sentence; it tells you how the ideas are related.", "注意句中的 {w}，它告诉你这些意思如何关联。"),
    ("The worksheet asks you to replace {w} and say whether the meaning shifts.", "练习纸要求你替换 {w}，并说明意思是否改变。"),
]

FUNC_LONG = [
    ("A small word like {w} can decide whether a sentence states a cause or only a time order.", "像 {w} 这样的小词，可以决定一个句子是在陈述原因，还是只是时间顺序。"),
    ("The professor highlighted {w} because students often skip it and then miss the author's point.", "教授标出了 {w}，因为学生常常跳过它，于是错过作者的意思。"),
    ("When you paraphrase, keep the relation that {w} signals, even if you change the other words.", "改写时，即使换掉其他词，也要保留 {w} 所表示的关系。"),
    ("The listening question turns on {w}, so the rest of the sentence is only context.", "这道听力题的关键在 {w}，句子的其余部分只是语境。"),
]


def _pick_two(items: list, key: str):
    h = int(hashlib.sha1(key.encode()).hexdigest()[:8], 16)
    i = h % len(items)
    j = (i + 1 + (h % (len(items) - 1))) % len(items)
    return items[i], items[j]


def _fill(template: str, **kw: str) -> str:
    out = template
    for k, v in kw.items():
        out = out.replace("{" + k + "}", v)
    return out


def gloss_of(entry: dict) -> str:
    parts = re.split(r"[；;]", entry["senses"][0]["zh"])
    cands = []
    for p in parts:
        p = re.sub(r"（[^）]*）", "", p)
        p = p.replace("…", "").replace("...", "").strip(" ，,、")
        if p.startswith("给"):
            p = p[1:].strip()
        if p and len(p) <= 8 and not re.search(r"[A-Za-z0-9]", p):
            cands.append(p)
    if not cands:
        return "该词"
    cands.sort(key=len)
    return cands[0]


def pos_of(entry: dict) -> str:
    p = (entry["senses"][0].get("pos") or "").lower().strip().rstrip(".")
    if p.startswith("adv"):
        return "adv"
    if p.startswith("adj"):
        return "adj"
    if p.startswith("v"):
        return "v"
    if p.startswith("n"):
        return "n"
    if p.startswith("prep"):
        return "prep"
    if p.startswith("conj"):
        return "conj"
    return "other"


def article(word: str) -> str:
    w = word.lower()
    if w[:1] in "aeiou" or w.startswith(("honest", "hour", "honor")):
        return "an"
    return "a"


def _phrases(entry: dict) -> list[tuple[str, str]]:
    w = entry["w"].lower()
    found = []
    for c in entry.get("col") or []:
        if "｜" not in c:
            continue
        en, zh = c.split("｜", 1)
        en, zh = en.strip(), zh.strip()
        if en and zh and re.search(rf"(?i)\b{re.escape(w)}\b", en):
            found.append((en, zh))
    return found


def _lemma_leads(phrase: str, lemma: str) -> bool:
    first = re.split(r"[\s/]+", phrase.strip())[0].lower().strip(".,;:")
    return first == lemma


_LEAD_VERBS = {
    "be", "being", "been", "is", "are", "was", "were", "do", "does", "did",
    "have", "has", "had", "get", "gets", "make", "makes", "take", "takes",
    "give", "gives", "go", "goes", "come", "comes", "put", "keep", "let",
    "see", "look", "bring", "write", "lay", "pay", "run", "hold", "leave",
    "find", "show", "tell", "ask", "use", "try", "start", "stop", "help",
    "want", "need", "seem", "feel", "become", "set", "turn", "call", "sit",
    "stand", "live", "play", "work", "move", "open", "close", "read", "hear",
    "pass", "spread", "deliver", "lie", "remain", "stay", "fall", "reach",
    "meet", "win", "lose", "break", "cut", "send", "build", "draw", "raise",
    "drop", "fill", "cover", "join", "cause", "avoid", "enjoy", "include",
    "provide", "offer", "describe", "explain", "discuss", "suggest", "learn",
    "study", "teach", "change", "happen", "rest", "lay", "gain", "lose",
}


def _score_phrase(phrase: str, pos: str, lemma: str) -> int:
    if any(x in phrase for x in ("……", "...", "sb.", "sth.")):
        return -5
    words = re.findall(r"[a-z']+", phrase.lower())
    if not words:
        return -5
    score = 0
    if pos == "v":
        score += 6 if words[0] == lemma else -4
        if "someone" in words or "something" in words:
            score -= 1
        if words[0] in {"be", "being", "been"}:
            score -= 3
    elif pos == "adv":
        score += 5 if words[0] == lemma else -2
        if lemma in SENTENCE_ADVERBS:
            score -= 2
    else:
        dets = {"a", "an", "the", "this", "that", "these", "those", "his", "her", "their", "its", "our", "my", "some", "any", "no"}
        preps = {"in", "on", "at", "of", "for", "to", "with", "by", "from", "about", "into", "over", "under", "as", "between", "without", "within", "during", "through", "per", "via"}
        if words[0] in _LEAD_VERBS or words[0] in preps:
            score -= 6
        if lemma in words and words[0] not in _LEAD_VERBS and words[0] not in preps:
            score += 4
        if words[-1] == lemma or words[-1].rstrip("s") == lemma or words[-1].startswith(lemma):
            score += 2
        for i, word in enumerate(words):
            if word in dets and i > 0 and words[i - 1] not in dets:
                score -= 6
                break
        if "someone" in words or "something" in words:
            score -= 2
    return score


def _choose(items: list[tuple[str, str]], key: str) -> tuple[str, str]:
    h = int(hashlib.sha1(key.encode()).hexdigest()[:8], 16)
    return items[h % len(items)]


def examples_for(entry: dict, topic: str) -> list[dict]:
    """Campus line plus a longer academic line.

    Real collocations carry the grammar, so the sentence stays natural for
    that lemma instead of forcing every verb into the same object frame.
    """
    ov = OVERRIDES.get(entry["id"])
    if ov:
        return [{"en": ov[0], "zh": ov[1]}, {"en": ov[2], "zh": ov[3]}]
    field, field_zh = TOPIC_FIELD.get(topic, ("academic study", "学术研究"))
    w = entry["w"]
    wl = w.lower()
    zh = gloss_of(entry)
    pos = pos_of(entry)
    phrases = _phrases(entry)
    ranked = sorted(phrases, key=lambda p: _score_phrase(p[0], pos, wl), reverse=True)
    best_score = _score_phrase(ranked[0][0], pos, wl) if ranked else -5
    phrase, pzh = ranked[0] if ranked and best_score >= 3 else (w, zh)
    kw = {"phrase": phrase, "pzh": pzh, "field": field, "field_zh": field_zh, "w": w, "zh": zh, "W": w[:1].upper() + w[1:]}

    if best_score < 3 and not (pos == "adv" and wl in SENTENCE_ADVERBS):
        short = [
            ("The professor explained {w} with a short example from campus.", "教授用一个简短的校园例子解释了{zh}。"),
            ("After the lecture, we used {w} in a sentence of our own.", "讲座之后，我们在自己的句子里用了{zh}。"),
            ("I wrote {w} on a note card with its meaning.", "我把{w}和它的意思写在了笔记卡上。"),
            ("The quiz expected us to recognize {w} in a lecture clip.", "小测要求我们在一段讲座录音里认出{zh}。"),
        ]
        long = [
            ("A reading on {field} uses {w} when the author sets up the main claim.", "一篇关于{field_zh}的阅读在提出主要主张时用到了{zh}。"),
            ("Students who can explain {w} usually follow the rest of a lecture on {field}.", "能解释{zh}的学生，通常跟得上一节关于{field_zh}的讲座。"),
            ("The sample listening brings up {w} while discussing evidence about {field}.", "示例听力在讨论关于{field_zh}的证据时提到了{zh}。"),
        ]
    elif pos == "adv" and wl in SENTENCE_ADVERBS:
        short = [
            ("{W}, the class checked the chart a second time.", "{zh}，全班又核对了一次图表。"),
            ("{W}, one campus is not enough to settle the question.", "{zh}，只有一所学校并不足以回答这个问题。"),
            ("{W}, the author limits the claim in the final paragraph.", "{zh}，作者在最后一段限定了这个主张。"),
            ("{W}, the lab report still needs a clearer definition.", "{zh}，实验报告仍然需要一个更清楚的定义。"),
        ]
        long = [
            ("{W}, evidence from a single semester cannot support a policy for the whole college.", "{zh}，仅一个学期的证据不足以支持面向全院的政策。"),
            ("{W}, the lecture treats the two trends as related rather than identical.", "{zh}，讲座把这两种趋势视为相关，而不是同一回事。"),
            ("{W}, readers should separate what the passage proves from what it only suggests.", "{zh}，读者应当区分文章证明了什么，又仅仅暗示了什么。"),
        ]
    elif pos == "v" and _lemma_leads(phrase, wl):
        short = [
            ("The professor asked us to {phrase}.", "教授让我们{pzh}。"),
            ("Before Friday's seminar, our group has to {phrase}.", "周五研讨课之前，我们小组必须{pzh}。"),
            ("The lab instructions say to {phrase}.", "实验说明要求{pzh}。"),
            ("In office hours we practiced how to {phrase}.", "答疑时我们练习如何{pzh}。"),
            ("The assignment is to {phrase}, then say why it matters.", "作业是先{pzh}，再说明它为什么重要。"),
            ("I heard the lecturer {phrase} during the example.", "我听到讲者在举例时{pzh}。"),
        ]
        long = [
            ("A lecture on {field} showed why researchers {phrase} before they publish.", "关于{field_zh}的讲座说明了研究者为什么在发表之前要{pzh}。"),
            ("The passage says students who can {phrase} follow the argument more easily.", "文章说，能够{pzh}的学生更容易跟上论点。"),
            ("When the class discussed {field}, the speaker told us to {phrase}.", "全班讨论{field_zh}时，讲者让我们{pzh}。"),
            ("Careful notes from the talk include a reminder to {phrase}.", "听课笔记里写着要记得{pzh}。"),
            ("The reading asks you to {phrase} and then check a second source.", "这篇阅读要求你{pzh}，然后再核对第二个来源。"),
            ("In the sample listening, the professor pauses to {phrase}.", "在示例听力里，教授停下来{pzh}。"),
        ]
    elif pos == "adv" and _lemma_leads(phrase, wl) and phrase.lower() != wl:
        short = [
            ("The lab manual says to {phrase} before you record the number.", "实验手册要求先{pzh}，再记下数字。"),
            ("In the methods section, students learn to {phrase}.", "在方法部分，学生学习{pzh}。"),
            ("The professor told us to {phrase} and then compare notes.", "教授让我们{pzh}，然后比较笔记。"),
        ]
        long = [
            ("A lecture on {field} asks the class to {phrase} before trusting a chart.", "关于{field_zh}的讲座要求全班在相信图表之前先{pzh}。"),
            ("The reading shows why a careful writer will {phrase} when the evidence is thin.", "这篇阅读说明，证据不足时，谨慎的作者会{pzh}。"),
            ("Students who {phrase} are less likely to misread the lecture.", "能够{pzh}的学生不太会误读这场讲座。"),
        ]
    else:
        short = [
            ("The seminar spent a few minutes on {phrase}.", "研讨课花了几分钟讨论{pzh}。"),
            ("I copied {phrase} into my lecture notes.", "我把{pzh}抄进了课堂笔记。"),
            ("The quiz had a short question about {phrase}.", "小测里有一道关于{pzh}的简答题。"),
            ("Our professor circled {phrase} on the slide.", "教授在幻灯片上圈出了{pzh}。"),
            ("The textbook introduces {phrase} in the first chapter.", "教材在第一章介绍了{pzh}。"),
            ("Office hours began with {phrase}.", "答疑从{pzh}开始。"),
        ]
        long = [
            ("The reading connects {phrase} with a larger point about {field}.", "这篇阅读把{pzh}和关于{field_zh}的一个更大的问题联系起来。"),
            ("In the lecture on {field}, everyone remembered the example of {phrase}.", "在关于{field_zh}的讲座里，大家都记得{pzh}这个例子。"),
            ("Students compared two sources that both discuss {phrase}.", "学生比较了两份都讨论{pzh}的材料。"),
            ("The author returns to {phrase} when explaining the conclusion.", "作者在解释结论时又回到了{pzh}。"),
            ("A campus survey used {phrase} to explain a pattern in {field}.", "一项校园调查用{pzh}来解释{field_zh}中的一种模式。"),
            ("The listening passage defines the discussion around {phrase}.", "这段听力材料围绕{pzh}展开说明。"),
        ]
    a = _choose(short, entry["id"] + "|s")
    b = _choose(long, entry["id"] + "|l")
    ex = [
        {"en": _fill(a[0], **kw), "zh": _fill(a[1], **kw)},
        {"en": _fill(b[0], **kw), "zh": _fill(b[1], **kw)},
    ]
    for item in ex:
        if wl not in item["en"].lower():
            item["en"] = f"The lecture uses {w} when it discusses {field}."
            item["zh"] = f"讲座在讨论{field_zh}时用到了{zh}。"
    return ex


def assign_topic(src_topic: str, word: str, wid: str) -> str:
    wl = word.lower()
    if wid in CAMPUS_IDS or wl in CAMPUS_IDS:
        return "campus"
    if wid in PSYCH_IDS or wl in PSYCH_IDS or src_topic == "emotion":
        return "psychology"
    if src_topic == "thinking":
        if any(k in wl for k in ("cognit", "psych", "emot", "behav", "memor")):
            return "psychology"
        return "lecture"
    if src_topic == "education":
        return "lecture"
    if src_topic in {"science"}:
        return "natural"
    if src_topic == "nature":
        if any(h in wl for h in ENV_HINTS):
            return "environment"
        return "natural"
    if src_topic == "environment":
        return "environment"
    if src_topic == "health":
        return "health"
    if src_topic == "society":
        return "social"
    if src_topic == "government":
        return "government"
    if src_topic in {"economy", "work"}:
        return "business"
    if src_topic == "technology":
        return "technology"
    if src_topic == "arts":
        return "arts"
    if src_topic == "media":
        return "media"
    if src_topic == "history":
        return "history"
    if src_topic in {"city", "daily", "travel", "sport"}:
        return "campus"
    return "lecture"


def clean_tip(tip: str, wid: str) -> str:
    if wid in TIP_FIX:
        return TIP_FIX[wid]
    tip = (tip or "").strip()
    tip = tip.replace("雅思", "托福").replace("IELTS", "TOEFL").replace("ielts", "TOEFL")
    return tip


def include_source(entry: dict) -> bool:
    wid = entry["id"]
    if wid in DENY or not entry.get("w") or entry["w"][:1].isupper():
        return False
    if wid in ALLOW:
        return True
    topic = entry.get("topic")
    cefr = entry.get("cefr")
    if cefr in {"B1", "B2", "C1", "C2"} and topic in ACADEMIC_TOPICS:
        if topic == "nature" and cefr == "B1":
            return False
        return True
    if cefr == "A2" and topic in A2_TOPICS:
        return True
    return False
