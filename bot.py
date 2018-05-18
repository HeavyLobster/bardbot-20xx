# Standard imports
import configparser
import random
# PyPI imports
from discord.ext import commands
import discord
# My imports
import libchampmastery
import numtrans

# Function which returns a list of prefixes for the bot's commands
def _get_prefix(bot, message):
    prefixes = ["!"]

    return prefixes

class BardBot(commands.Bot):
    def __init__(self):
        # Pass prefix function to inherited class init function
        super().__init__(command_prefix=_get_prefix)

        # Read configuration
        self.config = configparser.ConfigParser()
        self.config.read("bot.ini")

        # Set up Riot API
        self.api = libchampmastery.ApiInterface(
            self.config["auth"]["riotkey"]
        )

        # Set up commands
        self.add_command(self.masteryrole)
        self.add_command(self.rmmasteryrole)

    def run(self):
        super().run(self.config["auth"]["discordkey"])

    async def on_member_join(self, member):
        # Get greeting channel from configs
        channel = member.guild.get_channel(
            int(self.config[str(member.guild.id)]["greetchannel"])
        )
        if random.randrange(6) != 0:
            await channel.send(
                f"Welcome, {member.mention}, to the "
                f"{member.guild.name}! "
                "Head to <#265551115901206528> to get Roles! "
                "<:bardlove:242942446072233984>"
            )
        else:
            await channel.send(
                f"Welcome {member.mention}!"
                "<:bardhi2:269858268048916480> Have some "
                "<:cacao:269857893086527488> and "
                "<:porosnax:278951733609234433> "
                "<:bardhug:269858053820645389> \nHead to "
                "<#265551115901206528> to get Roles! "
                "<:bardlove:242942446072233984>"
            )

        return

    def get_valid_roles(self, ctx, region, username):
        validRoles = []

        try:
            userData = self.api.user(region, username, 432)
        except KeyError:
            return validRoles

        points = userData["mastery"]

        for role in ctx.guild.roles:
            if role.name[0] in "123456789":
                if (numtrans.from_shorthand(role.name.split()[0].lower())
                        < points):
                    validRoles.append(role)

        return validRoles

    @commands.command()
    async def masteryrole(self, ctx):
        if len(ctx.message.content.split()) < 4:
            await ctx.message.channel.send(
                "I got your command and I'm choosing to ignore it "
                "because you're missing something"
            )

            return

        desiredRole = ctx.message.content.split()[1]
        userRegion = ctx.message.content.split()[2]
        username = "".join(ctx.message.content.split()[3:])

        validRoles = self.get_valid_roles(ctx, userRegion, username)

        for role in validRoles:
            if desiredRole.lower() == role.name.lower():
                await ctx.message.author.add_roles(role)
                await ctx.message.channel.send(
                    f"Gave you the role {role.name}!"
                )
                return

        await ctx.message.channel.send(
            "I couldn't give you that role for some reason"
        )

        return

    @commands.command()
    async def rmmasteryrole(self, ctx):
        if len(ctx.message.content.split()) < 2:
            await ctx.message.channel.send(
                "I got your command and I'm choosing to ignore it "
                "because you're missing something"
            )

            return

        unwantedRole = ctx.message.content.split()[1].lower()
        masteryRoles = []

        for shorthand in numtrans.mastery_range(10000000):
            for role in ctx.guild.roles:
                if (numtrans.to_shorthand(shorthand).lower()
                        == role.name.split()[0].lower()):
                    masteryRoles.append(role)

        for role in masteryRoles:
            if unwantedRole == role.name.split()[0].lower():
                await ctx.message.author.remove_roles(role)
                await ctx.message.channel.send(
                    f"Removed the {role.name} role from you"
                )
                return

        await ctx.message.channel.send(
            "Something didn't go right and I have no idea what"
        )

        return

if __name__ == "__main__":
    bardBot = BardBot()
    bardBot.run()
