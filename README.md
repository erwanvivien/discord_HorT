# discord-HorT
A Heads or Tails discord bot

## Usages
- [``$hart``](https://github.com/erwanvivien/discord-HorT#default-command)
- [``$harts``](https://github.com/erwanvivien/discord-HorT#Multiple-draws)
- [``$hartlim``](https://github.com/erwanvivien/discord-HorT#More-results-if-not-satisfied)
- [``$hartspec``](https://github.com/erwanvivien/discord-HorT#Specific-results-from-any-SubReddit)
- [``$hartadd`` or ``$hartremove`` or ``$hartlist``](https://github.com/erwanvivien/discord-HorT#Add-or-remove-from-list-of-SubReddits)

### Default command
``$hart`` or ``$hort`` for a simple heads or tails situation (they are the same)

HOW TO:
```
$hart [show] [novideo] [bad/good]
```

### Multiple draws
``$harts`` or ``$horts`` for many heads or tails situations (same again)

HOW TO:
```bash
$harts nb [show] [novideo] [bad/good]     # with (1 <= nb <= 10)
```

### Specific results from any SubReddit
``$hartspec`` or ``$hortspec`` for results in a specific SubReddit (equivalent to ``$hartlim``)

HOW TO:
```bash
$hartspec sub_name [nb] [show] [novideo] [bad/good]     # with (1 <= nb <= 10)
```

### Add or remove from list of SubReddits
``$hartadd`` or ``$hartremove`` or ``$hartlist`` for more results 

HOW TO:
```bash
$hartadd good/bad sub_name
```

## SubReddit Error
It is possible if a sub is private, quarantined or banned.
```json
{
    "reason": "quarantined", 
    "quarantine_message_html": "It is dedicated to shocking or highly offensive content", 
    "message": "Forbidden", 
    "quarantine_message": "It is dedicated to shocking or highly offensive content.", 
    "error": 403
}
```
