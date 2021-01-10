import discord

# constants
PASTEL_GREEN = 0x77dd77
PASTEL_PURPLE = 0x7777dd
PASTEL_PINK = 0xdd77dd
PASTEL_YELLOW = 0xdddd77


def create_assignment_embed(assignments, title, color) -> discord.Embed:
    """
    Create a discord embed from a given assignment or list of assignments.

    @param assignments: list of dicts or single dict
    @param title: string
    @param color: hex code of desired embed color
    @return: discord.Embed
    """
    if type(assignments) is dict:
        assignments = [assignments]  # account for single assignment param

    em = discord.Embed(
        title=title,
        color=color
    )

    for i in assignments:
        assignment_description = \
            f'''
                `📌 Desc:` {i['assignment_body']}
                `📆 Due:` {i['due_month']}/{i['due_day']}
                `🔑 ID:` {i['id']}
            '''

        em.add_field(
            name=i['assignment_name'],
            value=assignment_description,
            inline=False
        )

    return em
