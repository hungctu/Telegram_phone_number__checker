import argparse
import asyncio

from config import API_ID, PHONE_NUMBER, API_HASH, BOT_TOKEN
from telethon import TelegramClient, errors, events, sync
from telethon.tl.types import InputPhoneContact
from telethon import functions, types

from getpass import getpass

from phone_country import get_country_flag

result = 0

client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


async def get_names(phone_number):

    try:
        contact =InputPhoneContact(client_id=0, phone=phone_number, first_name="", last_name="")

        contacts = await client(functions.contacts.ImportContactsRequest([contact]))

        print(f"c:{contacts}")

        username = contacts.to_dict()['users'][0]['username']
        print("1")


        if not username:
            print("2")
            print(
                "*" * 5 + f' Response detected, but no user name returned by the API for the number: {phone_number} ' + "*" * 5)

            return 2
        else:
            del_usr = await client(functions.contacts.DeleteContactsRequest(id=[username]))

            return 0
    except IndexError as e:
        print(f'ERROR: there was no response for the phone number: {phone_number}')
        return 1
    except TypeError as e:
        print(f'TypeError: {e}. --> The error might have occured due to the inability to delete the {phone_number} from the contact list.')
        return 3
    except:
        raise


async def user_validator(phone):
    global result
    # phones = phones.split()
    try:
        # for phone in phones:
        api_res = await get_names(phone)
        result = api_res
    except:
        raise

# @client.on(events.NewMessage(pattern='/(?i)/start'))
# async def start(event):
#     sender = await event.get_sender()
#     SENDER = sender.id
#     await client.send_message(SENDER,'hello')

async def client_telegram(phone):
    parser = argparse.ArgumentParser(description='Check to see if a phone number is a valid Telegram account')
    args = parser.parse_args()
    # client.start(bot_token=BOT_TOKEN)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        try:
            await client.sign_in(PHONE_NUMBER, input('Enter the code (sent on telegram): '))
        except errors.SessionPasswordNeededError:
            pw = getpass('Two-Step Verification enabled. Please enter your account password: ')
            await client.sign_in(password=pw)
    await user_validator(phone)

    return result

async def message_telegram(phone_list):
    reg_phones = {}
    unknown_username = {}
    unreg_phones = {}
    error_phone = {}
    for i in phone_list:
        country = get_country_flag(i)
        phone = await client_telegram(i)
        if phone == 0:
            reg_phones[i]= f'{i}  {country} ✅'
        elif phone == 1:
            unreg_phones[i]= f'{i}  {country} ❌'
        elif phone == 2:
            unknown_username[i] = f'{i}  {country} ❗️'
        else:
            error_phone[i] = f'{i} is error phone numbers'

    message = 'Results of phone numbers\n (✅: registered phone number\n ❌: unregistered phone number\n ❗: Response detected, but no user name returned )\n'
    for i in reg_phones.values():
        message += f'{i}\n'
    for i in unreg_phones.values():
        message += f'{i}\n'
    for i in unknown_username.values():
        message += f'{i}\n'
    message += 'END'
    return message