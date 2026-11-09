---
name: travel-food-souvenirs-through-airport-security
description: On a trip, list the local food souvenirs worth buying at a local supermarket or shop that can go in carry-on luggage through airport security (no liquids, gels or pastes over 100 ml) and are allowed into the destination country, sourced from first-hand writing by locals and travellers. Each item has a photo, pack size, a rough local price, carry-on and customs notes, shelf life, packing tips, and what it is made from and how. Use when the user wants food souvenirs, gifts or snacks to take home from a trip in hand luggage. The place and destination country may come later; if they are not given, ask for them in the chat.
---

# Food souvenirs through airport security

Turn a place name and a destination country into a list, shown in the chat, of local
food souvenirs the user can buy at a local shop and carry home in their hand luggage.
Every item comes from real posts by residents or people who travelled there, passes
the carry-on liquids rule, and is allowed into the destination country.

Favour what locals buy as gifts and what travellers say they brought home: packaged,
shelf-stable food from supermarkets, sweet shops, bakeries, delis and market stalls.
Leave out alcohol entirely.

The user is usually already on the trip, often reading on a phone, and wants the list
soon. Keep the research focused and the output narrow: no wide tables.

**A missing fact is better than a wrong fact. A missing link is better than a guessed
link.** Never invent sizes, prices, ingredients, rules or URLs.

These instructions are agent-neutral. "Search the web", "open the page" and "run the
command" mean whatever tools your environment provides. If you cannot run scripts,
follow the manual path in Step 9.

## Step 1: Ask for the place and the destination in the chat and wait

The skill needs two things: the **place** where the user is shopping, and the
**destination country** they are flying to (usually home).

- If the user's message names both, use them and go to Step 2.
- Otherwise, your whole reply is one short question in the chat, in the user's
  language, asking only for what is missing. For example:

  > Where are you shopping, and which country are you flying to? A city or region is
  > enough for the first, plus the country if the name could mean more than one place.

- Ask as ordinary chat text, then stop and wait. Do not search or guess first.
- If the place name is ambiguous (Portland, Victoria, San José), ask which one.
- Ask nothing else: not budget, number of gifts, diet or which airport.
- Note the **user's language** (the language they write in) and the **local
  language(s)** of the place. Write the list in the user's language; local names and
  terms come from the local language.

## Step 2: Find first-hand sources

Search in the user's language and the local language. When neither is English, also
search in English, which usually has more first-hand posts. Use several phrasings, for
example (translate and adapt them; the local-language ones here are Finnish):

- `<place> food souvenirs to bring home`, `<place> supermarket souvenirs`
- `what to buy at <country> supermarket to take home`, `<country> edible gifts`
- `<place> souvenirs hand luggage`, `what I brought home from <place>`
- local words for souvenir and gift: `tuliaiset`, `omiyage`, `Mitbringsel`, `recuerdo`
- local language: `parhaat tuliaiset Suomesta`, `suomalaiset herkut ulkomaille`
- forum and community threads (Reddit, local forums) when they contain detail

Open and read the posts, not just the search snippets. Aim for 3 to 5 distinct
first-hand sources; for small places accept however many genuinely exist.

