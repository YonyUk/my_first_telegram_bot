"""
user

this module manage the comunication bettwen the user and the bot
"""

from user.telegram_command_handlers import start_handler,help_handler,list_handler,update_handler,menu_handler,predict_handler,predictx100_handler,predictx10_handler,predict_atomic_handler,predict_value_handler

commands = [
    ('start',start_handler),
    ('help',help_handler),
    ('list',list_handler),
    ('update',update_handler),
    ('list_actions',menu_handler),
    ('predict',predict_handler),
    ('predictx100class',predictx100_handler),
    ('predictx10class',predictx10_handler),
    ('predict_atomic_class',predict_atomic_handler),
    ('predict_value',predict_value_handler)
]