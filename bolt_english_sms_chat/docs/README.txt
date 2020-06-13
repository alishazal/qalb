Title: BOLT English SMS/Chat
Authors: Zhiyi Song, Dana Fore, Stephanie Strassel, Haejoong Lee, Jonathan Wright

1. Introduction

This file contains documentation for the BOLT English SMS/Chat Corpus.
This corpus consists of naturally-occurring Short Message Service
(SMS) and Chat (CHT) data collected through data donations
and live collection involving native speakers of English.

The DARPA BOLT (Broad Operational Language Translation) Program developed
genre-independent machine translation and information retrieval systems. 
While earlier DARPA programs made significant strides in improving natural 
language processing capabilities in structured genres like newswire and 
broadcasts, BOLT was particularly concerned with improving translation
and information retrieval performance for less-formal genres with a special
focus on user-contributed content. 

LDC supported the BOLT Program by collecting informal data sources
including discussion forums, text messaging and chat in Chinese, Egyptian
Arabic and English. The collected data was translated and richly annotated
for a variety of tasks including word alignment, Treebanking, PropBanking,
and co-reference. LDC supported the evaluation of BOLT technologies by
post-editing machine translation system output and assessing information
retrieval system responses during annual evaluations conducted by NIST.

This corpus comprises the English training data collected for BOLT phase 2.
The corpus contains SMS and chat conversations between two or
more native English speakers. The bulk of the data in this release
consists of naturally-occurring, pre-existing SMS or chat message archives
donated by consented English speakers. Donated data is supplemented by new 
conversations among people who may or may not know one another, collected by
LDC specifically for BOLT using a custom collection platform. All data was 
obtained with the informed consent of the English speakers. Collected and
donated data was manually reviewed by LDC to exclude any messages that were
not in the target language, had potentially sensitive content, such as
personal identifying information (PII), or contained offensive content.
However, due to the informal nature of SMS/chat messages and subjective
nature of offensiveness, profanity or potentially offensive content may be
present in the data.

The corpus contains 18,429 conversations totaling 3,674,802 words across
375,967 messages. Section 4 below describes the data collection, auditing
process in detail.

2. Package structure

 README.txt                 - this file
 data/                      - source conversations

 docs/                      - directory containing package documents
   conversation0.2.1.dtd    - a DTD for .conv.xml files in the
				             data/ source directory
   gt24hrs.txt		    - list of conversations that contain a gap
                               between messages larger than 24 hours

   English_sms_chat_source_collection.tab
	                    - source file list with message and word counts


The filenaming convention for xml files is by conversation ID, which is

    <genre>_<lang>_<date>.<num>

where
    <genre>      is one of the genres: SMS and CHT
    <lang>       is ENG which stands for English
    <date>       is YYYYMMDD date of the first message of a conversation
    <num>        four-digit identifier


3. Contents

The table below shows the quantity of source data by genre:

Source:
+----------+----------+-------------+-------------+------------+
| language |   genre  | num_conv    | num_message | num_word   |
+----------+----------+-------------+-------------+------------+
| eng      |   cht    |      343    |    53,894   |   383,088  |
+----------+----------+-------------+-------------+------------+
| eng      |   sms    |   18,086    |   322,073   | 3,291,714  |
+----------+----------+-------------+-------------+------------+
| total    |   --     |   18,429    |   375,967   | 3,674,802  |
+----------+----------+-------------+-------------+------------+

The file English_sms_chat_source_collection.tab in the docs/ directory lists 
the inventory of documents with relevant quantities of messages and words.

4. BOLT SMS and Chat Collection Pipeline

The data in this release was collected using two methods: new collection via
LDC's collection platform, and donation of SMS or chat archives from BOLT
collection participants.  All data collected were reviewed manually to exclude
any messages/conversations that were not in the target language or that had
sensitive content, such as personal identifying information (PII).

4.1 LDC's SMS and Chat Collection Platform

