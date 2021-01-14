{\rtf1\ansi\ansicpg1252\cocoartf2576
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Monaco;}
{\colortbl;\red255\green255\blue255;\red10\green82\blue135;\red255\green255\blue255;\red47\green52\blue71;
\red0\green0\blue0;\red15\green114\blue1;\red251\green0\blue129;\red18\green139\blue2;\red109\green109\blue109;
\red0\green0\blue255;}
{\*\expandedcolortbl;;\cssrgb\c0\c40000\c60000;\cssrgb\c100000\c100000\c100000;\cssrgb\c23922\c26667\c34902;
\cssrgb\c0\c0\c0;\cssrgb\c0\c50980\c0;\cssrgb\c100000\c7843\c57647;\cssrgb\c0\c60000\c0;\cssrgb\c50196\c50196\c50196;
\cssrgb\c0\c0\c100000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28600\viewh15060\viewkind0
\deftab720
\pard\pardeftab720\sl374\partightenfactor0

\f0\fs34 \cf2 \cb3 \expnd0\expndtw0\kerning0
from\cf4  \cf5 gensim.summarization.summarizer \cf2 import\cf4  \cf5 summarize\cf4 \
\cf2 from\cf4  \cf5 gensim.summarization.textcleaner \cf2 import\cf4  \cf5 split_sentences\cf4 \
\'a0\
\'a0\
\cf2 def\cf4  \cf5 f(seq): \cf6 # Order preserving unique sentences - sometimes duplicate sentences appear in summaries\cf4 \
\'a0\'a0\'a0\'a0\cf5 seen \cf2 =\cf4  \cf7 set\cf5 ()\cf4 \
\'a0\'a0\'a0\'a0\cf2 return\cf4  \cf5 [x \cf2 for\cf4  \cf5 x \cf2 in\cf4  \cf5 seq \cf2 if\cf4  \cf5 x \cf2 not\cf4  \cf2 in\cf4  \cf5 seen \cf2 and\cf4  \cf2 not\cf4  \cf5 seen.add(x)]\cf4 \
\'a0\
\'a0\
\cf2 def\cf4  \cf5 summary(x, perc): \cf6 #x input document, perc: percentage of the original document to keep\cf4 \
\'a0\'a0\'a0\'a0\cf2 if\cf4  \cf7 len\cf5 (split_sentences(x)) > \cf8 10\cf5 :\cf4 \
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\cf5 test_summary \cf2 =\cf4  \cf5 summarize(x, ratio \cf2 =\cf4  \cf5 perc, split\cf2 =\cf9 True\cf5 )\cf4 \
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\cf5 test_summary \cf2 =\cf4  \cf10 '\\n'\cf5 .join(\cf7 map\cf5 (\cf7 str\cf5 , f(test_summary)))\cf4 \
\'a0\'a0\'a0\'a0\cf2 else\cf5 :\cf4 \
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\cf5 test_summary \cf2 =\cf4  \cf5 x\cf4 \
\'a0\'a0\'a0\'a0\cf2 return\cf4  \cf5 test_summary\cf4 \
\'a0\
\'a0\
\cf6 # Define the input\cf4 \
\cf5 mytxt \cf2 =\cf4  \cf6 """ The unnamed Narrator is a traveling automobile recall specialist who suffers from insomnia. When he is unsuccessful at receiving medical assistance for it, the admonishing doctor suggests he realize his relatively small amount of suffering by visiting a support group for testicular cancer victims. The group assumes that he, too, is affected like they are, and he spontaneously weeps into the nurturing arms of another man, finding a freedom from the catharsis that relieves his insomnia. He decides to participate in support groups of various kinds, always allowing the groups to assume that he suffers what they do. However, he begins to notice another impostor, Marla Singer, whose presence reminds him that he is attending these groups dishonestly, and this disturbs his bliss. The two negotiate to avoid their attending the same groups, but, before going their separate ways, Marla gives him her phone number.\cf4 \
\cf6 On a flight home from a business trip, the Narrator meets Tyler Durden, a soap salesman with whom he begins to converse after noticing the two share the same kind of briefcase. After the flight, the Narrator returns home to find that his apartment has been destroyed by an explosion. With no one else to contact, he calls Tyler, and they meet at a bar. After a conversation about consumerism, outside the bar, Tyler chastises the Narrator for his timidity about needing a place to stay. Tyler requests that the Narrator hit him, which leads the two to engage in a fistfight. The Narrator moves into Tyler\'92s home, a large dilapidated house in an industrial area of their city. They have further fights outside the bar on subsequent nights, and these fights attract growing crowds of men. The fighting eventually moves to the bar\'92s basement where the men form a club (\'93Fight Club\'94) which routinely meets only to provide an opportunity for the men to fight recreationally.\cf4 \
\cf6 Marla overdoses on pills and telephones the Narrator for help; he eventually ignores her, leaving his phone receiver without disconnecting. Tyler notices the phone soon after, talks to her and goes to her apartment to save her. Tyler and Marla become sexually involved. He warns the Narrator never to talk to Marla about him. More fight clubs form across the country and, under Tyler\'92s leadership (and without the Narrator\'92s knowledge), they become an anti-materialist and anti-corporate organization, Project Mayhem, with many of the former local Fight Club members moving into the dilapidated house and improving it.\cf4 \
\cf6 The Narrator complains to Tyler about Tyler excluding him from the newer manifestation of the Fight Club organization Project Mayhem. Soon after, Tyler leaves the house without notice. When a member of Project Mayhem is killed by the police during a botched sabotage operation, the Narrator tries to shut down the project. Seeking Tyler, he follows evidence of Tyler\'92s national travels. In one city, a Project Mayhem member greets the Narrator as Tyler Durden. The Narrator calls Marla from his hotel room and discovers that Marla also believes him to be Tyler. Tyler suddenly appears in his hotel room, and reveals that they are dissociated personalities in the same body. When the Narrator has believed himself to be asleep, Tyler has been controlling his body and traveling to different locations.\cf4 \
\cf6 The Narrator blacks out after the conversation, and when he awakes, he uncovers Tyler\'92s plans to erase debt by destroying buildings that contain credit card companies\'92 records. The Narrator tries to warn the police, but he finds that these officers are members of the Project. He attempts to disarm the explosives in a building, but Tyler subdues him and moves him to the uppermost floor. Held at gunpoint by Tyler, the Narrator realizes that, in sharing the same body with Tyler, he himself is actually in control holding \'93Tyler\'92s\'94 gun. The Narrator fires it into his own mouth, shooting through the cheek without killing himself. Tyler collapses with an exit wound to the back of his head, and the Narrator stops mentally projecting him. Afterward, Project Mayhem members bring a kidnapped Marla to him, believing him to be Tyler, and leave them alone. Holding hands, the Narrator and Marla watch as the explosives detonate, collapsing many buildings around them."""\cf4 \
\'a0\
\'a0\
\cf6 # Get the Summary\cf4 \
\cf5 mysummary \cf2 =\cf4  \cf5 summary(mytxt, \cf8 0.1\cf5 )\cf4 \
\'a0\
\cf7 print\cf5 (mysummary)\cf4 \
}