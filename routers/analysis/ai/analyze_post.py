from openai import OpenAI
from dotenv import load_dotenv
import os

ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(ENV_PATH)
print(OPENAI_API_KEY)

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY!")

client = OpenAI(api_key=OPENAI_API_KEY)


prompt = """
You are an investment analysis assistant. Your task is to process a collection of posts from investment subreddits, SeekingAlpha, and similar sources about a given stock. These posts contain investment theses and corresponding comments, including criticisms. Your goal is to extract clear, actionable investment points in a one-liner format. Follow these instructions:

Extract Investment Points:

Identify the key investment thesis or argument made about the stock.
Each point must be a short, one-sentence statement that clearly summarizes the core argument.
Do not provide a summary of the entire post—only extract individual investment points.
If a post does not contain any relevant investment points, return nothing.
Simplify and Shorten:

Use simple and direct language.
Remove unnecessary adjectives or descriptors.
For example, if the original point is "Neffy's needle-free epinephrine nasal spray targets a large market, offering a convenient alternative to traditional auto-injectors," simplify it to:
"Neffy's nasal spray targets large market, offers convenient alternative to traditional auto-injectors."
Output Format:

Present each investment point as a single, concise one-liner.
No bullet symbols or extra formatting are needed—simply output one investment point per line.
Your final output should be clear, concise, and structured so that an investor or trader can quickly understand the key arguments for or against the stock.
---

POST:

"""

def summarize_post(content: str):
    response = client.responses.create(
        model = "gpt-3.5-turbo",
        input = [
            {
                "role": "user",
                "content": prompt+content,
            }
        ]
    )

    return response.output_text

