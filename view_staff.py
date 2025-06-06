import discord
import json
from discord import app_commands

def load_account_data():
    try:
        with open('accounts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"GM": [], "QA": [], "Helper": []}

def format_staff_list(staff_list, include_discord=False):
    if not staff_list:
        return "No accounts added (yet!)"

    if include_discord:
        header = "Name       | PlayAcc ID | Discord ID          | Rank\n"
        divider = "-----------|------------|---------------------|-------------------\n"
        body = "\n".join(
            f"{s['name']:<10} | {s['id']:<10} | {str(s.get('discord_id', 'N/A')):<19} | {s.get('rank', 'N/A')}" for s in
            staff_list
        )
    else:
        header = "Name       | PlayAcc ID\n"
        divider = "-----------|------------\n"
        body = "\n".join(
            f"{s['name']:<10} | {s['id']:<10}" for s in staff_list
        )
    return f"```\n{header}{divider}{body}\n```"


@app_commands.command(name="view-staff", description="View all staff members.")
async def view_staff(interaction: discord.Interaction):
    staff_data = load_account_data()
    gm_block = format_staff_list(staff_data.get("GM", []), include_discord=True)
    qa_block = format_staff_list(staff_data.get("QA", []))
    helper_block = format_staff_list(staff_data.get("Helper", []))

    response = f"<:felsong:1364766519149723760> __**GM List**__\n{gm_block}\n<:felsong:1364766519149723760> __**QA List**__\n{qa_block}\n<:felsong:1364766519149723760> __**Helper List**__\n{helper_block}"
    await interaction.response.send_message(response)