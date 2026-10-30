# Lovable Prompts: Sideline Ready Blog

How to use this file:
1. Start a NEW Lovable project. Paste **Prompt 1** exactly as written. Let it finish.
2. Paste **Prompt 2** (admin, CSV import, link checker) in the same project.
3. Paste **Prompt 3** (SEO and launch audit).
4. Then follow the **Launch Checklist** at the bottom. When every box is checked, tell Claude "site is live" and Claude builds the 365-post CSV in the exact format below.

---

## PROMPT 1: Build the site

```
You are building "Sideline Ready", a content site for sports moms. Every post answers one thing a mom searched on Pinterest (a problem, a packing list, a buying decision, or a gift), tells a short story or walks through a how-to, and ends with a curated bundle of 5-7 Amazon products she can add to her cart in one click.

The site must be fast, mobile-first (most visitors arrive from Pinterest on a phone), and fully ready for Google to crawl and index. Use server-side rendering so every public page returns complete HTML on the first request.

== BRAND ==
Name: Sideline Ready
Tagline: Everything you need for game day, tournament weekends and the bleachers.
Colors: navy #14213D (primary, headers), turf green #1F7A4C (links, accents), orange #FF7F3F (buy buttons), yellow #FFC93C (highlights), off-white #FAF7F2 (background), text #1C1C1C.
Fonts: Oswald for headings, Inter for body text (load from Google Fonts, display=swap).
Feel: clean, warm, easy to scan with one thumb. Big tap targets. No pop-ups, no autoplay.
Do NOT show children's faces or names anywhere. Use simple illustrations, icons or product-free sideline scenes for placeholders.

== SITE CONFIG (one settings record, editable later in admin) ==
- SITE_URL: https://YOUR-DOMAIN.com   (placeholder; used for canonical URLs, sitemap, RSS, Open Graph)
- AMAZON_TAG: YOURTAG-20   (placeholder Amazon Associates tracking ID)
- TIMEZONE: America/Chicago
- Disclosure text: "As an Amazon Associate I earn from qualifying purchases. Some links on this page are affiliate links, which means I may earn a small commission at no extra cost to you."
- Google Search Console verification meta tag: empty placeholder
- Pinterest domain verification meta tag: empty placeholder
- Google Analytics 4 measurement ID: empty placeholder (only load the script if set)

== DATA MODEL (use Lovable Cloud database) ==
categories: id, slug (unique), name, description, sort_order
posts: id, day_number (int, unique), publish_date (date, unique), slug (unique), category_id, seo_title, meta_description, h1, primary_keyword, secondary_keywords (text[]), journey_stage (Problem | Planning | Comparing | Ready to buy), post_type (How-to | Survival guide | What to wear | Checklist | Ideas list | Setup guide | Buying guide | Gift guide), hook, body_markdown, cta_text, cart_url_override (nullable), featured_image_url (nullable), featured_image_alt, pin_title, pin_description, faq (jsonb array of {q, a}), created_at, updated_at
post_items: id, post_id, position (1-7; position 1 = the anchor product), asin, name, blurb, url_override (nullable)
redirects: from_path (unique), to_path, created_at
link_clicks: id, post_id, position (0 = add-all-to-cart button), clicked_at   (no personal data)

Seed these 13 categories (slug | name):
sports-mom-bag-essentials | Sports Mom Must Haves & Bag Essentials
stadium-seats | Stadium Seats & Bleacher Comfort
cold-game-essentials | Cold Football Game Essentials
sports-wagons | Sports Wagon Ideas & Accessories
travel-ball-tournaments | Travel Ball & Tournament Must Haves
sports-mom-gifts | Sports Mom Gifts & Gift Baskets
coach-team-mom | Coach Gifts & Team Mom Ideas
sports-dad | Sports Dad Essentials & Gifts
hot-weather-sideline | Hot Weather Sideline Essentials
game-day-bags | Game Day Bags & Stadium Bags
backyard-training | Backyard Sports Training Equipment
gear-storage | Sports Equipment Storage & Garage Organization
athlete-meals-snacks | Teen Athlete Meals, Snacks & Meal Prep

== AMAZON LINKS (build them, don't hard-code them) ==
- Product link for an item = url_override if set, otherwise https://www.amazon.com/dp/{asin}?tag={AMAZON_TAG}
- "Add all to cart" link for a post = cart_url_override if set, otherwise
  https://www.amazon.com/gp/aws/cart/add.html?AssociateTag={AMAZON_TAG}&ASIN.1={asin1}&Quantity.1=1&ASIN.2={asin2}&Quantity.2=1 ... for every item in position order.
- Changing AMAZON_TAG in settings must update every link on the site instantly.
- All Amazon links: open in a new tab, rel="sponsored nofollow noopener". Link straight to amazon.com (no redirect or cloaked /go/ links).
- Any URL containing the text PLACEHOLDER is treated as unfinished (see Link Checker in Prompt 2) and renders as a disabled grey button that says "Link coming soon" on the public site.
- NEVER display prices, star ratings or review counts anywhere on the site, and never use Amazon product photos. Product cards show the name, the blurb and the button only.
- Record a row in link_clicks when any Amazon button is clicked (fire-and-forget, must not slow the click).

== POST DATING AND SCHEDULED PUBLISHING (important) ==
- Every post has a publish_date. Day 1 = November 1, 2026. Day 365 = October 31, 2027. One post per day.
- A post is PUBLIC only when publish_date <= today's date in America/Chicago (it goes live at 12:00 AM Central on its date). Compute this at request time on the server, so no manual publishing or rebuild is ever needed.
- Future-dated posts must be invisible to the public: their URL returns a real 404 status, and they are excluded from the home page, category pages, search, related posts, sitemap.xml and the RSS feed.
- Logged-in admins can still open future posts (show a yellow "Scheduled for {date}" banner) so they can be reviewed.
- Show dates on posts as "Published November 1, 2026". If updated_at is on a later day than publish_date, also show "Updated {Month D, YYYY}".
- Lists are ordered newest publish_date first.
- Use these dates in structured data: datePublished = publish_date at 00:00 America/Chicago with the correct UTC offset (handle daylight saving), dateModified = updated_at.
- Posts with past dates are fine (if the site launches after Nov 1, 2026, those posts are simply already live).

== PAGES AND URLS ==
/                          Home: hero with tagline, "Today's pick" (the newest public post), latest 12 posts grid, category tiles, short About blurb.
/blog                      All public posts, paginated 24 per page (/blog/page/2 ...).
/blog/{slug}               Post page.
/category/{category-slug}  Category page with intro description and its posts, paginated.
/search?q=                 Simple search over title, h1, primary keyword (noindex).
/about                     About Sideline Ready (written for sports moms; no names or photos of children).
/disclosure                Full affiliate disclosure.
/privacy                   Privacy policy (mentions affiliate cookies and analytics if enabled).
/contact                   Simple contact form (stores messages in the database).
/rss.xml                   RSS feed of the 50 newest public posts (title, link, description = meta_description, pubDate, image enclosure). Pinterest can auto-pin from this feed.
/sitemap.xml               All public posts, categories and static pages with lastmod.
/robots.txt                Allow all, disallow /admin and /search, link to sitemap.
Custom 404 page with search box and latest posts.
No trailing slashes; lowercase URLs only. If a post slug changes, automatically save a 301 redirect from the old path.

== POST PAGE LAYOUT (in this order) ==
1. Breadcrumbs: Home > {Category} > {short title}
2. H1 (posts.h1)
3. Date line + category chip + estimated read time
4. Disclosure box (small, above the first link, always visible)
5. Featured image (2:3 vertical pin image, width 100% on mobile, max 600px on desktop, real alt text from featured_image_alt, lazy-load everything below it). If no image yet, show a branded placeholder card with the h1 text.
6. Hook paragraph (posts.hook) in slightly larger text
7. "Jump to the bundle" button (anchor link)
8. Body (render body_markdown: H2/H3, lists, bold, links, tables). Auto-build a table of contents from the H2s when there are 3 or more.
9. THE BUNDLE section (id="bundle"): heading "The {N}-Item Bundle", then one card per post_item in order: number, product name, blurb (1-2 sentences), orange "View on Amazon" button. Position 1 gets a small "Start here" label.
10. Big orange "Add all {N} to my Amazon cart" button using the cart link, with cta_text above it and a small line under it: "Opens Amazon with every item in your cart. You can remove anything before checkout."
11. FAQ section (if faq has items) as an accordion.
12. "Save this for later" Pinterest Save button (use the pin image + pin_description).
13. Related posts: 3 from the same category, then fill by shared keywords. Public posts only.
14. Footer: disclosure link, categories, about, privacy, contact, RSS.

== SEO REQUIREMENTS (every public page) ==
- Server-rendered HTML with <title> = seo_title (posts) and <meta name="description"> = meta_description. Unique on every page; category and page-2+ titles include the category name or "Page N".
- <link rel="canonical"> using SITE_URL. Paginated pages canonical to themselves.
- Open Graph (og:type=article, og:title, og:description, og:image, og:url, article:published_time, article:modified_time, og:site_name) and Twitter card tags. These also make Pinterest Rich Pins work.
- JSON-LD on posts: BlogPosting (headline, description, image, datePublished, dateModified, author {@type Person, name "Sideline Ready"}, publisher Organization with logo, mainEntityOfPage), BreadcrumbList, and an ItemList of the bundle items (name + url only, no prices or ratings). FAQPage only when FAQ exists.
- JSON-LD on home: WebSite (with SearchAction pointing to /search?q=) and Organization.
- One H1 per page, logical H2/H3 order, descriptive link text, every image has alt text and width/height set.
- Admin, search and preview pages: <meta name="robots" content="noindex, nofollow">.
- Core Web Vitals: no layout shift, fonts with swap, images in modern formats with srcset, no heavy libraries on public pages. Target Lighthouse 90+ on mobile for Performance, SEO, Accessibility and Best Practices.
- Add the verification meta tags from settings when they are filled in.

== SAMPLE CONTENT (so I can test the design; I will replace it later) ==
Create 2 sample posts marked "SAMPLE - delete before import" in the admin.

Sample A (publish_date 2026-11-01, day_number 1, category backyard-training)
slug: backyard-basketball-court-ideas-spalding-portable-hoop
seo_title: Backyard Basketball Court Ideas: 5-Piece Home Practice Setup
meta_description: Backyard basketball court ideas: how to set up practice at home, starting with the Spalding portable hoop. See the full 5-piece setup.
h1: Backyard Basketball Court Ideas: A Home Practice Setup Built Around the Spalding Portable Hoop
primary_keyword: backyard basketball court ideas
journey_stage: Comparing, post_type: Setup guide
hook: Practice is twice a week, but the reps happen at home. Here's the setup, starting with the Spalding portable hoop.
items: 1 B0BYFBT9LK Spalding Momentous Portable Basketball Hoop | 2 B00099YJJK Tachikara Portable Ball Cart | 3 B003D6FGB6 SKLZ D-Man Defensive Mannequin | 4 B01GPBXP86 GHB Pro Agility Ladder | 5 B0009KF59M Wilson NCAA Final Four Basketball
Write an 800-1,000 word body in a warm, practical sports-mom voice: why home reps matter, choosing a spot in the driveway or backyard, setting the hoop height by age, a simple 20-minute practice routine, safety notes, then lead into the bundle. Add 3 FAQs.

Sample B (publish_date 2026-11-02, day_number 2, category sports-mom-bag-essentials) - a checklist post:
slug: travel-baseball-snacks-beef-jerky-multipack
h1: Travel Baseball Snacks: Easy Ideas, Plus the 6 Supplies That Make It Simple
hook: Practice ends at 7, there's a game at 8 a.m., and everyone is starving. Here's the plan, starting with the beef jerky multipack.
items: 1 B07NR7694X Jack Link's Beef Jerky Multipack | 2 B083X6TSHQ Kar's Sweet 'N Salty Trail Mix Packs | 3 B0CJ92X9VX Stainless Steel Snack Containers | 4 B01MRZZ3KC Quaker Chewy Granola Bars | 5 B08VDBW5PW SPARTER Backpack Cooler | 6 B0GVLCQ2DK Gatorade Zero Powder Variety Pack
Write a 700-900 word body (snack timing between games, a packing list, keeping things cold, what to avoid in the heat), then the bundle. Add 3 FAQs. Write your own SEO title (max 60 characters) and meta description (max 155 characters).

Content rules for anything you write: helpful and specific, no invented personal experiences, statistics, testimonials, or "#1 / best-selling" claims; no prices; no medical claims.
```

