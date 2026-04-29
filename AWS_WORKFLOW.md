# AWS instance — Discord-bot workflow

The course gives every student a personal AWS VM, gated behind a Discord bot.
You manage start/stop/info via DM commands; you connect via SSH.

## One-time setup

1. Join Discord: https://discord.gg/u4yZN22E
2. DM `CESE5040Bot` (find it in the member list) with `$hello`.
3. If it replies "not assigned", contact **llandsmeer** on Discord.
4. After the "assigned" confirmation, run `$info` to get your instance IP.

## Daily commands (DM the bot)

| Command | Effect |
|---|---|
| `$hello` | Print the command list, confirm assignment. |
| `$info`  | Show instance IP, state (`stopped`/`running`), budget, used time, time-left-this-week. |
| `$start` | Boot the instance. Takes 1–3 minutes. Run `$info` again afterwards to get the (new?) IP. |
| `$stop`  | Shut it down. **Do this every time** you finish working. |

## Budget rules — the only thing that can wreck your weekend

- **16 hours per week**, resets **every Monday**.
- If you blow through it, you're locked out until the next Monday.
- **Stop the instance whenever you're not actively running things.** Editing
  code locally costs 0 hours; leaving an idle SSH session burns hours.

## Connecting

```
ssh ubuntu@<public-ip>
# password: see secrets.txt (gitignored)
```

The cursor doesn't move while typing the password — that's normal.

Recommended Windows client: **MobaXterm** (Home Edition). It bundles SFTP, so
you can drag-drop files between your laptop and the VM without scp.

## Environment

Pre-installed: Python 3.12, the lab packages.

```bash
python3 --version
pip3 list
```

Recommended check on first login:

```bash
python3 -c "import numpy, numba, matplotlib, scipy; print('ok')"
```

## Data persistence — assume worst case

Course wording: "we make every effort to preserve data after the instance
stops, you should back up important files... Data recovery cannot be
guaranteed."

Translation:
- Push your code to a private git repo, or sync via SFTP, every session.
- Don't keep the only copy of an experiment log on the VM.
- Cache files (e.g. `~/.cache/tvb_algo/` containing the connectome `.npz`s)
  are cheap to regenerate — `lib/data.py` re-downloads them on demand.

## Workflow that respects the 16-hour budget

1. Develop and small-N test on your laptop (TVB76 runs in seconds in pure
   Python).
2. `$start` only when you're ready to run a measurement on TVB192/TVB998 or
   to time JIT versions.
3. Push code via SFTP, run, copy results back, `$stop`.
4. Write the report locally.
