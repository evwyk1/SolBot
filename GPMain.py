import time
import os
import pytesseract
from PIL import Image
import pyautogui
import re
import requests  # To send the message to the bot
import winsound  # Windows sound module

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\insid\Tesseract\tesseract.exe'

# Telegram bot details
bot_token = 'xxxx'
chat_id = 'xxxx'

# Exclusion list for vWallet
ExWallets = [ 'A282IV8','ADGEQT','','','','','','','','','',
'BHACF','INSS8Q','AQQUNKM','ATMV7','AQBRAMU','','','','','','','','',
'28ZIV8','FHLNI3','PPYTUXI','YEINSS','EINSS','YEJ3HAC','COPLAB','YEDEQIE','MEDEQIE','RPUKE','AHINTS','8RAMUI','DARWIB','CYHEIR','AHHLNI','INSSQ','ADGQTE','APARWIB','WNKMN','AYTUXOM','ABRAMUI','A33HAC','ASRAMUI',
'INS58Q','BHLN13','QUNKMN','AYTUXI','HHLN13','A282IV','DHLN13','ADEQIE','JP8RAMU','PDGATE','JP28ZIV','7375PF','7391Q','YEHHLN1','YYQUNKM','YYYTUXX','YYSRAMU','MEDEQTE','A202V0','A8RAMUs','AFKETR','HALNI3','33HACF','YYDGQTE','YYINS58','YYDARWI','Y28ZIV8','SRAMUI','YTUXIM','A8RAMU','J3HACF','YEQUNKM','HHIN13','A282Z3','AYTUGM','AIHACF','FKETR','QUNKM',
'ME28ZIV','7609PF','PQUNKM','7631Q','7655PI','7879VE','7902EO','7926EO','7945VE','7961VE','VESEULT','VE70EN','8029E','8042E','8063VE','8087EO','8110EO','8130VE','8145VE','8233E','8250E','8270VE','8296EO','8326EO','8360VE','58387VE','8440E','8459E','8472VE','YYJ3HAC','YFTKETR','9162Q','YEDEQTE','8161PI','METKETR','MEDARWI','9388A8','FKETRL','EQYTUXI','JYTUXI','AEEN','AQMNT','AQON','GIYTUXI','ADEQTEB','AITNOKI','QFKETR','AJSRAMU','FKETR1','DGQTEB','AJSRAMU','QFKETR','AJ3HACT','YEDGQTE',
'8489EO','8510EO','8565VE','8613VE','8613VE','8663E','8680E','8701VE','8730EO','8763EO','8812VE','8859VE','8904E','9360AE','9383E','9498AOS','9524AQ','9593AO','58932E','VEEE','9012AOS','9041VE','9061VE','9112VE','9160E','9174E','9190VE','9226AOS','9258VE','9280VE','9329AO','EA','9439VE','9614AE','9647E','9681E','PINS58Q','JPJ3HAC','PRA2TEN','EQUNKM','PPHHLN1','PYTUXI','PINS58Q','PFKETRI','PDARWI','JPJ3HAC','PPHHLN1','PRINS58','PPDEQT','PPTZ823','YPFKETR','YPQUNKM','YPYTUXI','PPINS58','YESRAMU','PPJ3HAC','YPYTUXI','YESRAMU','AQPARWI','AQPARWI','AQYTUXI','A28ZIV8','DEQTEB','AQPARWI','AQUNKMN','A28ZIV8','AQYTUXI','AINS58','AIT8FED','AQPARWI','HHLNI3','AQYTUXI','MEINS58','AQUNKMN','A28ZIV','AQSRAMU','EDGQTEE','AQUNKM','ADARWIB','AJ3HAC','DHLNI3','AJ8RAMU','YYHHLN1','Y28ZIV8','YYINS58','YYDARWI','YYHHLN1','YJ3HACT','YFTKETR',
'8100A2', '81002', '8195A8', 'MEJ3HAC', '83002', '8314F', '8330Q', '8348I', '8366AY', '8385A8', 'YEINS58','MEYTUXI','XESRAMU','AG8V2D','MEHHLN1','XEJ3HAC','MEDGQTE','EDGQTE','YEDARWI','YE28ZIV','MEFKETR','MEQUNKM','','YEFKETR','XEQUNKM','XE28ZIV','EFKETR','XEQUNKM','AQ8RAMU','PYTUXI'
'8429J', '84742', '8509Q', '8530I', '8577A8', '8628J', '8691A2', '86912', '8713F', '8803A8', 
'8825H', '8848J', '', '8946I', '8914F', '8966AY', '9012H', '9032J', '9112F', '7837E', '7859E',
'FKETRI', 'PPTOKBZ', 'AYTUXIM', 'A8RAMUI', 'AHHLN1', 'J3HACT', 'ADEQTE', 'AQDARWI', '28ZIV8'
    '8825H', '8848J', '', '8946I', '8914F', '8966AY', '9012H', '9032J', '9112F', #'7837E', '7859E',
    'FKETRI', 'PPTOKBZ', 'AYTUXIM', 'A8RAMUI', 'AHHLN1', 'J3HACT', 'ADEQTE', #'AQDARWI', '28ZIV8'
]