---

## PROMPT 2: Admin, editing, CSV import, link checker

```
Add a private admin area for the Sideline Ready site.

== ACCESS ==
- /admin requires login (email + password via Lovable Cloud auth). Only users with role "admin" can access. Make my account the first admin. No public sign-up page.
- All admin pages are noindex and excluded from the sitemap.

== DASHBOARD (/admin) ==
- Counts: total posts, published (date reached), scheduled (future), posts with unfinished links, posts missing a featured image.
- "Today" card: the post going live today and the next 7 days.
- Calendar view by month (Nov 2026 - Oct 2027) showing each day's post title, colored by status: green published, blue scheduled, red has problems (missing required field, unfinished link, missing image). Click a day to edit.
- Clicks report from link_clicks: top 20 posts by Amazon clicks (last 7 / 30 / all days) and clicks on "Add all to cart" vs single items.

== POST EDITOR (/admin/posts/{id}) ==
- Edit every field of the post: dates, slug, category, SEO title (live character counter, warn over 60), meta description (counter, warn over 155), h1, keywords, journey stage, post type, hook, body (Markdown editor with live preview), CTA text, cart URL override, featured image (upload to storage or paste URL) + alt text, pin title, pin description, FAQ items (add/remove/reorder).
- Bundle editor: list of items (drag to reorder, 1-7 items), each with ASIN, name, blurb, URL override. Show the auto-built Amazon link next to each item and a "Test link" button that opens it.
- Google preview (title + URL + description as it would appear in search) and Pinterest preview.
- Save, plus "Preview as public page" (works for scheduled posts).
- Changing the slug creates a 301 redirect automatically.
- Posts list (/admin/posts): table with search, filters (status, category, month, problems only), sortable by date; bulk delete for the SAMPLE posts.

== SETTINGS (/admin/settings) ==
Edit SITE_URL, AMAZON_TAG, disclosure text, verification tags, GA4 ID, About page text.

== LINK CHECKER (/admin/links) ==
- Lists every post item and cart link that is unfinished: URL contains PLACEHOLDER, ASIN is not 10 characters (letters/numbers), or AMAZON_TAG is still YOURTAG-20.
- For each row: post title, publish date, item, current link, "Edit" and "Test" buttons.
- "Mark tested" checkbox per post (stores tested_at) so I can track which links I've opened and confirmed.

== CSV IMPORT / EXPORT (/admin/import) ==
I will upload one CSV with up to 365 rows (one row per post). Build an importer that matches this format EXACTLY:

Encoding UTF-8, comma-separated, first row is the header, fields that contain commas, quotes or line breaks are wrapped in double quotes, quotes inside fields are doubled (""). Line breaks inside body_markdown are real line breaks inside a quoted field.

Header (exact order, exact spelling):
day_number,publish_date,slug,category_slug,seo_title,meta_description,h1,primary_keyword,secondary_keywords,journey_stage,post_type,hook,body_markdown,cta_text,cart_url_override,featured_image_url,featured_image_alt,pin_title,pin_description,faq_1_q,faq_1_a,faq_2_q,faq_2_a,faq_3_q,faq_3_a,item_1_asin,item_1_name,item_1_blurb,item_1_url,item_2_asin,item_2_name,item_2_blurb,item_2_url,item_3_asin,item_3_name,item_3_blurb,item_3_url,item_4_asin,item_4_name,item_4_blurb,item_4_url,item_5_asin,item_5_name,item_5_blurb,item_5_url,item_6_asin,item_6_name,item_6_blurb,item_6_url,item_7_asin,item_7_name,item_7_blurb,item_7_url

Rules:
- day_number 1-365, unique. publish_date YYYY-MM-DD, unique, and must equal 2026-11-01 + (day_number - 1) days.
- slug: lowercase letters, numbers and hyphens only, max 80 characters, unique.
- category_slug must match an existing category.
- seo_title max 70 characters (warn above 60). meta_description max 160 (warn above 155). h1, hook, body_markdown required.
- secondary_keywords separated by | (pipe).
- journey_stage and post_type must be one of the allowed values.
- cart_url_override, featured_image_url and item_N_url may be empty (empty = use the auto-built link / placeholder image).
- Items 1-5 required (asin + name + blurb). Items 6-7 optional, but if an asin is given, name and blurb are required. ASIN = exactly 10 letters/numbers.
- FAQ pairs optional; a question needs an answer.
- Any URL must start with https:// or contain PLACEHOLDER.

Import flow:
1. Upload CSV -> DRY RUN: parse and validate every row WITHOUT saving. Show a summary (rows OK, rows with errors, rows with warnings) and a table of every problem: row number, day_number, column, what's wrong.
2. If there are errors, nothing can be imported. Let me download the error list as CSV.
3. If there are no errors, show "Import 365 posts" button. The import runs in ONE database transaction (all rows or nothing). Match existing posts by day_number: update them (keep their id and any manual edits to featured image if the CSV image is empty), otherwise insert. Replace each post's items with the CSV items.
4. After import, show a result report and link to the calendar.
- Export button: download all posts in this exact same CSV format (so a round-trip export -> import changes nothing).
- Provide a "Download blank template" button with just the header row.
```

