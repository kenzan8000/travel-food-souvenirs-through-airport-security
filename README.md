# Travel food souvenirs through airport security

An agent skill for trips. Tell it where you are shopping and which country you are
flying to, and it lists the local food souvenirs worth buying at a supermarket or local
shop that can go in your hand luggage and are allowed into that country. The agent
reads posts by residents and people who travelled there, picks what they recommend,
checks each item against the carry-on liquids rule and the destination's customs
rules, looks up the details, and shows the list in the chat.

The carry-on check uses the strict rule: liquids, gels, pastes and spreads only in
containers of 100 ml or less, all in one 1 L clear bag. So jam, honey, sauces and soft
cheese in normal sizes are left out, and the list says why. Alcohol is not included.

The output is laid out for reading on a phone, with no wide tables. It starts with the
travel rules for the trip. Souvenirs come next, with a short numbered overview grouped
by category and then a card per item. Items that were left out follow, with reasons.
Each card has:

| Field | Content |
| --- | --- |
| Photo | Official product image, Open Food Facts, Wikimedia Commons, or a source post's photo, checked to embed from another site |
| Name | Local name, with your language's name when it helps |
| Size and price | Typical pack and a rough local price |
| Carry-on | Why it passes the liquids rule, such as solid or a 50 g tube |
| Customs | Allowed or declare at the destination, with a link to the official page |
| Shelf life, packing | How long it keeps, and whether it is fragile, melts or smells |
| Made from, how it's made, taste | Ingredients and production |
| Look for on the label | Local words to find a style of item, such as *ruis* = rye |
| Sources | The posts that recommended it |

Widely sold brands are listed as exact products. Categories with many similar products,
such as salty liquorice or rye crisps, are listed as a style with label hints and
examples.

## What's in here

```
travel-food-souvenirs-through-airport-security/
  SKILL.md                      the skill: workflow and rules for the agent
  scripts/render_souvenirs.py   checks photos, filters items, prints Markdown
  examples/helsinki.json        sample input (Helsinki to Japan)
```

The script needs only Python 3.9 or newer, with no extra packages. Agents that cannot
run scripts can follow the manual path in `SKILL.md`.

## Install

`SKILL.md` uses the open Agent Skills format (a folder with a `SKILL.md` file and
`name`/`description` frontmatter). Copy or symlink the whole folder:

| Agent | Where |
| --- | --- |
| Claude Code | `~/.claude/skills/travel-food-souvenirs-through-airport-security/` |
| Claude apps (phone, web, desktop) | Zip the folder and upload it in the Skills section of Settings |
| Cursor | `~/.cursor/skills/travel-food-souvenirs-through-airport-security/` |
| Cursor Cloud Agents (phone, web) | Keep the folder in a repo the agent opens, under `.cursor/skills/` |
| Codex CLI | `~/.codex/skills/travel-food-souvenirs-through-airport-security/` |
| Anything else | Paste `SKILL.md` into the chat or the agent's custom instructions |

Then ask something like "What food souvenirs can I take home to Japan from Helsinki in
my hand luggage?" The agent needs web search and page reading.

Apps that cannot run scripts, or whose code sandbox has no internet access, still
work. The agent follows the manual path in `SKILL.md` and checks photos with its own
browsing tool.

## Running the script yourself

```bash
python3 scripts/render_souvenirs.py examples/helsinki.json
```

Options:

- `-o list.md`: write the Markdown to a file instead of stdout
- `--no-check-images`: use the first image URL without checking it
- `--no-proxy`: keep the original image URLs instead of GitHub image proxy URLs.
  Some chat apps, often on mobile and web, only show images from a short list of
  trusted hosts such as `camo.githubusercontent.com`; without the proxy, photos may
  not show there.
  `GITHUB_TOKEN` or `GH_TOKEN` raises GitHub's limit of 60 requests an hour.
- `--timeout 8`: seconds per image request

The script leaves out items with no used source, no carry-on reason or no customs
status, and moves items marked `banned` to the Left out section, warning about each.

The sample's source URLs are `example.com` placeholders and its prices are
illustrative; real runs use the actual posts, listings and official customs pages.