**Keep** a source when it is first-person ("we brought back", "I always take this to
friends abroad"), shows the author was there (own photos, specific details), and has
an identifiable author or publication.

**Reject** shop and review aggregators, AI-generated or SEO listicles, pages with no
author, and content that only rewrites other sites. Log every source you opened, kept
or rejected, with a one-line reason.

## Step 3: Extract souvenirs

Collect the food the sources recommend buying in a shop and taking home. Skip what is
only sold in restaurants or must be eaten fresh.

Decide each item's `kind`:

- `product`: one specific, widely sold brand, for example Fazer Blue chocolate in
  Finnish shops. Use this when the sources name it and shoppers will find exactly that
  product.
- `style`: a category with many interchangeable products, for example rye crisps or
  salty liquorice. Describe what is popular, what to look for on the label, and give 1
  to 3 example products only if sources or retailer listings name them.

For each item record what the source authors said and the URL of every kept source
that mentions it. Merge duplicates across sources and keep all their URLs.

Give each item a `category`, such as sweets, savoury snacks, pantry and spices, or tea
and coffee. Use the same wording for items in the same category; the list is grouped
by it.

## Step 4: Apply the carry-on filter

This is a hard rule. The list is for hand luggage, checked with the strict liquids
rule: **every liquid, gel, paste, cream or spread must be in a container of 100 ml
(or 100 g) or less, and all of them together must fit in one clear 1 L bag.** Some
airports have relaxed this with new scanners, but rules change and differ by airport,
so the filter always uses the strict rule.

Keep only items that are:

- solid (chocolate, sweets, biscuits, crisps, dried fruit, tea, coffee beans or
  ground coffee, hard cheese, spices), or liquid, gel or paste in a container of 100
  ml/g or less that shops actually sell;
- in sealed factory packaging;
- fine without a fridge for the length of a trip.

Leave out jam, honey, spreads, soft or creamy cheese, yoghurt, sauces, syrups, oil,
mustard, fish or vegetables canned in liquid, and anything else that is liquid, gel or
paste and over 100 ml/g. If a famous item of this kind is also sold in a size of 100
ml/g or less, keep it and describe only that size. Leave out all alcohol.

Log every item the sources recommended strongly but the filter removed in `left_out`,
with the reason, so the user knows why a famous item is missing.

## Step 5: Check customs at the destination

Look up the destination country's rules for bringing food in for personal use, from
official sources only: the customs or agriculture authority's own pages. For example:
the EU's rules on personal imports of food from outside the EU, US CBP and USDA APHIS,
Japan's MAFF Animal and Plant Protection Service, Australia's DAFF, New Zealand's MPI.
If the place and destination share a single market (for example two EU countries),
say so and note any remaining limits.

For each item set `customs`:

- `status`: `allowed` (can be brought in without formalities), `declare` (allowed, but
  must be declared or is limited in amount), or `banned` (not allowed for travellers).
- `note`: one sentence in the user's language, such as "Meat products need an export
  inspection certificate, which shops do not provide."
- `source`: the URL of the official page that says so.

Meat and meat-containing products (including jerky, sausages, pâté and some
stock-flavoured snacks), dairy, eggs, fresh fruit and vegetables, seeds, nuts in the
shell and plants are the usual problems. Read the ingredient list: crisps flavoured
with real meat or a chocolate with a dairy filling can fall under a rule.

Remove items whose status is `banned` and log them in `left_out` with the reason. If
you cannot confirm the rule for an item, leave out `customs` and remove the item too;
the script drops items with no customs status.

## Step 6: Decide how many

There is no fixed number. Include what first-hand sources actually recommend and what
survives Steps 4 and 5, usually about 6 to 15 items; fewer for small places.

- Every item needs at least one kept source.
- Rank by how many independent sources mention it. Among similar items, prefer
  sturdy, light, long-lasting packs at everyday prices over fragile or expensive ones.
- List items in ranked order; the script groups them by `category` and keeps the rank
  within each group.

## Step 7: Fill in the details

Look up facts beyond the posts: the producer's site, Wikipedia (in both languages),
Wikidata, Open Food Facts and local retailer listings. Search retailer listings in the
local language; they give pack sizes, ingredients and prices.

- `pack_size`: net weight or volume of the common pack, such as `200 g bar`.
- `price`: a rough price in the local currency, such as `~3-4 EUR`. Rough is fine; no
  date or shop.
- `carry_on`: why it passes the carry-on filter, such as `Solid` or `50 g tube; put it
  in the liquids bag`.
- `shelf_life`: how long it keeps unopened, such as `about 9 months`, from the pack or
  the producer.
- `packing_tips`: what matters in a bag: fragile, crushes easily, melts above about 25
  °C, strong smell, powder that some airports screen separately.
- `made_from`, `how_made`, `taste`: ingredients, how it is made, and what it tastes
  like, in 1 or 2 sentences each.
- `where_to_buy`: the kind of shop, for example "any supermarket" or "the brand's own
  shop and the airport".
- `label_hints` (styles): local words to look for on the label or shelf.
- `local_terms`: useful local words from the name, with a pronunciation hint when
  useful.

Also collect `travel_rules`: 2 to 5 facts that matter for this trip, only from
official sources. Cover the 100 ml rule and 1 L bag, the destination's main bans on
food, and any duty-free or personal-use amount limits. You can mention that some
airports at the place have relaxed the liquids limit, but say the list still follows
the strict rule.

### Photos

Every item needs a photo; the output never shows a link instead of one. List image
URLs in `images`, best first, and give each item several candidates from different
sites, because some will not embed in chat apps.

1. The official product image from the producer or a local retailer. Search in the
   local language.
2. Open Food Facts (`world.openfoodfacts.org`), which has photos of supermarket
   packs. Use the `https://images.openfoodfacts.org/images/products/...` URL of a
   front photo at 400 px.
3. Wikimedia Commons. Use the direct `https://upload.wikimedia.org/...` thumbnail URL
   (about 480 px wide), not the `commons.wikimedia.org/wiki/File:` page.
4. A photo from one of the source posts.

For a `style`, use a photo of a typical example, such as the pack of one of its
`examples`. If an item still has no image, keep searching in the local language
(product name plus words like "pack", "bag", "box") before giving up.

Each URL must:

- start with `https://`;
- point directly at a JPEG, PNG, WebP or GIF file, not a web page, SVG or AVIF;
- be a thumbnail-sized file, under about 1.5 MB.

## Step 8: Write the JSON

If you can run scripts, write the list to any temporary file, for example
`/tmp/travel-food-souvenirs-<place-slug>.json`. Nothing needs to be kept after the
chat. If you cannot write files, keep the same structure in mind and use the manual
path in Step 9.

```json
{
  "place": {"query": "Helsinki, Finland", "name": "Helsinki", "slug": "helsinki",
            "destination": "Japan", "user_language": "en", "local_language": "fi",
            "currency": "EUR"},
  "labels": {},
  "travel_rules": ["Liquids, gels and pastes in hand luggage: 100 ml each, all in one 1 L clear bag."],
  "souvenirs": [
    {
      "id": "fazer-blue", "kind": "product", "category": "Sweets",
      "name": "Fazer Blue (Fazerin Sininen)", "local_name": "Fazerin Sininen",
      "type": "Milk chocolate", "producer": "Fazer", "origin": "Helsinki",
      "pack_size": "200 g bar", "price": "~3-4 EUR",
      "carry_on": "Solid",
      "customs": {"status": "allowed", "note": "...", "source": "https://..."},
      "shelf_life": "about 12 months", "packing_tips": "Melts in heat; keep it away from the outer pocket.",
      "made_from": "...", "how_made": "...", "taste": "...",
      "where_to_buy": "Any supermarket or kiosk",
      "tips": "What the source authors said.",
      "local_terms": [{"term": "suklaa", "meaning": "chocolate", "pronunciation": "SOOK-laa"}],
      "sources": ["https://..."],
      "images": ["https://...", "https://..."]
    }
  ],
  "left_out": [
    {"name": "Lingonberry jam (puolukkahillo)", "reason": "Sold in jars of about 400 g, over the 100 ml carry-on limit for gels.",
     "sources": ["https://..."]}
  ],
  "sources": [
    {"url": "https://...", "title": "...", "author": "...", "date": "2025-06-14",
     "language": "en", "kind": "traveller blog", "status": "used", "reason": "..."},
    {"url": "https://...", "title": "...", "status": "rejected", "reason": "SEO listicle"}
  ]
}
```

- `name`: the local name, with the user's-language name in brackets when it helps:
  `Salty liquorice (salmiakki)`.
- Style items add `label_hints` and, when known, `examples`.
- Leave out any field you could not confirm. Do not fill it with a guess.
- `labels`: when the user's language is not English, translate the output headings.
  Keys and English defaults: `travel_rules` Travel rules, `souvenirs` Souvenirs,
  `left_out` Left out, `sources` Sources, `rejected_sources` Rejected sources,
  `carry_on_ok` carry-on OK, `status_allowed` allowed, `status_declare` declare at
  customs, `status_banned` banned, `official` official, `size` Size, `carry_on`
  Carry-on, `customs` Customs, `shelf_life` Shelf life, `packing` Packing,
  `where_to_buy` Where to buy, `made_from` Made from, `how_made` How it's made,
  `taste` Taste, `look_for` Look for on the label, `examples` Examples, `tips` From
  the sources, `local_terms` Local terms, `item_sources` Sources.

## Step 9: Render

### With the script (preferred)

The script uses only the Python 3 standard library. The path is relative to this
skill's folder.

```bash
python3 scripts/render_souvenirs.py /tmp/travel-food-souvenirs-<slug>.json
```

It prints Markdown to stdout and warnings to stderr. It:

- tries each `images` URL in order the way a chat app would embed it (from another
  site, following redirects) and keeps the first that passes the rules above;
- rewrites that photo to a `https://camo.githubusercontent.com/...` URL through
  GitHub's Markdown API. Some chat apps, often on mobile and web, only show images
  from a short list of trusted hosts, and GitHub's image proxy is commonly on it;
  everywhere else the photo shows as usual. Set `GITHUB_TOKEN` or `GH_TOKEN` to raise
  GitHub's rate limit; without one it allows 60 requests an hour;
- leaves out items with no used source, no `carry_on`, or no valid `customs.status`,
  and moves items marked `banned` to Left out;
- groups the overview and cards by `category`, keeping your ranking within each group.

Read the warnings. Every "no working image" warning means an item would show without
a photo: add candidates from other sites in the Photos order and rerun until each
item has one. Every "left out" warning means an item was dropped: fix the field if you
can confirm it, or accept the drop. If the script says no image could be reached, the
environment where you run scripts probably has no internet access. Check the image
URLs with your browsing tool, remove the ones that do not show the item, and rerun
with `--no-check-images`.

### Without the script (manual path)

1. Drop items with no used source, no `carry_on`, or a customs status that is missing
   or `banned`; put the banned ones in Left out.
2. Open each image URL; keep the first that shows the right item and follows the
   rules in Photos. Use the final URL after any redirect. Then send
   `{"text": "![](<url>)", "mode": "gfm"}` as a POST to `https://api.github.com/markdown`
   and use the `camo.githubusercontent.com` URL from the `<img src="...">` it returns.
3. Write the Markdown in the layout of Step 10. Escape `(`, `)` and spaces in URLs as
   `%28`, `%29` and `%20` so links and images render.

## Step 10: Show the list in the chat

Post the rendered Markdown as your reply, in the user's language, with one short
sentence before it. Do not only point to a file. The layout is made for a phone
screen, with no tables:

1. **Travel rules**: bullets.
2. **Souvenirs**: a numbered overview grouped by category, one line per item with
   type, pack size, price, carry-on and customs status. Then one card per item, in
   the same order.
3. **Left out**: bullets with the reason for each.
4. **Sources**: used sources numbered, then rejected sources with reasons.

An overview group looks like this:

```markdown
**Sweets**

1. **Fazer Blue (Fazerin Sininen)**: Milk chocolate · 200 g bar ~3-4 EUR · carry-on OK · allowed
```

A card looks like this:

```markdown
### Fazer Blue (Fazerin Sininen)

![Fazerin Sininen](https://...)

*Milk chocolate · Fazer, Helsinki*

- **Size:** 200 g bar ~3-4 EUR
- **Carry-on:** Solid
- **Customs:** allowed. Chocolate and sweets are not restricted. [official](https://...)
- **Shelf life:** about 12 months
- **Packing:** Melts in heat; keep it away from the outer pocket.
- **Where to buy:** Any supermarket or kiosk
- **Made from:** ...
- **How it's made:** ...
- **Taste:** ...
- **From the sources:** ...
- **Local terms:** *suklaa* = chocolate (SOOK-laa)
- **Sources:** [1](https://...)
```

Style cards also have **Look for on the label** and, when known, **Examples**.