---

## PROMPT 3: SEO and launch audit

```
Audit the Sideline Ready site for launch and fix anything that fails. Report a checklist with pass/fail for each item:

1. View the raw HTML response (not the rendered DOM) for the home page, a category page, a published post and a scheduled post. Published pages must contain the full title, meta description, canonical, Open Graph tags, JSON-LD and the article text in the HTML. The scheduled post must return HTTP 404 to a logged-out visitor.
2. sitemap.xml lists only public posts (none with a future publish_date), all categories and static pages, uses SITE_URL, and is valid XML. robots.txt links to it and blocks /admin and /search.
3. Every public page has a unique title and meta description; exactly one H1; canonical URL is absolute and has no trailing slash.
4. JSON-LD validates (BlogPosting, BreadcrumbList, ItemList, Organization, WebSite, FAQPage where used): no prices, no ratings.
5. Every Amazon link has rel="sponsored nofollow noopener" and target="_blank"; the disclosure appears above the first affiliate link on every post; no prices or Amazon images appear anywhere.
6. Scheduled publishing: temporarily set a sample post's date to tomorrow and confirm it disappears from the home page, category page, sitemap, RSS and returns 404; set it back and confirm it reappears. Confirm dates use America/Chicago.
7. RSS feed is valid and only contains public posts.
8. 301 redirect works after changing a slug.
9. Mobile Lighthouse scores for home and a post page (Performance, Accessibility, Best Practices, SEO); fix anything under 90.
10. 404 page returns status 404.
11. Admin is noindex and not reachable when logged out.
12. Export CSV, re-import it as a dry run: zero errors and zero changes.
```