if __name__ == "__main__":

    test_content = """
    ARS Pharmaceuticals (NASDAQ:SPRY) is a biopharma company that's generally trying to address allergic reactions. In particular, they recently launched their star product called "Neffy," which is the first FDA-approved needle-free epinephrine. The interesting part about Neffy is that it's essentially just a nasal spray that delivers the same emergency treatment as traditional auto-injectors like the EpiPen. Currently, they're working on their rollout, aiming to gain market share in that large multibillion-dollar TAM. Neffy might also soon gain an indication expansion for other conditions like treatment-resistant chronic spontaneous urticaria [CSU]. And from a valuation angle, SPRY seems priced for growth, but I don't believe it trades at an unreasonable multiple just yet. So, I rate the stock a 'Buy' at these levels.

    A Convenient Nasal Spray Alternative
    First of all, ARS Pharmaceuticals is currently headquartered in California. They were founded in 2015, with a focus on severe allergic reactions that cause anaphylaxis. More recently, in August the FDA approved their Neffy nasal spray. This is technically an adrenaline or epinephrine nasal spray that's intended for emergency situations with allergic reactions. Similarly, the EU approved Neffy under the brand "EURneffy," and there are other regulatory submissions expected across other jurisdictions in 2025.

    For context, Type I allergic reactions can happen within minutes and could be life-threatening if left unchecked. This is why most patients prone to this condition often carry auto-injectors like the EpiPen in case they get a serious allergic episode. However, SPRY's nasal spray could be a much easier way to treat this condition, as it's just a simple inhaler that gives patients epinephrine treatment without needing an injection. And since these types of Type I reactions can happen with immediate exposure to allergens, it can be helpful for patients at risk of insect stings, bites, certain foods, or medications.

    Source: Corporate Presentation. January 2025.
    Corporate Presentation. January 2025.

    SPRY developed the drug and entered a license agreement with ALK to commercialize it outside the US, Australia, New Zealand, Japan, and China. SPRY is responsible for manufacturing and supplying the medication to ALK.

    Moreover, SPRY was developed, and it's marketed under a license agreement with ALK, which actually owns the rights outside the US, Australia, New Zealand, Japan, and China. Still, SPRY manufactures and supplies ALK with Neffy, so they still benefit from those sales. And Neffy has so far been a success as a "needle-free" alternative since its Q4 2024 launch. In the first few weeks since launch, they've generated over $7.1 million in sales, which also beat expectations.

    Source: Corporate Presentation. January 2025.
    Corporate Presentation. January 2025.

    Plus, the US TAM for this product is sizeable and estimated at roughly $3.0 billion as a prescription service segment. You see, healthcare providers often prescribe auto-injectors like the EpiPen for patients with severe allergies. But now, Neffy seems like a much more convenient alternative, so even if they capture a smaller market share than auto-injectors, it would still be massive for SPRY. There's also an adjacent TAM for Neffy with patients who have "injection aversion" that could be worth up to $7.0 billion if regulators approve it as an OTC medication.

    On top of that, SPRY believes that there are roughly 40 million patients in the US who suffer from Type I allergic reactions, but only 20 million are actually diagnosed. And if you include the 13.5 million patients who aren't currently prescribed epinephrine, it's evident that this is still a huge and largely untapped market. So, SPRY's current strategy is twofold: first, try to gain market share in the prescribed segment by marketing it closely with healthcare providers. In 2025 SPRY will launch an awareness campaign directed to patients and doctors to motivate them to transition to Neffy as its preferred option for allergy treatment.

    Source: Corporate Presentation. January 2025.
    Corporate Presentation. January 2025.

    And secondly SPRY wants to enhance Neffy's indications and potential as an OTC alternative that unprescribed patients can purchase with ease. Similarly, they're also working on growing Neffy's insurance coverage from 60% to 80%, which would only further expand its revenue potential.

    Neffy's Promise in CSU and Pediatric Markets
    As a side note, Neffy can also potentially gain another indication for CSU, which would bring in an additional peak sales of $2-$3 billion if SPRY succeeds. They currently have a Phase 2b trial planned for this indication in Q1 2025. Moreover, there are roughly 2 million diagnosed CSU patients, and 1 million are prescribed for this condition.

    So far, SPRY's data on CSU seems promising because there's notable relief of symptoms with Neffy compared to placebo and traditional antihistamines. In other words, Neffy could be used as an episodic treatment that reduces adverse effects and hospital visits. There's also an sNDA submitted for Neffy 1 mg targeted for children weighing 15 to 30 kg.

    Source: Corporate Presentation. January 2025.
    Corporate Presentation. January 2025.

    That particular PDUFA date is set for March 6, 2025, which I believe gives us yet another catalyst to look forward to with SPRY. And if it's approved, they could quickly begin commercializing it by Q2 2025. So overall, I think Neffy has massive blockbuster potential as long as management executes well going forward.

    SPRY Is Definitely Priced For Growth
    Besides, from a valuation angle, the company now has a respectable $1.2 billion market cap. And if we look at their balance sheet, they're actually relatively well capitalized. For context, they held $39.7 million in cash and $165.0 million in short-term investments as of Q3. So, in total, they have roughly $204.7 million in resources they can use to fund their R&D. Of course, they still have some cash burn of about $14.6 million per quarter. I got that figure by adding their CFOs and Net CAPEX.

    This would suggest a cash runway of approximately 14.0 quarters. But note that such a runway was back in Q3 or September 2024. By now, in February 2025, I calculate their runway is slightly shorter at 12.7 quarters, or about 3.2 years. So, evidently, the company seems to have ample resources for the next few years. Moreover, Seeking Alpha's dashboard also projects SPRY's revenue will jump substantially to $122.3 million in 2025.

    Source: Seeking Alpha.
    Seeking Alpha

    In my view, this jump is going to be largely on the back of Neffy, which, I think, will be on a growth curve for several years. Obviously, this still implies a somewhat high P/S of 9.8. For comparison, their sector's median P/S is much lower at just 3.6. So clearly, SPRY is pricing in substantial growth in the coming years. But this premium multiple actually seems reasonable when you realize that SPRY's YoY growth in 2025 will be a whopping 503.7%. On the other hand, their peers' median sales growth is just 7.4%, so the premium multiple seems more than justified, in my opinion.

    Source: TradingView.
    TradingView

    This is why I have to give SPRY a "Buy" rating at these levels, even though the stock has already made a significant move. But even though the stock is up nicely from the recent December lows by about 18.5%, it still remains down 28.5% from its yearly highs in 2024. So, I think there's still room to catch up, especially as revenues ramp up in 2025.

    But There Are Some Risks Worth Considering
    Obviously, SPRY's growth curve is probably just getting started with Neffy. However, let's not forget that rollouts have their challenges, and they also require investment. If they start missing their sales targets this year, their cash burn might be higher than expected, and it could become an issue if it only leads to an even worse cash burn.

    I would also mention that most of this sales growth rides on the assumption that they'll manage to increase insurance coverage going forward. But then again, this is also somewhat speculative, and if they fail at this, it could be a bit of a headwind for their revenue growth as well. Other than that, I lean pretty bullish on this new product. But I do believe they'll have to craft their sales narrative carefully against more traditional competitors like the EpiPen and auto-injectors in general.

    Source: Corporate Presentation. January 2025.
    Corporate Presentation. January 2025.

    Still, a nasal spray seems much more convenient in my view, so I think SPRY will be able to capture a meaningful market share of this market. For context, Epinephrine auto-injectors generated almost $1.5 billion in yearly revenues (2023) and are projected to reach $4.4 billion by 2032. So, there seems to be more than enough room for growth with SPRY's more

    convenient nasal spray alternative. Lastly, there still remains a bit of uncertainty tied to the FDA's decision on Neffy's 1mg sNDA, but I believe they'll ultimately give them the green light on this as well. Still, if that doesn't happen, the shares could sell off in response, so just be aware of that.

    Time To Be Bullish
    Overall, I feel SPRY is probably going to ramp up its sales quickly in 2025, and depending on how well it performs, we'll get a clearer idea of its actual growth potential once we see revenue figures at scale. But as it stands, I think their current market cap seems like it's not fully pricing in its potential for upside surprises with Neffy. And with their next earnings report coming up next month, I think it's worthwhile being bullish at these levels. So, while I admit there are some execution and competitive risks, I ultimately feel it's justified to give SPRY a 'Buy' rating.
    """
    print(summarize_post(test_content))