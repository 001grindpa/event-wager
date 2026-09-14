# Event Wager

This contract lets two parties lock equal GEN on a dated yes/no event question. A creator opens the wager with a question, the event date, and the resolution date. The joiner takes the opposite side with the same stake. After the resolution date, anyone can call resolve. Validators fetch two allowlisted official pages and compare them. If both pages support the same answer, the pot pays to that side. If the answers disagree, are incomplete, or miss the date, both sides are refunded.

## Live links

- Studio: https://studio.genlayer.com/?import-contract=0xEEe6b7655C7d0779a1e52812b7a426F8Dba9C3bf
- Explorer: https://explorer-studio.genlayer.com/address/0xEEe6b7655C7d0779a1e52812b7a426F8Dba9C3bf
- Contract address: 0xEEe6b7655C7d0779a1e52812b7a426F8Dba9C3bf
- Chain: GenLayer StudioNet (chain 61999)

## How it works

### Lifecycle

1. OPEN
   - The creator calls `create_wager` with the question, `event_date`, `resolve_after`, the chosen side, and two source URLs.
   - The creator locks the initial GEN stake.

2. MATCHED
   - The joiner calls `join` with the opposite side and the same stake.
   - The wager status becomes `MATCHED`.
   - The contract holds the combined pot.

3. SETTLED or REFUNDED
   - Once `resolve_after` has passed, anyone can call `resolve`.
   - Validators fetch two allowlisted public pages for the same claim and event date.
   - If both sources clearly support `YES`, the pot is paid to the YES side.
   - If both sources clearly support `NO`, the pot is paid to the NO side.
   - If the sources disagree, are off-topic, are undated, or are inconclusive, resolution returns `UNKNOWN` or `DISAGREE` and both stakes are refunded.

## Resolution time guard

The contract enforces a time check before close. `resolve` must not run before `resolve_after`. This prevents early settlement when the event date has not yet been reached and keeps the wager in a stable `MATCHED` state until the allowed resolution window begins.

This is the key guard in the direct test. The test creates a wager with `event_date=2026-12-31` and `resolve_after=2026-12-31`, joins it, and then calls `resolve` before the later date. The call reverts with the message `wager cannot be closed before resolve_after`, and the status remains `MATCHED`.

## Contract methods

| Method | Purpose | Notes |
| --- | --- | --- |
| `create_wager` | Create a wager with a question, date, resolution date, side, and two source URLs | Creator locks a stake |
| `join` | Take the opposite side with the same stake | Requires a matching value |
| `resolve` | Close the wager after `resolve_after` | Reverts before the allowed time |
| `get_wager` | Return the wager state | Shows status and related fields |
| `can_resolve` | Check whether the wager is allowed to resolve | Returns `false` before `resolve_after` |

## Allowlisted source hosts

Source URLs must be `https` and must come from official, allowlisted hosts. The repo accepts these host families:

- `bbc.com` and `www.bbc.com`
- `reuters.com` and `www.reuters.com`
- `apnews.com` and `www.apnews.com`
- `theguardian.com` and `www.theguardian.com`
- `nytimes.com` and `www.nytimes.com`
- `espn.com` and `www.espn.com`
- `skysports.com` and `www.skysports.com`
- `en.wikipedia.org` and `wikipedia.org`
- `sec.gov` and `www.sec.gov`
- `nasa.gov` and `www.nasa.gov`
- `who.int` and `www.who.int`
- `un.org` and `www.un.org`
- `europa.eu` and `www.europa.eu`

Additional allowlisted suffixes include:

- `.gov`
- `.gov.uk`
- `.gouv.fr`
- `.gob.mx`
- `.gc.ca`
- `.europa.eu`
- `.int`

## Deploy in Studio

1. Open the Studio import link above.
2. Select the contract from `contracts/EventWager.py`.
3. Use the no-argument constructor.
4. Deploy on GenLayer StudioNet (chain 61999).
5. Copy the deployed address from the Studio output and use it with the explorer link.

This repo’s direct deployment flow is a no-arg constructor deployment.

## Run the early-resolve test

From the repo root, run:

```bash
pip install genlayer-test && pytest tests/direct/test_early_resolve.py -v
```

This is the exact direct-mode validation in the repo. It checks that a wager cannot resolve before `resolve_after` and that the status stays `MATCHED`.

## Exact Studio replay for stewards

Use the following exact sequence in Studio:

1. Create a wager with:
   - `event_date = 2026-12-31`
   - `resolve_after = 2026-12-31`
   - a question such as `Did team X win on 2026-12-31?`
   - a stake of equal GEN on each side
   - two allowlisted source URLs

2. Join the wager with the opposite side and the same stake.

3. Call `resolve` immediately.

4. Expect a revert with: `wager cannot be closed before resolve_after`.

5. Check the updated wager state.

Expected result:

- status remains `MATCHED`
- `REFUNDED` is not set
- `SETTLED` is not set
- `can_resolve` is `false`

## Repo layout

```text
.
├── LICENSE
├── README.md
├── contracts/
│   └── EventWager.py
└── tests/
    └── direct/
        └── test_early_resolve.py
```

## Notes

- This repo is small and focused.
- The direct test is the authoritative check for the early-resolve guard.
- No contract or test files were changed while writing this README.
