import discord
from discord.ext import commands, tasks
import datetime
import random
import re
from typing import List, Optional
from wordlist import words


EMOJI_CODES = {
    "green": {
        "a": "<:green_a:1250091193027526727>",
        "b": "<:green_b:1250091195380797471>",
        "c": "<:green_c:1250091196827828328>",
        "d": "<:green_d:1250091198832574497>",
        "e": "<:green_e:1250091200627867649>",
        "f": "<:green_f:1250091202150137856>",
        "g": "<:green_g:1250091203714744432>",
        "h": "<:green_h:1250091205027430553>",
        "i": "<:green_i:1250091207304937605>",
        "j": "<:green_j:1250091209054097500>",
        "k": "<:green_k:1250091211218485339>",
        "l": "<:green_l:1250091571362267209>",
        "m": "<:green_m:1250091216763097200>",
        "n": "<:green_n:1250091219711824038>",
        "o": "<:green_o:1250091222505226312>",
        "p": "<:green_p:1250091225210687549>",
        "q": "<:green_q:1250091573690105887>",
        "r": "<:green_r:1250091229517975552>",
        "s": "<:green_s:1250091575367831635>",
        "t": "<:green_t:1250091233854881852>",
        "u": "<:green_u:1250091235360903210>",
        "v": "<:green_v:1250091577116852326>",
        "w": "<:green_w:1250091239857061940>",
        "x": "<:green_x:1250091242465919068>",
        "y": "<:green_y:1250091245745995817>",
        "z": "<:green_z:1250091579239039048>",
    },
    "yellow": {
        "a": "<:yellow_a:1250091763423776788>",
        "b": "<:yellow_b:1250091764740657173>",
        "c": "<:yellow_c:1250091766443675699>",
        "d": "<:yellow_d:1250091768469262336>",
        "e": "<:yellow_e:1250091769983537224>",
        "f": "<:yellow_f:1250091771866906786>",
        "g": "<:yellow_g:1250091773745696768>",
        "h": "<:yellow_h:1250091775721209916>",
        "i": "<:yellow_i:1250091777545867384>",
        "j": "<:yellow_j:1250091779471183912>",
        "k": "<:yellow_k:1250091781614469201>",
        "l": "<:yellow_l:1250091953056645171>",
        "m": "<:yellow_m:1250091786219814942>",
        "n": "<:yellow_n:1250091954876715039>",
        "o": "<:yellow_o:1250091790397083730>",
        "p": "<:yellow_p:1250091792880238703>",
        "q": "<:yellow_q:1250091956965474394>",
        "r": "<:yellow_r:1250091797020020798>",
        "s": "<:yellow_s:1250091800228663296>",
        "t": "<:yellow_t:1250091802938048524>",
        "u": "<:yellow_u:1250091806121787424>",
        "v": "<:yellow_v:1250091959155163176>",
        "w": "<:yellow_w:1250091810076758048>",
        "x": "<:yellow_x:1250091812417310843>",
        "y": "<:yellow_y:1250091960904187987>",
        "z": "<:yellow_z:1250091817316388975>",
    },
    "gray": {
        "a": "<:gray_a:1250090577710678067>",
        "b": "<:gray_b:1250090579359043594>",
        "c": "<:gray_c:1250090581145944124>",
        "d": "<:gray_d:1250090582974664747>",
        "e": "<:gray_e:1250090584891461835>",
        "f": "<:gray_f:1250090586388566047>",
        "g": "<:gray_g:1250090588317941810>",
        "h": "<:gray_h:1250090589568110753>",
        "i": "<:gray_i:1250090591614927081>",
        "j": "<:gray_j:1250090594127319041>",
        "k": "<:gray_k:1250090595997974659>",
        "l": "<:gray_l:1250091050517925931>",
        "m": "<:gray_m:1250090600590606429>",
        "n": "<:gray_n:1250090602335309885>",
        "o": "<:gray_o:1250091052770267227>",
        "p": "<:gray_p:1250090606655442994>",
        "q": "<:gray_q:1250090609545314385>",
        "r": "<:gray_r:1250091054477213738>",
        "s": "<:gray_s:1250090616029708329>",
        "t": "<:gray_t:1250090617862754405>",
        "u": "<:gray_u:1250090619649654835>",
        "v": "<:gray_v:1250091056318382204>",
        "w": "<:gray_w:1250090624393412618>",
        "x": "<:gray_x:1250091058524852284>",
        "y": "<:gray_y:1250090628461760583>",
        "z": "<:gray_z:1250090630445535263>",
    },
}



def generate_colored_word(guess: str, answer: str) -> str:
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters: List[Optional[str]] = list(guess)
    answer_letters: List[Optional[str]] = list(answer)
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(ctx, puzzle_id: int) -> discord.Embed:
    user = ctx.author
    embed = discord.Embed(title="WORDLEEEEE!!!!!!!!")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /wodle!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: discord.Embed, guess: str) -> discord.Embed:
    puzzle_id = int(embed.footer.text.split()[1])
    answer = words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    return word in words


def random_puzzle_id() -> int:
    return random.randint(0, len(words) - 1)


def is_game_over(embed: discord.Embed) -> bool:
    return "\n\n" in embed.description


async def process_message_as_guess(bot, message: discord.Message) -> bool:
    ref = message.reference
    if not ref or not isinstance(ref.resolved, discord.Message):
        return False
    parent = ref.resolved

    if parent.author.id != bot.user.id:
        return False

    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "Start a new game with /play"
        if embed.author:
            reply = f"This game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    if is_game_over(embed):
        await message.reply("The game is already over. Start a new game with $play", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    guess = re.sub(r"<@!?\d+>", "", guess).strip()

    bot_name = message.guild.me.nick if message.guild and message.guild.me.nick else bot.user.name

    if len(guess) == 0:
        await message.reply(
            "I am unable to see what you are trying to guess.\n"
            "Please try mentioning me in your reply before the word you want to guess.\n\n"
            f"**For example:**\n{bot.user.mention} crate\n\n"
            f"To bypass this restriction, you can start a game with `@\u200b{bot_name} play` instead of `/play`",
            delete_after=14,
        )
        try:
            await message.delete(delay=14)
        except Exception:
            pass
        return True

    if len(guess.split()) > 1:
        await message.reply("Please respond with a single 5-letter word.", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    if not is_valid_word(guess):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    try:
        await message.delete()
    except Exception:
        pass

    return True