For text messaging (SMS) collection, LDC's collection platform initiated
each session by sending a text message to a pair of consented participants,
introducing them to one another and inviting them to begin texting.  The
participants were native English speakers who were typically known
to one another but could be strangers.  Participants replied to the
initiating message to start the conversation.  The collection platform
relayed messages between the participants, so they experienced normal SMS
conversations.  Relayed messages were stored in LDC's database along with
participant and conversation metadata.

For chat messaging collection, LDC's chat robot sent a message to each
participant pair inviting them to start a session.  As with the SMS
collection, the participants were typically known to one another but could
be strangers.  The participants carried on a discussion and the robot
captured the conversation.  All conversations were stored in the collection
database along with participant and conversation metadata.

For both SMS and chat collections, there was no suggested topic and participants
were free to discuss any topic of their own choosing.

For SMS and chat data from live collection, a conversation was defined as
messages between a pair of participants within a 24-hour time frame.

4.2 SMS and Chat Collection from Donations

Consented, native English speaking participants followed LDC's 
instructions to create an archive of their SMS or chat data from their 
phone or computer and upload the archive to LDC's collection site. 
Participants had an opportunity to edit their archives prior to final 
upload to exclude any data they didn't want to donate.  Participants 
could delete entire messages and/or search their messages and redact 
specific content, using a simple GUI developed by LDC.  Redacted content 
was replaced with "#", preserving a one-to-one character mapping.

Post-processing of the uploaded archive included checking for duplication,
doing a simple automated language ID, and dividing the archive into
conversations.  An archive is first automatically divided into groups of
messages between particular sets of SMS/chat partners, and those message groups
are further subdivided into conversations every time a chat partner takes more 
than 24 hours to respond.  For example: an archive contains messages from 
Person A's phone.  It has conversations involving Person A, B and C chatting,
which we'll call them Group 1.  Person A is chatting separately with Person D; 
that's Group 2.  In Group 2, Person D has for some reason not replied to a 
message sent by Person A at 3pm yesterday, until 7pm today - that's 28 hours 
between messages, so Group 2 will have two conversations: those messages before 
3pm yesterday, and those after 7pm today.  So in the end, the archive from Person
A may be divided into multiple conversations. 

4.3 Auditing

After collection, each conversation was audited by LDC to ensure compliance
with language requirements and to flag:

  - any sensitive personal identifying information (PII) or offensive
    content
  - messages not in the target language
  - messages that are duplicates
  - auto-generated messages by Chat clients 

Messages/conversations not in the target language or containing PII or sensitive
content were removed from the corpus.  Messages that are predominantly in the
target language with occasional words in a different language are retained.  Note
that due to the informal nature of SMS/chat messages and subjective
nature of offensiveness, profanity or potentially offensive content may be
present in the data.

Messages consisting solely of auto-generated mark-up are retained in the
source files. For example:

        &lt;media omitted&gt;

5. Data Format

5.1 Source Data Conversation Format

The conv.xml files have one of the following formats:

<conversation id="conv_ID" medium="SMS|CHT" donated="true|false">
  <messages>
    <message id="mNNNN" time="YYYY-MM-DD HH:MM:SS TZ" participant="NNNNNN">
      <body> </body>
    </message>
  </messages>
</conversation>

Or

<conversation id="conv_ID" medium="SMS|CHT" donated="true|false">
  <messages>
    <message id="mNNNN" participant="NNNNNN" time="YYYY-MM-DD HH:MM:SS TZ">
      <body> </body>
    </message>
  </messages>
</conversation>

Medium value is either SMS or CHT (chat) and donated value is either true or
false where true indicates the conversation is from a donated archive and
false indicates the conversation was collected via LDC's SMS and chat 
collection platform.

Reserved characters such as "&" have been escaped using the standard format 
(e.g., "&amp;").  Proper ingesting of XML data requires an XML parsing
library.

The conversation_id is the file name minus the extension.  Each message has
message id, subject id, and date attributes and contains a message body.

For more information see docs/conversation0.2.1.dtd

6. Data Processing

Data was originally in a variety of formats, due to differences between
donated and collected data.  These formats were normalized; the content of
message bodies was not altered except to convert from UTF-16 to UTF-8,
replacing carriage returns with newlines, and removing apparently extraneous
newlines and quotes from the periphery of messages.  Internal newlines may
still occur when they are part of the content entered by the message sender.
Dates were converted to UTC, and the various original means of identifying
participants were converted to LDC subject IDs.