---

## LAUNCH CHECKLIST (you do these, then tell Claude "site is live")

- [ ] Connect your custom domain in Lovable and set SITE_URL in Admin > Settings to it.
- [ ] Set AMAZON_TAG to your Sideline Ready tracking ID (or keep screenfreet0f-20).
- [ ] Add the domain to Amazon Associates: Account Settings > Website and mobile app list.
- [ ] Google Search Console: add the domain, paste the verification tag in Settings, submit /sitemap.xml.
- [ ] Pinterest: claim the website (paste the Pinterest tag in Settings), then validate Rich Pins with one post URL.
- [ ] Open both sample posts on your phone; click every Amazon button and the "Add all to cart" button; confirm Amazon opens with your tag in the URL.
- [ ] Run Prompt 3's audit and confirm every line passes.
- [ ] Delete the 2 SAMPLE posts (or leave them; the CSV import overwrites day 1 and day 2).

Then message Claude: "Site is live, links tested." Claude will build the 365-row CSV in exactly the format above (Day 1 = Nov 1, 2026 through Day 365 = Oct 31, 2027), run it through the same validation rules before sending, and you upload it at /admin/import.

Notes for the CSV phase (Claude's to-do, nothing for you to do now):
- The current 365-day plan starts Dec 1, 2026. It will be re-dated to start Nov 1, 2026 and the seasonal order rebuilt for that start (gifts in Nov-Dec, cold gear Oct-Feb, summer gear Mar-Aug).
- The bundle call-to-action text in the plan includes an "about $X" cart total. Prices will be removed from the CSV, because Amazon doesn't allow showing prices that aren't pulled live from Amazon.
- Pins should be scheduled for 8 AM Central or later, so each pin goes out after its post is live (posts go live at 12:00 AM Central).