x, y, width, height = 110, 470, 1650, 60  # Coordinates for the screenshot region

# Step 1: Print1 - Single Screenshot with 1-second delay at the end
def Print1():
    message = "Hello from your bot!"
    send_telegram_message(message)  # Send the initial message to the bot

   # time.sleep(0.1)  # Delay to allow navigation
   # x, y, width, height = 330, 310, 1040, 35
   # vOutput = read_screen_region(x, y, width, height)  # Capture screen region

    return True

# Step 2: PrintLoop - Capture the region for continuous checks
def PrintLoop():
    #x, y, width, height = 110, 475, 1665, 60
    vOutput = read_screen_region(x, y, width, height)  # Capture screen region
    
    return True

# Function to read the screen region and capture output
def read_screen_region(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    vOutput = pytesseract.image_to_string(screenshot)
    return vOutput

# Step 3: GPFormat - Extract and assign raw variables from latest screenshot
def GPFormat():
    #x, y, width, height = 110, 475, 1665, 60  # Coordinates for the screenshot region
    
    #time.sleep(0.1)
    
    vOutput = read_screen_region(x, y, width, height)
    
    #time.sleep(0.1)
    
    # Assigning variables based on fixed lengths without formatting
    vTimeCurrent = vOutput[:8].strip()  # First 8 characters, trimmed
    
    # vSolTemp is the last 33 characters of vOutput
    vSolTemp = vOutput[-33:]
    vSolParts = vSolTemp.split(' ')  # Split by spaces
    if len(vSolParts) >= 3:
        vSolRaw = vSolParts[1]  # Take the characters between the first and second space
    else:
        vSolRaw = ''  # If not enough parts, assign an empty string

    # Extracting vWallet from vWalletTemp based on spaces
    vWalletTemp = vOutput[-15:]  # Last 15 characters of vOutput
    vWalletParts = vWalletTemp.split(' ', 1)  # Split into 2 parts

    if len(vWalletParts) > 1:
        vWallet = vWalletParts[1].strip()[:8].upper()  
        vWallet = re.sub(r'[^A-Z0-9]', '', vWallet)  
    else:
        vWallet = ''  # If splitting fails, assign empty string

    return vTimeCurrent.strip(), vWallet.strip(), vSolRaw.strip(), vOutput.strip()

# Step 4: IFStatements - Check and process the extracted values
def IFStatements(vTimeCurrent, vWallet, vSolRaw):
    # Output to console
    
    # Make a beep sound (frequency: 100Hz, duration: 100ms)
    winsound.Beep(300, 500)
    print(f"T: {vTimeCurrent} -- W: {vWallet} -- Sol: {vSolRaw}") 


    # Format message to send to Telegram bot
    message = f"{vTimeCurrent} W:{vWallet} S:{vSolRaw}"

    # Send the message to the Telegram bot
    send_telegram_message(message)

# Helper function to send a message to the Telegram bot
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    
    requests.post(url, data=data)  # Send the message silently, without any confirmation
    
    time.sleep(0.25)  # Short delay at the end of the loop 
    

# GPMain Execution with IF2 and IF3 conditions
def GPMain():
    if Print1():  # Step 1
        while True:  # Step 2: Loop begins
            if PrintLoop():  # Step 3
                vTimeCurrent, vWallet, vSolRaw, vOutput = GPFormat()  # Step 4

                # IF2: Check for vWallet, vTime, and vSolRaw conditions
                if len(vTimeCurrent) < 4:  # If vTime is not 8 characters, skip to next loop
                    continue
                elif not vTimeCurrent[-1].isdigit():  # If last character of vTime is not numerical, skip to next loop
                    continue
                elif re.search(r'[^A-Za-z0-9:]', vTimeCurrent):  # If vTimeCurrent contains special characters other than ":"
                    continue
                elif vTimeCurrent[1] == ':':  # If second character of vTime is ':', skip to next loop
                    continue
                else:
                    # IF3: Proceed if vWallet is not in the exclusion list
                    if vWallet not in ExWallets:  # Test against ExWallets
                        IFStatements(vTimeCurrent, vWallet, vSolRaw)  # Conditional checks

          #  time.sleep(0.1)  # Short delay at the end of the loop

# Start GPMain
GPMain()
