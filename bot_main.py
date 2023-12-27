import gspread_signup, gspread_registration, canvas_notifications
import gspread
import discord
from discord.ext import commands
import traceback
import colorama
import config
import tracemalloc
import asyncio

# importing discord.py libraries to work with discord's API
# importing colorama to change console's text color to make debugging more comfortable


# colorama uses ANSI escape codes. Below I used some color codes...
colorama.init()
cyan = "\x1b[36m"
red = "\x1b[31m"
green = "\x1b[32m"
yellow = "\x1b[33m"

# creating class instance with command prefix "!" (to use bot in discord type in !command_to_use"
# discord.Intents.All makes bof free to use all server's features
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

rules_channel = bot.get_channel(config.RULES_ID)
tracemalloc.start()


# decorator (bot event) which outputs bot's successful start to the console
# async function allows bot to operate multiple users at once, otherwise users' requests would go one by one

@bot.event
async def on_ready():
    print(cyan + f"Bot {bot.user.name} is ready for use!")
    debugging_channel = bot.get_channel(config.DEBUGGING_CHANNEL_ID)

    trips, dates, times, atendees, wl, wks_ids = gspread_signup.get_signups()

    for i in range(len(trips)):
        bot.add_view(SignUpButtons(trips[i], dates[i], times[i], atendees[i], wl[i]))
    bot.add_view(RegisterButton())
    bot.add_view(CanvasNotificationButtons())
    await debugging_channel.send("Bot is started and online!")


# decorator which outputs any messages written in any text channel on the server to the console
@bot.event
async def on_message(message):
    print(yellow + f'{message.author} ' + cyan + "said: " + yellow + f"'{message.content}'")
    await bot.process_commands(message)
    channel = message.channel


# decorator which reacts on any reactions added to already existing on all messages
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == config.RULES_ID and payload.message_id == config.RULES_MESSAGE_ID:
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji="✅")
        if str(reaction) == "✅":
            member = payload.member
            unregistered_role = discord.utils.get(member.guild.roles, name="Unregistered")
            await member.add_roles(unregistered_role)


# decorator which output a welcome message into "welcome" channel on user join event
@bot.event
async def on_member_join(member):
    # Get the Unregistered role
    unregistered_role = discord.utils.get(member.guild.roles, name="Unregistered")

    # Assign the Unregistered role to the new member
    if unregistered_role:
        welcome_channel = bot.get_channel(config.WELCOME_ID)
        print(green + f"{member} just joined")
        await welcome_channel.send(f"**{member}** hopped into the server!")


# just a test command to get currently online users on the server
@bot.command()
async def online(ctx):
    online_members = [f'**{member.name}**' for member in ctx.guild.members if member.status == discord.Status.online]
    online_members_str = ', '.join(online_members)

    if online_members_str:
        await ctx.send(f'Currently online members: {online_members_str}')
    else:
        await ctx.send('No members are currently online.')


class CanvasNotificationButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enable", style=discord.ButtonStyle.blurple, custom_id="enableBtn")
    async def enableCanvaNotification(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Enabled", ephemeral=True)
        username = interaction.user.nick.split()
        canvas_notifications.enable_ntf(username[0], username[1])


    @discord.ui.button(label="Disable", style=discord.ButtonStyle.gray, custom_id="disableBtn")
    async def disableCanvaNotification(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Disabled", ephemeral=True)


@bot.command()
async def send(ctx):
    embed = discord.Embed(title="Canvas Notifications",
                          description=f"If you enable these notifications, Griffy will send you personal "
                                      f"notifications about your grades, homework and upcoming assignments.")
    await ctx.send(embed=embed, view=CanvasNotificationButtons())


class RegistrationModal(discord.ui.Modal, title='Registration'):
    user_id = discord.ui.TextInput(
        label='Registration ID',
        placeholder='5 or 6 digit length number...',
        required=True,
        style=discord.TextStyle.short,
        max_length=6)

    async def on_submit(self, interaction: discord.Interaction):
        result = gspread_registration.registrate(int(str(self.user_id)))
        if not result:
            await interaction.response.send_message("Wrong ID...", ephemeral=True)
        else:
            if result[3]:
                await interaction.user.edit(nick=f"{str(result[0])} {str(result[1])}")
                faculty_role = discord.utils.get(interaction.user.guild.roles, name="Faculty")
                unregistered_role = discord.utils.get(interaction.user.guild.roles, name="Unregistered")
                await interaction.user.add_roles(faculty_role)
                await interaction.user.remove_roles(unregistered_role)
            elif not result[3]:
                await interaction.user.edit(nick=f"{str(result[0])} {str(result[1])} {str(result[2])}'")
                student_role = discord.utils.get(interaction.user.guild.roles, name="Student")
                unregistered_role = discord.utils.get(interaction.user.guild.roles, name="Unregistered")
                await interaction.user.add_roles(student_role)
                await interaction.user.remove_roles(unregistered_role)
            await interaction.response.send_message("You've been successfully registered!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


class RegisterButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click me to login", style=discord.ButtonStyle.blurple, custom_id="regBtn")
    async def regBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RegistrationModal())


class SignupModal(discord.ui.Modal, title='New sign-up'):
    name_input = discord.ui.TextInput(
        label='Event name',
        placeholder='Name of event/trip...',
        required=True,
        style=discord.TextStyle.short,
        max_length=50

    )
    date_input = discord.ui.TextInput(
        label='Event date',
        style=discord.TextStyle.short,
        placeholder="MM/DD/YY",
        required=True,
        max_length=8,
    )
    time_input = discord.ui.TextInput(
        label='Event time',
        placeholder='xx:xx',
        required=True,
        style=discord.TextStyle.short,
        max_length=5
    )
    max_attendees_input = discord.ui.TextInput(
        label='Max attendees',
        placeholder='Number of how many people may attend',
        required=True,
        style=discord.TextStyle.short,
        max_length=3
    )
    waitlist_input = discord.ui.TextInput(
        label='Waitlist',
        placeholder='True/False',
        required=True,
        style=discord.TextStyle.short,
        max_length=5
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Event Sign-up", description=f"**Event Name:** {str(self.name_input)}\n"
                                                                 f"**Date:** {str(self.date_input)}\n"
                                                                 f"**Time:** {str(self.time_input)}\n"
                                                                 f"**Max Attendees:** {str(self.max_attendees_input)}\n"
                                                                 f"**Waitlist Enabled:** {str(self.waitlist_input)}\n",
                              color=discord.Color.blue())
        gspread_signup.newsignup(str(self.name_input), str(self.date_input), str(self.time_input),
                                 int(str(self.max_attendees_input)), bool(self.waitlist_input))
        channel = bot.get_channel(config.SIGN_UPS_ID)
        await channel.send(embed=embed,
                           view=SignUpButtons(str(self.name_input), str(self.date_input), str(self.time_input),
                                              int(str(self.max_attendees_input)), bool(self.waitlist_input)))
        await interaction.response.send_message("Sign-up created!", ephemeral=True)


@bot.tree.command(description="Create a new sign-up!")
async def signup(interaction: discord.Interaction):
    if interaction.channel.id == config.SIGN_UPS_ID:
        await interaction.response.send_modal(SignupModal())
    else:
        await interaction.response.send_message(content="Can't be used in this channel!", ephemeral=True)


class SignUpButtons(discord.ui.View):
    def __init__(self, event_name, event_date, event_time, max_attendees, waitlist_enabled):
        super().__init__(timeout=None)  # timeout of the view must be set to None
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.max_attendees = max_attendees
        self.waitlist_enabled = waitlist_enabled

    @discord.ui.button(label="+", style=discord.ButtonStyle.green, custom_id="+btn")
    async def greenBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        nickname = interaction.user.display_name.split()
        print(nickname)
        eph_msg = gspread_signup.adduser(nickname[0], nickname[1], int(nickname[2][:-1]), self.event_name,
                                         int(self.max_attendees),
                                         self.waitlist_enabled)

        await interaction.response.send_message(eph_msg, ephemeral=True)

    @discord.ui.button(label="-", style=discord.ButtonStyle.red, custom_id="-btn")
    async def redBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        nickname = interaction.user.display_name.split()
        eph_msg = gspread_signup.removeuser(nickname[0], nickname[1], self.event_name,
                                            int(self.max_attendees))

        await interaction.response.send_message(eph_msg, ephemeral=True)

    @discord.ui.button(label="End sign-up", style=discord.ButtonStyle.gray, custom_id="end_btn")
    async def EndBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        student_role = discord.utils.get(interaction.guild.roles, name="Student")
        if interaction.user.top_role != student_role:
            gspread_signup.removesignup(self.event_name)
            await interaction.message.delete()
            await interaction.response.send_message("Sign-up was successfully ended!", ephemeral=True)
        else:
            await interaction.response.send_message("Not permitted!", ephemeral=True)


def check_required_args(ctx):
    return len(ctx.message.content.split()) != 6


@bot.command()
async def sync(ctx: commands.Context) -> None:
    synced = await bot.tree.sync()
    await ctx.reply("Synced {} commands".format(len(synced)))


# bot startup
bot.run(config.BOT_TOKEN)
