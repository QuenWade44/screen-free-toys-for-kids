# Pinterest Monthly System (3 accounts)

Accounts: School Templates by Dr. Q (TPT links) · Dr. Q | Screen-Free Kid Toys (Amazon, tag screenfreet0f-20) · Sideline Ready (Amazon)

## The rule that drives everything
Pinterest holds at most 100 scheduled pins per account. Uploads beyond that fail ("More than 100 scheduled Pins").
So each account gets 5 pins/day split into 2 files per month, each file 80 rows or fewer.

## Monthly calendar (same for all 3 accounts)
| When | What you do |
|---|---|
| Around the 25th | Prompt Claude: "Build next month's pins." You get 3 zips (one per account). |
| 28th | Upload PART A (days 1-15 of next month, 75 pins) to each account |
| 14th | Upload PART B (days 16-end, 75-80 pins) to each account |

Why those dates: on the 28th at most 20 pins are still waiting (+75 = 95). On the 14th at most 10 are waiting (+80 = 90). Both stay under 100.

## Locked CSV format
Header, exact order: Title,Media URL,Pinterest board,Thumbnail,Description,Link,Publish date,Keywords
- Title: 100 characters max, unique within the account
- Media URL: direct public https link ending in .png/.jpg/.mp4 (GitHub raw links)
- Pinterest board: exact board name that already exists in that account
- Thumbnail: empty for images
- Description: 500 characters max, includes "Contains affiliate links." and Amazon's required line for Amazon accounts
- Link: full https link (Amazon links include ?tag=)
- Publish date: UTC, format 2026-12-01T14:00:00 (8am, 11am, 3pm, 6pm, 9pm Central = 14:00, 17:00, 21:00, 00:00+1, 03:00+1 UTC)
- Keywords: comma-separated search phrases
- UTF-8, no BOM, 80 rows max per file
Every file is checked with validate_csv.py (including that every image link loads) before delivery.

## Zip layout each month
YYYY-MM_<Account>.zip
  PART-A_upload-28th_<dates>.csv
  PART-B_upload-14th_<dates>.csv
  alt-text-and-schedule.csv
  links.csv