Participant IDs are assigned consistently within each donated archive, but LDC 
did not make any effort to normalize participant IDs across donated archives, 
as such information is not consistently available in the donations.

Message IDs were assigned, local to each conversation, starting at m0000,
based on the message order by date-time, which is also the order in which
messages are displayed in the output.  Note that if a message is deleted from
a conversation during auditing, the message number sequence will reflect the
deletion in that it will have non-contiguous numbering.  For example, if a
conversation originally contained 6 messages but the third message is deleted
during auditing because it contains PII, the conversation xml will contain
messages with IDs m0000, m0001, m0003, m0004, and m0005.  If participants
delete certain messages before uploading their archive, LDC has no way of
detecting this.  Therefore, donated conversations with message IDs whose
numbering is continuous will not necessary have continuity of content.

Conversation IDs were assigned based on medium, language, and the date of the
first message.

Donated messages were extracted from various applications and devices.  These
different sources use varying styles of newlines.  For simplicity and
consistency all newlines have been converted to use the single-character,
Unix-style line-feed, "\n."

7. Known Issues

7.1 Differences, some double-escapes in conv.xml Format

As described in section 5.1, there are two slightly different conv.xml formats
in this package.  Also, there are a small number of messages in which escaping
was mistakenly applied twice to characters like "&", producing a string like
'&amp;amp;'.  These were intentionally not normalized or corrected because
previously completed annotation of these source files relies on the original
character off-sets, including markup.

7.2 Private Use Area characters

Some conversations included a range of emoticon characters whose Unicode
code-point values occupy the "Private Use Area" of the Unicode character table.
These characters have been left in place.

7.3 Message Gaps of Greater than 24 Hours

Some conversations contain a gap between messages greater than 24 hours in
duration.  A list of these conversations may be found in docs/gt24hrs.tab.
There are two possible reasons behind the issue:

  - Some conversations were donated and processed before the 24-hour rule was 
    implemented.
  - During auditing, some messages were flagged and hence excluded, which then 
    increased the gap between surrounding messages to more than 24 hours

These files are being left as-is, containing an over-long gap within the 
message sequence, rather than being split into separate conversations. 

7.4 Placeholder Dates

Five filenames have a date of '19700101' and the xml metadata for these files
has 'time="1970-01-01 00:00:00 UTC"'.  This is not an accurate date or timestamp,
but a placeholder for files created from donated conversations that did not contain
time and date information.

8. Acknowledgments

This material is based upon work supported by the Defense Advanced Research
Projects Agency (DARPA) under Contract No. HR0011-11-C-0145. The content does
not necessarily reflect the position or the policy of the Government, and no
official endorsement should be inferred.

The authors acknowledge Kevin Walker, Jennifer Garland, Brian Gainor, Preston 
Cabe, Thomas Thomas, Brendan Callahan, Stephen Grimes, David Graff, Will Haun
and Ann Sawyer for their help and support in collection infrastructure, data
processing, delivery preparation and documentation. 

9. References

Zhiyi Song, Stephanie Strassel, Haejoong Lee, Kevin Walker, Jonathan Wright, 
Jennifer Garland, Dana Fore, Brian Gainor, Preston Cabe, Thomas Thomas, Brendan 
Callahan, Ann Sawyer. 2014. Collecting Natural SMS and Chat Conversations in 
Multiple Languages: The BOLT Phase 2 Corpus. LREC 2014: 9th Edition of the 
Language Resources and Evaluation Conference, Reykjavik, May 26-31.

10. Contact Information

  Zhiyi Song         <zhiyi@ldc.upenn.edu>      Collection Manager
  Stephanie Strassel <strassel@ldc.upenn.edu>   BOLT PI
  Dana Delgado       <foredana@ldc.upenn.edu>   Collection Coordinator
  Jonathan Wright    <jdwright@ldc.upenn.edu>   Technical Manager

-----------
README Created by Dana Delgado April 26,2018
